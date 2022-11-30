import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin


db = SQLAlchemy()
lm = LoginManager()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    fullname = db.Column(db.String(64), nullable=False)
    photo = db.Column(db.String(256), nullable=False)


class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    comment = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='places')
    added_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
