"""Tests against the API"""
import pytest

from . import factories
from eas import urls


NUMBER_URL = urls.API_URL + "/random_number/"


def test_create_draw_check_basic_fields(api):
    rn = factories.PublicNumber.dict()
    create_result = api.post(NUMBER_URL, json=rn).json
    get_result = api.get(NUMBER_URL + create_result["id"]).json

    for k, v in get_result.items():
        assert create_result[k] == v
    assert get_result["title"] == rn["title"]


def test_private_link_is_returned_only_on_create(api):
    rn = factories.SimpleNumber.dict()
    create_result = api.post(NUMBER_URL, json=rn).json
    get_result = api.get(NUMBER_URL + create_result["id"]).json

    assert "private_id" in create_result
    assert "private_id" not in get_result


def test_private_link_can_be_used_on_get(api):
    rn = factories.PublicNumber.dict()
    create_result = api.post(NUMBER_URL, json=rn).json
    get_result = api.get(NUMBER_URL + create_result["private_id"]).json

    assert get_result["id"] == create_result["id"]


def test_retrieve_invalid_item_gives_404(api):
    get_result = api.get(NUMBER_URL + "clear-fake-id")

    assert get_result.status_code == 404


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


def test_create_draw_creates_result(api):
    number = factories.PublicNumber.dict(range_min=5, range_max=6)
    create_result = api.post(NUMBER_URL, json=number).json

    assert 1 == len(create_result["results"])
    assert create_result["results"][0]["value"][0] in range(5, 7)

