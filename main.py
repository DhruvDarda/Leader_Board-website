import flask
import os
import sqlite3
from flask import Blueprint, render_template, url_for, request, redirect, abort
from models import Score
from werkzeug.utils import secure_filename, redirect
from flask_login import login_required, current_user
from datetime import datetime
from __init__ import create_app, db
from leaderboard import Leaderboard
from models import *

DEFAULT_ROUTE_LEADERBOARD = "main.index"
DEFAULT_ROUTE_UPLOADER = "main.uploader"

main = Blueprint('main', __name__)

leaderboard = Leaderboard()


@main.route("/")
def index():
    return render_template("index.html")


@main.route('/profile')  # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route("/POS/", methods=["GET", "POST"])
def POS():
    path = 'Datasets/POS/'
    conn = sqlite3.connect('db_leaderboard.sqlite')
    if request.method == 'POST':
        # if request.form['AdminDel'][:12] == 'Delete Entry':
        del_id = request.form['AdminDel']
        cursor = conn.cursor()
        cursor.execute("DELETE FROM leaderboard_CM WHERE id == " + del_id)
        conn.commit()
    post = conn.execute("SELECT * FROM leaderboard_CM WHERE pos>=0").fetchall()
    conn.close()
    return render_template("POS.html", post=post, datasets=os.listdir(path))


@main.route("/LID/", methods=["GET", "POST"])
def LID():
    path = 'Datasets/LID/'
    conn = sqlite3.connect('db_leaderboard.sqlite')
    if request.method == 'POST':
        # if request.form['AdminDel'][:12] == 'Delete Entry':
        del_id = request.form['AdminDel']
        cursor = conn.cursor()
        cursor.execute("DELETE FROM leaderboard_CM WHERE id == " + del_id)
        conn.commit()
    post = conn.execute("SELECT * FROM leaderboard_CM WHERE lid>=0").fetchall()
    conn.close()
    return render_template("LID.html", post=post, datasets=os.listdir(path))


@main.route("/NER/", methods=["GET", "POST"])
def NER():
    path = 'Datasets/NER/'
    conn = sqlite3.connect('db_leaderboard.sqlite')
    if request.method == 'POST':
        # if request.form['AdminDel'][:12] == 'Delete Entry':
        del_id = request.form['AdminDel']
        cursor = conn.cursor()
        cursor.execute("DELETE FROM leaderboard_CM WHERE id == " + del_id)
        conn.commit()
    post = conn.execute("SELECT * FROM leaderboard_CM WHERE ner>=0").fetchall()
    conn.close()
    return render_template("NER.html", post=post, datasets=os.listdir(path))


@main.route("/SA/", methods=["GET", "POST"])
def SA():
    path = 'Datasets/SA/'
    conn = sqlite3.connect('db_leaderboard.sqlite')
    if request.method == 'POST':
        # if request.form['AdminDel'][:12] == 'Delete Entry':
        del_id = request.form['AdminDel']
        cursor = conn.cursor()
        cursor.execute("DELETE FROM leaderboard_CM WHERE id == " + del_id)
        conn.commit()
    post = conn.execute("SELECT * FROM leaderboard_CM WHERE sa>=0").fetchall()
    conn.close()
    return render_template("SA.html", post=post, datasets=os.listdir(path))


@main.route("/MT/", methods=["GET", "POST"])
def MT():
    path = 'Datasets/MT/'
    conn = sqlite3.connect('db_leaderboard.sqlite')
    if request.method == 'POST':
        # if request.form['AdminDel'][:12] == 'Delete Entry':
        del_id = request.form['AdminDel']
        cursor = conn.cursor()
        cursor.execute("DELETE FROM leaderboard_CM WHERE id == " + del_id)
        conn.commit()
    post = conn.execute("SELECT * FROM leaderboard_CM WHERE mt>=0").fetchall()
    conn.close()
    return render_template("MT.html", post=post, datasets=os.listdir(path))


@main.route("/uploader", methods=["GET", "POST"])
@login_required
def uploader():
    if request.method == 'POST':
        id = flask.request.values.get("id")
        model_name = flask.request.values.get("model")
        team_name = flask.request.values.get("team")
        model_link = flask.request.values.get("model_link")
        tasks = request.form.getlist('flexCheckChecked')
        now = datetime.now()
        f = request.files['file']
        name = model_name + '_' + team_name + '_' + \
            now.strftime("%d-%m-%Y_%H-%M-%S") + '.txt'
        f.save(os.path.join(os.getcwd(), 'Entries', secure_filename(name)))

        score = Score(id=id, model=model_name,
                      team=team_name, model_link=model_link, file_name=name, tasks=tasks)
        leaderboard.add_score(score)

        return redirect(url_for(DEFAULT_ROUTE_LEADERBOARD))
    else:
        score = Score(model="",
                      team="", model_link="")
        return render_template("uploader.html", score=score)


app = create_app()
db.create_all(app=create_app())
app.run(debug=True)
