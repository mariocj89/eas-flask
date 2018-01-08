import pytest

import sqlalchemy.exc

from eas import models, factories


@pytest.fixture(autouse=True)
def clean_db():
    """Ensure the db is created and in a clean state"""
    # TODO: add a check that we are hitting in memory sqlite?
    app = factories.create_app()
    with app.app_context():
        models.db.create_all()
        yield
        models.db.session.commit()  # Commit time constraints to be validated
        models.db.drop_all()


def test_random_number_create_defaults():
    rn = models.RandomNumber.create()
    assert rn.range_max == models.RandomNumber.DEFAULT_MAX
    assert rn.range_min == models.RandomNumber.DEFAULT_MIN
    assert rn.id is not None


def test_random_number_create_unique_id():
    ids = [r.id for r in (models.RandomNumber.create() for _ in range(50))]
    assert len(models.RandomNumber.query.all()) == 50
    assert len(ids) == len(set(ids))


def test_random_number_create_with_custom_args():
    rn = models.RandomNumber.create(
        title="Example Draw",
        range_min=5,
        range_max=10,
    )
    assert rn.range_max == 10
    assert rn.range_min == 5
    assert rn.title == "Example Draw"


@pytest.mark.parametrize("values", [
    dict(range_min=-1),
    dict(range_max=-1),
    dict(range_min=15, range_max=10),
])
def test_random_number_invalid_config(values):
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        models.RandomNumber.create(**values)
    models.db.session.rollback()


def test_draw_repr():
    rn = models.RandomNumber.create()
    assert rn.id in repr(rn)
    assert rn.__class__.__name__ in repr(rn)


def test_draw_field_description():
    desc = models.RandomNumber().fields()
    assert desc["id"]["optional"]
    assert desc["range_max"]["optional"]
