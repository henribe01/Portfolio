from flask import Flask, request, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_consent import Consent
from flask_ckeditor import CKEditor
from flask_babel import Babel

import html
import markdown as md
import bleach
import re
from urllib.parse import urljoin, urlparse
from markupsafe import Markup

from config import Config


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'admin.login'
consent = Consent()
ckeditor = CKEditor()
babel = Babel()
GITHUB_ATTACHMENT_VIDEO_PATTERN = re.compile(
    r'^https://github\.com/user-attachments/assets/[a-zA-Z0-9-]+/?$'
)
DIRECT_VIDEO_URL_PATTERN = re.compile(
    r'^https?://\S+\.(mp4|webm|ogg|mov)(\?\S*)?$',
    re.IGNORECASE
)


def _is_embeddable_video_url(url: str) -> bool:
    return bool(
        GITHUB_ATTACHMENT_VIDEO_PATTERN.fullmatch(url)
        or DIRECT_VIDEO_URL_PATTERN.fullmatch(url)
    )


def _is_relative_url(url: str) -> bool:
    if not url:
        return False

    lowered = url.lower()
    if lowered.startswith(('#', 'mailto:', 'tel:', 'data:')):
        return False

    parsed = urlparse(url)
    return not parsed.scheme and not parsed.netloc


def _resolve_relative_html_urls(html_text: str, readme_base_url: str | None) -> str:
    if not html_text or not readme_base_url:
        return html_text

    if not readme_base_url.endswith('/'):
        readme_base_url = f'{readme_base_url}/'

    attr_pattern = re.compile(r'(?P<prefix>\b(?:src|href)\s*=\s*["\'])(?P<url>[^"\']+)(?P<suffix>["\'])')

    def _replace_attr(match: re.Match[str]) -> str:
        original_url = match.group('url').strip()
        if not _is_relative_url(original_url):
            return match.group(0)

        resolved_url = urljoin(readme_base_url, original_url)
        return f"{match.group('prefix')}{html.escape(resolved_url, quote=True)}{match.group('suffix')}"

    return attr_pattern.sub(_replace_attr, html_text)


def _convert_markdown_video_images(markdown_text: str, readme_base_url: str | None) -> str:
    if not markdown_text:
        return markdown_text

    image_video_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+\.(?:mp4|webm|ogg|mov)(?:\?[^)]*)?)\)', re.IGNORECASE)

    def _replace_video_image(match: re.Match[str]) -> str:
        alt_text = html.escape(match.group(1).strip(), quote=True)
        source_url = match.group(2).strip()
        if readme_base_url and _is_relative_url(source_url):
            source_url = urljoin(readme_base_url if readme_base_url.endswith('/') else f'{readme_base_url}/', source_url)
        escaped_url = html.escape(source_url, quote=True)
        return (
            '<video controls preload="metadata" style="max-width: 100%; height: auto;">'
            f'<source src="{escaped_url}">'
            f'{alt_text or "Video preview"}'
            '</video>'
        )

    return image_video_pattern.sub(_replace_video_image, markdown_text)


def _embed_standalone_media(markdown_text: str, readme_base_url: str | None) -> str:
    embedded_lines = []
    for line in (markdown_text or '').splitlines():
        stripped_line = line.strip()
        maybe_url = stripped_line
        if readme_base_url and _is_relative_url(maybe_url):
            maybe_url = urljoin(readme_base_url if readme_base_url.endswith('/') else f'{readme_base_url}/', maybe_url)

        if _is_embeddable_video_url(maybe_url):
            escaped_url = html.escape(maybe_url, quote=True)
            embedded_lines.append(
                '<video controls preload="metadata" style="max-width: 100%; height: auto;">'
                f'<source src="{escaped_url}">'
                'Your browser does not support the video tag.'
                '</video>'
            )
            continue
        embedded_lines.append(line)

    return '\n'.join(embedded_lines)


def render_markdown(markdown_text: str, readme_base_url: str | None = None) -> Markup:
    normalized_markdown = _convert_markdown_video_images(markdown_text, readme_base_url)
    normalized_markdown = _embed_standalone_media(normalized_markdown, readme_base_url)
    html_output = md.markdown(
        normalized_markdown,
        extensions=['fenced_code', 'tables', 'toc', 'pymdownx.tasklist', 'pymdownx.arithmatex'],
        extension_configs={
            'pymdownx.tasklist': {'custom_checkbox': True},
            'pymdownx.arithmatex': {'generic': True}
        }
    )
    html_output = _resolve_relative_html_urls(html_output, readme_base_url)
    return Markup(html_output)
    

def get_locale():
    lang = session.get('lang')
    if lang in Config.LANGUAGES:
        return lang
    return request.accept_languages.best_match(Config.LANGUAGES) or Config.BABEL_DEFAULT_LOCALE


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    consent.init_app(app)
    ckeditor.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    @app.context_processor
    def inject_current_locale():
        locale = str(get_locale() or app.config.get('BABEL_DEFAULT_LOCALE', 'en'))
        return {'current_locale': locale}
    
    app.jinja_env.filters['markdown'] = render_markdown

    consent.add_standard_categories()

    from portfolio.main import bp as main_bp
    app.register_blueprint(main_bp)

    from portfolio.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
