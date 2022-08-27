#from xml.parsers.expat import model
import flask
import os
from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap
from leaderboard import Leaderboard
from models import Score
from werkzeug.utils import secure_filename, redirect
from datetime import datetime

DEFAULT_ROUTE_LEADERBOARD = "index"
DEFAULT_ROUTE_UPLOADER = "uploader"

app = Flask(__name__, template_folder='templates')
Bootstrap(app)


leaderboard = Leaderboard()


@app.route("/")
def index():
    scores = leaderboard.get_scores()
    return render_template("index.html",
                           scores=scores)


@app.route("/uploader", methods=["GET", "POST"])
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
