import json

import pytest
import flask.testing

from eas import factories, models


@pytest.fixture()
def app():
    """Ensure the db is created and in a clean state"""
    # TODO: add a check that we are hitting in memory sqlite?
    app = factories.create_app()
    with app.app_context():
        models.db.create_all()
        yield app
        models.db.session.commit()  # Commit time constraints to be validated
        models.db.drop_all()


@pytest.fixture()
def api(app):
    app.response_class = Response
    app.test_client_class = JsonTestClient
    yield app.test_client()


class Response(flask.Response):
    @property
    def json(self):
        return json.loads(self.data)


class JsonTestClient(flask.testing.FlaskClient):
    def open(self, *args, **kwargs):
        if 'json' in kwargs:
            kwargs['data'] = json.dumps(kwargs.pop('json'))
            kwargs['content_type'] = 'application/json'
        kwargs.setdefault('follow_redirects', True)
        return super().open(*args, **kwargs)

