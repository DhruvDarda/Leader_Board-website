import zipfile
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
import flask
import os
import sqlite3
from flask import Blueprint, render_template, url_for, request, redirect, abort, send_from_directory, jsonify
#from sklearn import metrics
from models import Score
from werkzeug.utils import secure_filename, redirect
from flask_login import login_required, current_user
from datetime import datetime
from __init__ import create_app, db
from leaderboard import Leaderboard
from models import *
from wtforms import SelectField

LAST_PAGE = "main.index"
DEFAULT_ROUTE_UPLOADER = "main.uploader"

main = Blueprint('main', __name__)

leaderboard = Leaderboard()


@main.route("/")
def index():
    global LAST_PAGE
    LAST_PAGE = "main.index"
    return render_template("index.html")


@main.route('/profile')  # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


class TableUpdateForm(FlaskForm):
    '''conn = sqlite3.connect('db_dataset.sqlite')
    path = conn.execute(
        "SELECT location FROM dataset WHERE task=='{}' ".format(task)).fetchall()
    conn.close()'''
    metrics = SelectField(
        'metrics', choices=[('Accuracy', 'Accuracy'), ('RSME', 'RSME')])
    datasets = SelectField(
        'datasets', choices=[])


@main.route("/POS/", methods=["GET", "POST"])
def POS():
    global LAST_PAGE
    LAST_PAGE = "main.POS"
    conn = sqlite3.connect('db_leaderboard.sqlite')
    if request.method == 'POST':
        # if request.form['AdminDel'][:12] == 'Delete Entry':
        del_id = request.form['AdminDel']
        cursor = conn.cursor()
        cursor.execute("DELETE FROM leaderboard_CM WHERE id == " + del_id)
        conn.commit()
    post = conn.execute(
        "SELECT * FROM leaderboard_CM WHERE pos>=0 order by pos desc").fetchall()
    conn.close()
    conn = sqlite3.connect('db_dataset.sqlite')
    path = conn.execute(
        "SELECT location FROM dataset WHERE task=='POS' ").fetchall()
    conn.close()
    return render_template("POS.html", post=post, datasets=path)


@ main.route("/LID/", methods=["GET", "POST"])
def LID():
    global LAST_PAGE
    LAST_PAGE = "main.LID"
    conn = sqlite3.connect('db_leaderboard.sqlite')
    if request.method == 'POST':
        # if request.form['AdminDel'][:12] == 'Delete Entry':
        del_id = request.form['AdminDel']
        cursor = conn.cursor()
        cursor.execute("DELETE FROM leaderboard_CM WHERE id == " + del_id)
        conn.commit()
    post = conn.execute(
        "SELECT * FROM leaderboard_CM WHERE lid>=0  order by lid desc").fetchall()
    conn.close()
    conn = sqlite3.connect('db_dataset.sqlite')
    path = conn.execute(
        "SELECT location FROM dataset WHERE task=='LID' ").fetchall()
    name = conn.execute(
        "SELECT dataset_name FROM dataset WHERE task=='LID' ").fetchall()
    conn.close()
    print(name)
    return render_template("LID.html", post=post, datasets_names=list(zip(path, name)))


@main.route("/<dataset>")
def dataset_update(dataset):
    conn = sqlite3.connect('db_dataset.sqlite')
    path = conn.execute(
        "SELECT location FROM dataset WHERE task=='{task}' AND dataset_name=={datasetn} ".format(task=LAST_PAGE[5:], datasetn=dataset)).fetchall()
    name = conn.execute(
        "SELECT dataset_name FROM dataset WHERE task=='{task}' AND dataset_name=={datasetn} ".format(task=LAST_PAGE[5:], datasetn=dataset)).fetchall()
    conn.close()
    print(name)
    dataset_array = []
    for i in range(len(path)):
        dataset_obj = {}
        dataset_obj['path'] = path
        dataset_obj['name'] = name
        dataset_array.append(dataset_obj)
    return jsonify({'datasetlist': dataset_array})  # list(zip(path, name))


@main.route("/<metric>")
def metric_update(metric):
    if metric == "Accuracy":
        pass
    return metric


@ main.route("/datasetuploader", methods=["GET", "POST"])
def d_upload():
    if request.method == 'POST':
        f = request.files['file']
        task = request.form.get('flexRadioDefault')
        name = flask.request.values.get("dataset")
        data = Dataset(task=task, dataset_name=name,
                       location=os.path.join(os.getcwd(), 'Datasets', name))
        db.session.add(data)
        db.session.commit()
        f.save(os.path.join(os.getcwd(), 'Datasets', secure_filename(name)))
    return render_template("dataset.html")


@ main.route("/NER/", methods=["GET", "POST"])
def NER():
    global LAST_PAGE
    LAST_PAGE = "main.NER"
    conn = sqlite3.connect('db_leaderboard.sqlite')
    if request.method == 'POST':
        # if request.form['AdminDel'][:12] == 'Delete Entry':
        del_id = request.form['AdminDel']
        cursor = conn.cursor()
        cursor.execute("DELETE FROM leaderboard_CM WHERE id == " + del_id)
        conn.commit()
    post = conn.execute(
        "SELECT * FROM leaderboard_CM WHERE ner>=0 order by ner desc").fetchall()
    conn.close()
    conn = sqlite3.connect('db_dataset.sqlite')
    path = conn.execute(
        "SELECT location FROM dataset WHERE task=='NER' ").fetchall()
    conn.close()
    return render_template("NER.html", post=post, datasets=path)


@ main.route("/SA/", methods=["GET", "POST"])
def SA():
    global LAST_PAGE
    LAST_PAGE = "main.SA"
    conn = sqlite3.connect('db_leaderboard.sqlite')
    if request.method == 'POST':
        # if request.form['AdminDel'][:12] == 'Delete Entry':
        del_id = request.form['AdminDel']
        cursor = conn.cursor()
        cursor.execute("DELETE FROM leaderboard_CM WHERE id == " + del_id)
        conn.commit()
    post = conn.execute(
        "SELECT * FROM leaderboard_CM WHERE sa>=0 order by sa desc").fetchall()
    conn.close()
    conn = sqlite3.connect('db_dataset.sqlite')
    path = conn.execute(
        "SELECT location FROM dataset WHERE task=='SA' ").fetchall()
    conn.close()
    return render_template("SA.html", post=post, datasets=path)


@ main.route("/MT/", methods=["GET", "POST"])
def MT():
    global LAST_PAGE
    LAST_PAGE = "main.MT"
    conn = sqlite3.connect('db_leaderboard.sqlite')
    if request.method == 'POST':
        # if request.form['AdminDel'][:12] == 'Delete Entry':
        del_id = request.form['AdminDel']
        cursor = conn.cursor()
        cursor.execute("DELETE FROM leaderboard_CM WHERE id == " + del_id)
        conn.commit()
    post = conn.execute(
        "SELECT * FROM leaderboard_CM WHERE mt>=0 order by mt desc").fetchall()
    conn.close()
    conn = sqlite3.connect('db_dataset.sqlite')
    path = conn.execute(
        "SELECT location FROM dataset WHERE task=='MT' ").fetchall()
    conn.close()
    return render_template("MT.html", post=post, datasets=path)


class SubmissionForm(FlaskForm):
    submission = FileField(validators=[FileRequired()])


@ main.route("/uploader", methods=["GET", "POST"])
@ login_required
def uploader():
    if request.method == 'POST':
        id = flask.request.values.get("id")
        model_name = flask.request.values.get("model")
        team_name = flask.request.values.get("team")
        model_link = flask.request.values.get("model_link")
        tasks = request.form.get('select1')
        now = datetime.now()
        f = request.files['file']
        name = model_name + '_' + team_name + '_' + \
            now.strftime("%d-%m-%Y_%H-%M-%S") + '.txt'
        f.save(os.path.join(os.getcwd(), 'Entries', secure_filename(name)))

        score = Score(id=id, model=model_name,
                      team=team_name, model_link=model_link, file_name=name, tasks=tasks)
        leaderboard.add_score(score)

        return redirect(url_for(LAST_PAGE))
    else:
        score = Score(model="",
                      team="", model_link="")
        return render_template("uploader.html", score=score)


app = create_app()
db.create_all(app=create_app())
app.run(debug=True)
