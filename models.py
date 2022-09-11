from ast import Pass
from flask_login import UserMixin
from __init__ import db
import sqlite3


class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


def num_rows():
    try:
        conn = sqlite3.connect('db_leaderboard.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM leaderboard_CM")
        results = cursor.fetchall()
        return len(results)
    except:
        return 0


class Score():
    def __init__(self, model, team, model_link, file_name="no_name", id=num_rows()+1, tasks=[]):
        self.id = id
        self.model = model
        self.team = team
        self.model_link = model_link
        self.file_name = file_name
        self.tasks = tasks


class Leaderboard_CM(db.Model):
    __bind_key__ = 'leaderboard'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    model = db.Column(db.String(100))
    team = db.Column(db.String(100))
    link = db.Column(db.String(1000))
    rank = db.Column(db.Integer)
    lid = db.Column(db.Float)
    ner = db.Column(db.Float)
    pos = db.Column(db.Float)
    sa = db.Column(db.Float)
    mt = db.Column(db.Float)
