import datetime
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from config import config
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
def create_app(config_name="default"):
    an_app = Flask(__name__)
    an_app.permanent_session_lifetime = datetime.timedelta(days=365)
    an_app.config.from_object(config[config_name])
    config[config_name].init_app(an_app)
    mail.init_app(an_app)
    db.init_app(an_app)
    login_manager.init_app(an_app)

    from .main import main as main_blueprint
    an_app.register_blueprint(main_blueprint, config=config)

    from .auth import auth as auth_blueprint
    an_app.register_blueprint(auth_blueprint, url_prefix='/auth')
    return an_app



