from datetime import datetime

from portfolio import db


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __repr__(self):
        return '<Admin %r>' % self.username


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    git_url = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Project %r>' % self.name

    def __str__(self):
        return self.name


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Message %r>' % self.name

    def __str__(self):
        return self.name
