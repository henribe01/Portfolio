from flask import render_template

from portfolio import app
from portfolio.forms import ContactForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/projects')
def projects():
    return render_template('projects-grid-cards.html')


@app.route('/cv')
def cv():
    return render_template('cv.html')


@app.route('/contact')
def contact():
    contact_form = ContactForm()
    return render_template('contact.html', form=contact_form)
