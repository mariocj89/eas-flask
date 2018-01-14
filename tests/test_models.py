import pytest
from . import factories

from eas import models


@pytest.fixture(autouse=True)
def clean_db(app):
    """Ensure the db is created and in a clean state"""
    yield app


def test_create_with_defaults():
    rn = models.RandomNumber(**factories.SimpleNumber.dict())
    for f in ["id", "private_id", "created"]:
        assert getattr(rn, f) is not None


def test_create_with_fields():
    rn = models.RandomNumber(
        **factories.PublicNumber.dict(title="sample_title")
    )
    assert rn.title == "sample_title"


def test_random_number_create_unique_id():
    ids = [r.id for r in (factories.SimpleNumber.create() for _ in range(50))]
    assert len(models.RandomNumber.query.all()) == 50
    assert len(ids) == len(set(ids))


def test_draw_repr():
    rn = factories.SimpleNumber.create()
    assert rn.id in repr(rn)
    assert rn.__class__.__name__ in repr(rn)

