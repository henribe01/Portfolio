from flask import render_template, flash, redirect, url_for

from portfolio import app
from portfolio.forms import ContactForm
from portfolio.models import Project

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects-grid-cards.html', projects=projects)


@app.route('/cv')
def cv():
    return render_template('cv.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        #TODO: Send email
        flash('Ihre Nachricht wurde erfolgreich versendet.')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=contact_form)


@app.route('/admin')
def admin():
    #TODO: Create admin login
    #TODO: Create admin dashboard
    return render_template('admin.html')