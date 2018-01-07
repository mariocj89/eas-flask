"""Tests against the API"""
import json

import pytest
import flask.testing

from eas import app, db, API_URL


class Response(flask.Response):
    @property
    def json(self):
        print(self.data)
        return json.loads(self.data)


class JsonTestClient(flask.testing.FlaskClient):
    def open(self, *args, **kwargs):
        if 'json' in kwargs:
            kwargs['data'] = json.dumps(kwargs.pop('json'))
            kwargs['content_type'] = 'application/json'
        kwargs.setdefault('follow_redirects', True)
        return super().open(*args, **kwargs)


@pytest.fixture(autouse=True)
def clean_db():
    """Ensure the db is created and in a clean state"""
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
    db.create_all()
    yield
    db.session.commit()  # Commit time constraints to be validated
    db.drop_all()


app.response_class = Response
app.test_client_class = JsonTestClient
client = app.test_client()


NUMBER_URL = API_URL + "/random_number/"


def test_create_draw_check_basic_fields():
    result = client.post(NUMBER_URL, json=dict(title="Hello")).json
    res = client.get(NUMBER_URL + result["id"]).json

    assert result == res
    assert result["title"] == "Hello"
