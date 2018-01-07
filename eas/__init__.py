import flask

from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from . import models
from . import api

db.create_all()
app.register_blueprint(api.bp, url_prefix="/api/v1")

