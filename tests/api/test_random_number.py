"""Tests against the API"""
from os.path import join
import pytest

from .. import factories
from eas import urls


NUMBER_URL = join(urls.API_URL, "random_number")


@pytest.mark.parametrize("values", [
    dict(range_min=-1),
    dict(range_max=-1),
    dict(range_min=15, range_max=10),
])
def test_create_invalid_number_returns_400(api, values):
    number = factories.PublicNumber.dict()
    number.update(values)
    result = api.post(NUMBER_URL, json=number)

    assert result.status_code == 400
    assert any(k in values for k in result.json)


def test_create_valid_result(api):
    number = factories.PublicNumber.dict(range_min=5, range_max=6)
    create_result = api.post(NUMBER_URL, json=number).json
    put_result = api.put(join(NUMBER_URL, create_result["private_id"])).json

    assert 1 == len(put_result["results"])
    assert put_result["results"][0]["value"][0] in range(5, 7)
