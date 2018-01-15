import pytest
from . import factories

from eas.schemas import RandomNumber, ValidationError


def test_create_random_number_successfully():
    schema = RandomNumber(strict=True)

    res, err = schema.load(factories.SimpleNumber.dict())

    assert not err
    assert res is not None


@pytest.mark.parametrize("values", [
    dict(range_min=None),
    dict(range_max=None),
    dict(range_min=-1),
    dict(range_max=-1),
    dict(range_min=15, range_max=10),
])
def test_validate_ranges(values):
    schema = RandomNumber(strict=True)

    with pytest.raises(ValidationError) as err:
        schema.load(factories.SimpleNumber.dict(**values))

    assert any(k in str(err) for k in values)


def test_dumping_random_number(app):
    schema = RandomNumber()
    rn = factories.SimpleNumber.create(range_min=5, range_max=5)
    expected = {
        'range_max': 5,
        'range_min': 5,
    }
    result, errors = schema.dump(rn)
    assert not errors
    for k, v in expected.items():
        assert v == result[k]

    rn.toss()
    result, errors = schema.dump(rn)
    assert not errors
    assert len(result["results"]) == 1
    assert result["results"][0]["value"] == [5]

