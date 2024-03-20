import os

from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
an_app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))

an_app.config['SECRET_KEY'] = 'MyLittlePony'
an_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/duglas_adams'
an_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

an_app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
an_app.config['MAIL_PORT'] = 587
an_app.config['MAIL_USE_TLS'] = True

mail = Mail(an_app)
db = SQLAlchemy(an_app)
from models import *
migrate = Migrate(an_app, db)
from app import routes