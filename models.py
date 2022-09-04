from flask_login import UserMixin
from __init__ import db


class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Score():
    def __init__(self, model, team, model_link, file_name="no_name", id='unique'):
        self.id = id
        self.model = model
        self.team = team
        self.model_link = model_link
        self.file_name = file_name
