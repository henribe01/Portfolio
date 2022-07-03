from flask import render_template, flash, redirect, url_for

from portfolio import app
from portfolio.forms import ContactForm
from portfolio.models import Project


@app.route('/')
@app.route('/index')
def index():
    latest_projects = Project.query.order_by(Project.date.desc()).limit(app.config.get('CAROUSEL_AMOUNT'))
    return render_template('index.html', latest_projects=latest_projects)


@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects-grid-cards.html', projects=projects)


@app.route('/project/<project_name>')
def project(project_name):
    project = Project.query.filter_by(name=project_name).first()
    return render_template('project-page.html', project=project)


@app.route('/cv')
def cv():
    return render_template('cv.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        # TODO: Send email
        flash('Ihre Nachricht wurde erfolgreich versendet.')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=contact_form)


@app.route('/admin')
def admin():
    # TODO: Create admin login
    # TODO: Create admin dashboard
    return render_template('admin.html')
