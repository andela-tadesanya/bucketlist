from flask import Flask
from bucketlist.database import db_session, init_db, init_engine


# application factory function
def create_app(config):

    app = Flask(__name__)

    app.config.from_pyfile(config)

    init_engine(app.config['DATABASE_URI'])

    return app

app = create_app('development_config.py')

# create database
init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# import views and api module
import bucketlist.api
