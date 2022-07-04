from flask import render_template

from portfolio.admin import bp


@bp.route('/')
def index():
    return render_template('index_admin.html')


@bp.route('/projects')
def projects():
    return render_template('projects-table.html')


@bp.route('/messages')
def messages():
    return render_template('messages-table.html')
