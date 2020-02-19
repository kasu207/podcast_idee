import os
basedir = os.path.abspath(os.path.dirname(__file__))
#abspath returns absolute path of path 
#join join to path strings
#dirname returns the directory of a file
#__file__ refers to the scripts filename



class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False