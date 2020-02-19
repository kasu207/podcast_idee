from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) #represents DB
migrate = Migrate(app, db) #represents Migrate Engine

login = LoginManager(app) #initiierung FlaskLogin
login.login_view = 'login'

from app import routes, models