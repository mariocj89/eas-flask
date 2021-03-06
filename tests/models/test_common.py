from .. import factories

from eas import models


def test_create_with_defaults():
    rn = models.RandomNumber(**factories.SimpleNumber.dict())
    for f in ["id", "private_id", "created"]:
        assert getattr(rn, f) is not None


def test_create_with_fields():
    rn = models.RandomNumber(
        **factories.PublicNumber.dict(title="sample_title")
    )
    assert rn.title == "sample_title"


def test_id_is_unique_per_draw():
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


def test_result_limit():
    rn = factories.SimpleNumber.create(range_max=9999999)
    for _ in range(models.RandomNumber._RESULT_LIMIT):
        rn.toss()

    # Generating an extra toss doesnt increase the count
    first, *_, last = rn.results
    rn.toss()

    assert models.RandomNumber._RESULT_LIMIT == len(rn.results)
    assert last not in rn.results
    assert first == rn.results[1]

    # Neither in the one retrieved from db
    models.db.session.commit()
    retrieved_draw = models.RandomNumber.get_draw_or_404(rn.id)

    assert models.RandomNumber._RESULT_LIMIT == len(retrieved_draw.results)
    assert last not in rn.results
    assert first == rn.results[1]


def test_results_are_limited():
    limit = models.DrawBaseModel._RESULT_LIMIT
    rn = factories.SimpleNumber.create()
    for _ in range(limit * 2):
        rn.toss()

    assert limit == len(rn.results)

