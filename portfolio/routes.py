from flask import render_template

from portfolio import app


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
    return render_template('contact.html')
