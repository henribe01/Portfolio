from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_consent import Consent
from flask_ckeditor import CKEditor

import html
import markdown as md
import bleach
import re
from markupsafe import Markup

from config import Config


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'admin.login'
consent = Consent()
ckeditor = CKEditor()

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


def _embed_standalone_media(markdown_text: str) -> str:
    embedded_lines = []
    for line in (markdown_text or '').splitlines():
        stripped_line = line.strip()
        if _is_embeddable_video_url(stripped_line):
            escaped_url = html.escape(stripped_line, quote=True)
            embedded_lines.append(
                '<video controls preload="metadata" style="max-width: 100%; height: auto;">'
                f'<source src="{escaped_url}">'
                'Your browser does not support the video tag.'
                '</video>'
            )
            continue
        embedded_lines.append(line)

    return '\n'.join(embedded_lines)


def render_markdown(markdown_text: str) -> Markup:
    html = md.markdown(
        _embed_standalone_media(markdown_text),
        extensions=['fenced_code', 'tables', 'toc', 'pymdownx.tasklist', 'pymdownx.arithmatex'],
        extension_configs={
            'pymdownx.tasklist': {'custom_checkbox': True},
            'pymdownx.arithmatex': {'generic': True}
        }
    )
    return Markup(html)
    


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    consent.init_app(app)
    ckeditor.init_app(app)
    
    app.jinja_env.filters['markdown'] = render_markdown

    consent.add_standard_categories()

    from portfolio.main import bp as main_bp
    app.register_blueprint(main_bp)

    from portfolio.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
