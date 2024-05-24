import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'MyLittlePony'
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or 'smtp.googlemail.com'
    MAIL_PORT = os.environ.get("MAIL_PORT") or '587'
    MAIL_USE_TLS = int(os.environ.get("MAIL_USE_TLS", "587"))
    FLASKY_ADMIN = "vkevil42@gmail.com"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or 'vkevil42@gmail.com'
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or 'vtoq vgmo czdm akfx'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI") or 'postgresql://postgres:12345@localhost/duglas_adams'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI") or 'postgresql://postgres:12345@localhost/duglas_adams'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI") or 'postgresql://postgres:12345@localhost/duglas_adams'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}