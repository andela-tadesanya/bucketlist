from flask import Flask
app = Flask(__name__)

from bucketlist.database import db_session, init_db

# setup config
app.config.from_object(__name__)

# setup default config 
app.config.update(dict(
    DATABASE='sqlite:///bucket.db',
    DEBUG=True,
    SECRET_KEY='development key',
    JSON_SORT_KEYS=False,
))

# override config from an environment variable
app.config.from_envvar('BUCKETLIST_SETTINGS', silent=True)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# create database
init_db()

# import views and api module
import bucketlist.views
import bucketlist.api
