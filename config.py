#Whoosh does not work on Heroku
WHOOSH_ENABLED = os.environ.get('HEROKU') is None
