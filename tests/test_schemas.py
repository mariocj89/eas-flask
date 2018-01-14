import pytest
from . import factories

from eas.schemas import RandomNumber, ValidationError


def test_create_random_number_successfully():
    schema = RandomNumber(strict=True)

    res, err = schema.load(factories.SimpleNumber.dict())

    assert not err
    assert res is not None


@pytest.mark.parametrize("values", [
    dict(range_min=-1),
    dict(range_max=-1),
    dict(range_min=15, range_max=10),
])
def test_validate_ranges(values):
    schema = RandomNumber(strict=True)

    with pytest.raises(ValidationError) as err:
        schema.load(factories.SimpleNumber.dict(**values))

    assert any(k in str(err) for k in values)

