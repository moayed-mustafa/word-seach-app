# import stuff
import os
from secret import secret
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = secret
    # my database name: word-search-db
    # Get DB_URI from environ variable (useful for production/testing) or,
    # if not set there, use development local db.
    SQLALCHEMY_DATABASE_URI = 'postgres:///word-search-db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False




class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):

    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    # add a secretkey, a database uri here for the production server using os.environ
    pass


class TestingConfig(Config):
    # add a secretkey, a database uri here for testing using os.environ
    TESTING = True
    os.environ['DATABASE_URL'] = "postgresql:///word-search-test"