import flask
import os
from flask import Flask, Blueprint, render_template, url_for, request, redirect
from models import Score
from werkzeug.utils import secure_filename, redirect
from flask_login import login_required, current_user
from datetime import datetime
from __init__ import create_app, db
from leaderboard import Leaderboard

DEFAULT_ROUTE_LEADERBOARD = "main.index"
DEFAULT_ROUTE_UPLOADER = "main.uploader"

main = Blueprint('main', __name__)

leaderboard = Leaderboard()


@main.route("/")
def index():
    scores = leaderboard.get_scores()
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
        now = datetime.now()
        f = request.files['file']
        name = model_name + '_' + team_name + '_' + \
            now.strftime("%d-%m-%Y_%H-%M-%S") + '.txt'
        f.save(os.path.join(os.getcwd(), 'Entries', secure_filename(name)))

        score = Score(id=id, model=model_name,
                      team=team_name, model_link=model_link, file_name=name)
        leaderboard.add_score(score)

        return redirect(url_for(DEFAULT_ROUTE_LEADERBOARD))
    else:
        score = Score(model="",
                      team="", model_link="")
        return render_template("uploader.html", score=score)


app = create_app()
db.create_all(app=create_app())
app.run(debug=True)
