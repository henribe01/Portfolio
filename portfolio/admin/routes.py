import os

from flask import render_template, url_for, redirect, request, flash, \
    current_app
from flask_login import current_user, login_user, login_required
from werkzeug.utils import secure_filename

from portfolio import db
from portfolio.admin import bp
from portfolio.admin.forms import LoginForm, ProjectForm
from portfolio.models import Admin, Project, Messages


@bp.route('/')
@login_required
def index():
    return render_template('index_admin.html')


@bp.route('/projects', methods=['GET', 'POST'])
@login_required
def projects():
    page = request.args.get('page', 1, type=int)
    projects = Project.query.order_by(Project.date.desc()).paginate(page=page,
                                                                    per_page=10,
                                                                    error_out=False)# TODO: Replace 10 with settings from page
    # TODO: Add pagination in html
    if request.method == 'POST':
        return redirect(url_for('admin.create_project'))
    return render_template('projects-table.html', projects=projects.items)


@bp.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    project_form = ProjectForm()
    if project_form.validate_on_submit():
        uploaded_image = request.files.get('image')
        if uploaded_image.filename != '':
            uploaded_image.save(
                os.path.join(current_app.config['UPLOAD_FOLDER'],
                             secure_filename(uploaded_image.filename)))
        description = project_form.description.data
        # Turn escape characters into html tags
        description = description.replace('&lt;', '<')
        description = description.replace('&gt;', '>')
        description = description.replace('&quot;', '"')
        description = description.replace('&amp;', '&')
        project = Project(name=project_form.name.data,
                          description=description,
                          image=uploaded_image.filename,
                          git_url=project_form.git_url.data)
        db.session.add(project)
        db.session.commit()
        flash('Project created!')
        return redirect(url_for('admin.projects'))
    return render_template('create_project.html', form=project_form)


@bp.route('/delete_project/<int:id>')
@login_required
def delete_project(id):
    project = Project.query.get(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted!')
    return redirect(url_for('admin.projects'))


@bp.route('/messages')
@login_required
def messages_table():
    messages = Messages.query.order_by(Messages.unread.desc(),
                                       Messages.date.desc()).all()
    return render_template('messages-table.html', messages=messages)


@bp.route('/message/<int:id>', methods=['GET', 'PUT'])
@login_required
def message(id):
    message = Messages.query.get(id)
    if request.method == 'PUT':
        if message.unread:
            message.unread = False
        else:
            message.unread = True
        db.session.commit()
    return message.to_json()


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
