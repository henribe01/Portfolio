from flask import render_template, url_for, redirect, request
from flask_login import current_user, login_user, login_required

from portfolio.admin import bp
from portfolio.admin.forms import LoginForm
from portfolio.models import Admin


@bp.route('/')
@login_required
def index():
    return render_template('index_admin.html')


@bp.route('/projects')
@login_required
def projects():
    return render_template('projects-table.html')


@bp.route('/messages')
@login_required
def messages():
    return render_template('messages-table.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('admin.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('admin.index'))
    return render_template('login.html', form=form)
