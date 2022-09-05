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


'''def get_db_connection():
    conn = sqlite3.connect('LID.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post'''


@main.route("/")
def index():
    rowdel = flask.request.values.get("model")
    scores = leaderboard.get_scores()
    #scores = User.query.all()
    return render_template("index.html",
                           scores=scores)


@main.route('/profile')  # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/NER')  # profile page that return 'profile'
@login_required
def NER():
    return render_template('NER.html', name=current_user.name)


@main.route('/POS')  # profile page that return 'profile'
@login_required
def POS():
    return render_template('POS.html', name=current_user.name)


@main.route('/LID')  # profile page that return 'profile'
@login_required
def LID():
    return render_template('LID.html', name=current_user.name)


@main.route('/SA')  # profile page that return 'profile'
@login_required
def SA():
    return render_template('SA.html', name=current_user.name)


@main.route('/MT')  # profile page that return 'profile'
@login_required
def MT():
    return render_template('MT.html', name=current_user.name)


@main.route("/uploader", methods=["GET", "POST"])
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
