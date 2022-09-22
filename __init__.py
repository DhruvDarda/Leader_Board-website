########################################################################
#################        Importing packages      #######################
########################################################################
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import flask_sijax


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')


def create_app():
    # creates the Flask instance, __name__ is the name of the current Python module
    app = Flask(__name__, template_folder='templates')
    Bootstrap(app)
    # it is used by Flask and extensions to keep data safe
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SIJAX_STATIC_PATH'] = path
    app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
    # it is the path where the SQLite database file will be saved
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_profile.sqlite'
    app.config['SQLALCHEMY_BINDS'] = {
        'leaderboard': 'sqlite:///db_leaderboard.sqlite', 'dataset':'sqlite:///db_dataset.sqlite'}
    # deactivate Flask-SQLAlchemy track modifications
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  # Initialiaze sqlite database
    flask_sijax.Sijax(app)
    # The login manager contains the code that lets your application and Flask-Login work together
    login_manager = LoginManager()  # Create a Login Manager instance
    # define the redirection path when login required and we attempt to access without being logged in
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)  # configure it for login
    from models import User

    @login_manager.user_loader
    def load_user(user_id):  # reload user object from the user ID stored in the session
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    # blueprint for auth routes in our app
    # blueprint allow you to orgnize your flask app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    # blueprint for non-auth parts of app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
