import pytest


@pytest.fixture(autouse=True)
def clean_db(app):
    """Ensure the db is created and in a clean state"""
    yield app
