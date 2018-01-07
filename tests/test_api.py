"""Tests against the API"""
import json

import pytest

from eas import urls


NUMBER_URL = urls.API_URL + "/random_number/"


def test_create_draw_check_basic_fields(api):
    result = api.post(NUMBER_URL, json=dict(title="Hello")).json
    res = api.get(NUMBER_URL + result["id"]).json

    assert result == res
    assert result["title"] == "Hello"
