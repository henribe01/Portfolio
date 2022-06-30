from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ContactForm(FlaskForm):
    name = StringField('Ihr Name', validators=[DataRequired()])
    subject = StringField('Betreff', validators=[DataRequired()])
    email = EmailField('E-Mail', validators=[DataRequired()])
    message = TextAreaField('Nachricht', validators=[DataRequired()])
    submit = SubmitField('Abschicken')