"""Tests against the API"""
from eas import urls


NUMBER_URL = urls.API_URL + "/random_number/"


def test_create_draw_check_basic_fields(api):
    create_result = api.post(NUMBER_URL, json=dict(title="Hello")).json
    get_result = api.get(NUMBER_URL + create_result["id"]).json

    assert create_result == get_result
    assert get_result["title"] == "Hello"
