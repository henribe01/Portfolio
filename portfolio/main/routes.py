from flask import render_template, flash, redirect, url_for, current_app

from portfolio import db
from portfolio.main import bp
from portfolio.main.forms import ContactForm
from portfolio.models import Project, Messages


@bp.route('/')
@bp.route('/index')
def index():
    latest_projects = Project.query.order_by(Project.date.desc()).limit(
        current_app.config.get('CAROUSEL_AMOUNT'))
    return render_template('index.html', latest_projects=latest_projects)


@bp.route('/projects')
def projects():
    projects = Project.query.order_by(Project.date.desc()).all()
    return render_template('projects-grid-cards.html', projects=projects)


@bp.route('/project/<project_name>')
def project(project_name):
    project = Project.query.filter_by(name=project_name).first()
    latest_projects = Project.query.order_by(Project.date.desc()).limit(4)
    return render_template('project-page.html', project=project,
                           latest_projects=latest_projects)


@bp.route('/cv')
def cv():
    return render_template('cv.html')


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
        flash('Ihre Nachricht wurde erfolgreich versendet.')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', form=contact_form)


@bp.route('/admin')
def admin():
    # TODO: Create admin login
    # TODO: Create admin dashboard
    return render_template('admin.html')
