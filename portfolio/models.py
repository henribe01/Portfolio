from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from portfolio import db, login


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(255))

    def __repr__(self):
        return '<Admin %r>' % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    git_url = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    readme = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return '<Project %r>' % self.name

    def __str__(self):
        return self.name


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    unread = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Message %r>' % self.name

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'subject': self.subject,
            'email': self.email,
            'message': self.message,
            'date': self.date,
            'unread': self.unread
        }
