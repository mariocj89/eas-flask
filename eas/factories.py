import os

from flask import Flask
from . import urls


def create_app():
    app = Flask('flaskr')

    if "EAS_SETTINGS" not in os.environ:  # pragma: no cover
        raise RuntimeError(
            "Set the configuration file in the environment variable EAS_SETTINGS.\n"
            "Example: export EAS_SETTINGS=eas/settings/dev.py"
        )
    app.config.from_envvar("EAS_SETTINGS")

    register_blueprints(app)
    register_cli(app)
    init_db(app)
    setup_sentry(app)

    if app.config.get("CREATE_DB"):  # pragma: no cover
        create_db(app)

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


def create_db(app):  # pragma: no cover
    from eas.models import db
    with app.app_context():
        db.create_all()

def setup_sentry(app):  # pragma: no cover
    if app.config.get("ENABLE_SENTRY"):
        if "SENTRY_DSN" not in os.environ:
            raise RuntimeError("Please set SENTRY_DSN")
        from raven.contrib.flask import Sentry
        sentry = Sentry(app)
