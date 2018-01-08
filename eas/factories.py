from flask import Flask
from . import urls


def create_app():
    app = Flask('flaskr')

    app.config.from_pyfile('eas/config.py')

    register_blueprints(app)
    register_cli(app)
    init_db(app)

    return app


def register_blueprints(app):
    """Register all blueprint modules"""
    from . import api
    app.register_blueprint(api.bp, url_prefix=urls.API_URL)


def register_cli(app):  # pragma: nocover
    @app.cli.command('initdb')
    def initdb_command():
        """Creates the database tables."""
        create_app()
        init_db(app)
        print('Initialized the database.')


def init_db(app):
    from eas.models import db
    db.init_app(app)
