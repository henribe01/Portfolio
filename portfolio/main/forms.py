from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
    name = StringField(_l('Your name'), validators=[DataRequired()])
    subject = StringField(_l('Subject'), validators=[DataRequired()])
    email = EmailField(_l('Email'), validators=[DataRequired()])
    message = TextAreaField(_l('Message'), validators=[DataRequired()])
    submit = SubmitField(_l('Send'))
