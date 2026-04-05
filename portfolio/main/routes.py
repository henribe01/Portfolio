from flask import render_template, flash, redirect, url_for, current_app, send_from_directory, abort, request, session
from flask_babel import _
from urllib.parse import quote

from portfolio import db
from portfolio.main import bp
from portfolio.main.forms import ContactForm
from portfolio.models import Project, Messages


@bp.route('/')
@bp.route('/index')
def index():
    latest_projects = Project.query.order_by(Project.date.desc()).limit(
        current_app.config.get('CAROUSEL_AMOUNT'))
    return render_template('index.html', latest_projects=latest_projects, title=_('Home'))


@bp.route('/projects')
def projects():
    projects = Project.query.order_by(Project.date.desc()).all()
    return render_template('projects-grid-cards.html', projects=projects, title=_('Projects'))


@bp.route('/project/<project_name>')
def project(project_name):
    project = Project.query.filter_by(name=project_name).first()
    if project is None:
        abort(404)

    latest_projects = Project.query.order_by(Project.date.desc()).limit(4)
    # Get the readme file content from git_url
    readme = ''
    readme_base_url = None
    if project.git_url:
        clean_repo_url = project.git_url.rstrip('/')
        raw_repo_url = clean_repo_url.replace('github.com', 'raw.githubusercontent.com')
        try:
            import requests
            for branch in ('main', 'master'):
                readme_base_url = f'{raw_repo_url}/refs/heads/{quote(branch)}/'
                for readme_name in ('README.md', 'readme.md'):
                    response = requests.get(f'{readme_base_url}{readme_name}')
                    if response.status_code == 200:
                        readme = response.text
                        break
                if readme:
                    break

            if not readme:
                readme_base_url = None
                readme = project.description
        except Exception as e:
            print(f'Error fetching README: {e}')
            readme_base_url = None
            readme = project.description

    return render_template('project-page.html', project=project,
                           latest_projects=latest_projects, title=project.name,
                           readme=readme, readme_base_url=readme_base_url)


@bp.route('/cv')
def cv():
    return render_template('cv.html', title=_('CV'))


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        message = Messages(name=contact_form.name.data,
                           subject=contact_form.subject.data,
                           email=contact_form.email.data,
                           message=contact_form.message.data)
        db.session.add(message)
        db.session.commit()
        flash(_('Your message has been sent successfully.'))
        return redirect(url_for('main.contact'))
    return render_template('contact.html', form=contact_form, title=_('Contact'))

@bp.route('/download/<filename>')
def download(filename):
    return send_from_directory(current_app.config.get('DOWNLOAD_FOLDER'), filename)

@bp.route('/set-language/<lang>')
def set_language(lang):
    if lang in current_app.config.get('LANGUAGES'):
        session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))