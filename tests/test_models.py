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


def test_update_draw_changes_last_updated():
    rn = factories.SimpleNumber.create()
    models.db.session.commit()
    assert rn.created == rn.last_updated
    rn.title = "New title"
    models.db.session.commit()
    assert rn.title == "New title"
    assert rn.created != rn.last_updated


def test_dates_have_timezones():
    rn = factories.SimpleNumber.create()
    models.db.session.commit()
    assert rn.created.tzinfo
    assert rn.last_updated.tzinfo
    obj = models.RandomNumber.query.get(rn.id)
    assert obj.created.tzinfo
    assert obj.last_updated.tzinfo


def test_generate_result():
    rn = factories.SimpleNumber.create()
    res = rn.toss()
    models.db.session.commit()

    assert res == rn.results[0].value
    assert 1 == len(rn.results)

    # Check order is kept
    res2 = rn.toss()
    models.db.session.commit()

    assert 2 == len(rn.results)
    assert res2 == rn.results[0].value
    assert res == rn.results[1].value

    # exercise result repr
    assert str(res) in repr(rn.results[1])


def test_results_are_limited():
    limit = models.DrawBaseModel._RESULT_LIMIT
    rn = factories.SimpleNumber.create()
    for _ in range(limit * 2):
        rn.toss()

    assert limit == len(rn.results)

