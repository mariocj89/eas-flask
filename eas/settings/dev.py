"""Settings for the dev environment"""
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True

# Creates the db at startup
CREATE_DB = True

ENABLE_SENTRY = True
