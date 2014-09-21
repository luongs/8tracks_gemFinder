import os
#Whoosh does not work on Heroku
#WHOOSH_ENABLED = os.environ.get('HEROKU') is None,
SECRET_KEY = os.urandom(24)
DEBUG = False