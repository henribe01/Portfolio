from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    URLField
from wtforms.validators import DataRequired, URL


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    image = FileField('Image',
                      validators=[FileRequired(),
                                  FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    git_url = URLField('Git URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Create Project')
