import os
basedir = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'sgapp.db') #not usable on heroku
# SQLALCHEMY_DATABASE_URI = 'postgresql://' + os.path.join(basedir, 'sgapp.db')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# WTF_CSRF_ENABLED = True
# SECRET_KEY = 'you-will-never-guess'


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'oqEr[]*woi+145@#11!&$fsa%(Mn21eq'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    # SERVER_NAME = 'sgapp.local:4000'

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://roberto:qwerty@localhost/scgames'
    #SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'
# class ProductionConfig(Config):
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = 'postgres://fgtyoqghtksdtu:K6gbedf7P9_rI24UtS2AgH08Je@ec2-184-73-165-195.compute-1.amazonaws.com:5432/dbju68qkts7mte'
#     # SERVER_NAME = 'sourgame.herokuapp.com'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://roberto:qwerty@localhost/scgames_test'
    # SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'


# class StagingConfig(Config):
#     DEVELOPMENT = True