import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'MyLittlePony'
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or 'smtp.googlemail.com'
    MAIL_PORT = os.environ.get("MAIL_PORT") or '587'
    MAIL_USE_TLS = int(os.environ.get("MAIL_USE_TLS", "587"))

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or 'mysql://root:@localhost/duglas_adams'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or 'mysql://root:@localhost/duglas_adams'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or 'mysql://root:@localhost/duglas_adams'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}