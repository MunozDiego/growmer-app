import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///growmer.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')

class ProductionConfig(Config):
    dir_path = os.path.join(os.environ['APPDATA'], 'GROWMER APP BETA')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_path = os.path.join(dir_path, 'growmer.db')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path

config = {
 'development': DevelopmentConfig,
 'testing': TestingConfig,
 'production': ProductionConfig,
 'default': DevelopmentConfig
}