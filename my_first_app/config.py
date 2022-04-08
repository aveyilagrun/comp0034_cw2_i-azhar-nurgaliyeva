"""Flask config module."""

from pathlib import Path


class Config(object):
    """ General config """
    DEBUG = False
    SECRET_KEY = 'mmw3Wv8FToV1qGxo1Bo_VA'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """ Config for production environment """
    ENV = 'production'


class DevelopmentConfig(Config):
    """ Config for development environment """
    ENV = 'development'
    DEBUG = True
    DATA_PATH = Path('data')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(DATA_PATH.joinpath('example.sqlite'))
    SQLALCHEMY_ECHO = True
    MAIL_SERVER = 'smtp.mail.yahoo.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'azharnurgaliyeva@yahoo.com'
    MAIL_PASSWORD = 'plvfojhklclmtzmv'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False


class TestingConfig(Config):
    """ Config for testing environment """
    ENV = 'testing'
    TESTING = True
    SQLALCHEMY_ECHO = True
