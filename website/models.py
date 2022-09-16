import email
from email.policy import default
from enum import unique
from website import db 
from flask_login import UserMixin
from sqlalchemy.sql import func


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(150))
    year = db.Column(db.Integer)
    edition = db.Column(db.Integer)
    image = db.Column(db.String(500))
    amount = db.Column(db.Integer)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    #books= db.relationship('Book')