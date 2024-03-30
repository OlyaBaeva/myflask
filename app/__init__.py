from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config
mail = Mail()
db = SQLAlchemy()

def create_app(config_name="default"):
    an_app = Flask(__name__)
    an_app.config.from_object(config[config_name])
    config[config_name].init_app(an_app)
    mail.init_app(an_app)
    db.init_app(an_app)

    from .main import main as main_blueprint
    an_app.register_blueprint(main_blueprint)

    return an_app



