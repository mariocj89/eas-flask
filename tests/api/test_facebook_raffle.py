"""Tests against the API"""
from os.path import join
import pytest

from .. import factories
from eas import urls


NUMBER_URL = join(urls.API_URL, "facebook_raffle")


@pytest.mark.parametrize("values", [
    dict(facebook_object_id=None, prices=["a", "b"]),
])
def test_create_invalid_number_returns_400(api, values):
    number = factories.FacebookRaffle.dict()
    number.update(values)
    result = api.post(NUMBER_URL, json=number)

    assert result.status_code == 400
    assert any(k in values for k in result.json)


def test_create_valid_result(api):
    number = factories.FacebookRaffle.dict()
    create_result = api.post(NUMBER_URL, json=number).json
    assert "private_id" in create_result
