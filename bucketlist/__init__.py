from flask import Flask
app = Flask(__name__)

import bucketlist.views
from bucketlist.database import db_session


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()