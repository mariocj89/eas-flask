"""Tests against the API"""
from eas import urls


NUMBER_URL = urls.API_URL + "/random_number/"


def test_create_draw_check_basic_fields(api):
    create_result = api.post(NUMBER_URL, json=dict(title="Hello")).json
    get_result = api.get(NUMBER_URL + create_result["id"]).json

    for k, v in get_result.items():
        assert create_result[k] == v
    assert get_result["title"] == "Hello"


def test_private_link_is_returned_only_on_create(api):
    create_result = api.post(NUMBER_URL, json=dict(title="Hello")).json
    get_result = api.get(NUMBER_URL + create_result["id"]).json

    assert "private_id" in create_result
    assert "private_id" not in get_result


def test_private_link_can_be_used_on_get(api):
    create_result = api.post(NUMBER_URL, json=dict(title="Hello")).json
    get_result = api.get(NUMBER_URL + create_result["private_id"]).json

    assert get_result["id"] == create_result["id"]


def test_retrieve_invalid_item_gives_404(api):
    get_result = api.get(NUMBER_URL + "clear-fake-id")

    assert get_result.status_code == 404
