from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
#from models import Player
import os


login_manager = LoginManager()

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return Player.query.get(int(userid))


from app import views
from .admin import views, forms, admin_functions
from .demandgame import views
from models import *
from game_functions import *
