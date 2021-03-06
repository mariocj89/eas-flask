"""Tests against the API"""
from os.path import join
import pytest

from .. import factories
from eas import urls


NUMBER_URL = join(urls.API_URL, "random_number")


def test_get_swagger_yaml(api):
    content = api.get(join(urls.API_URL, "swagger.yaml")).data
    assert b"random_number" in content


def test_health_check(api):
    content = api.get(join(urls.API_URL, "ping")).data
    assert b"pong" in content


def test_create_draw_check_basic_fields(api):
    rn = factories.PublicNumber.dict()
    create_result = api.post(NUMBER_URL, json=rn).json
    get_result = api.get(join(NUMBER_URL, create_result["id"])).json

    for k, v in get_result.items():
        assert create_result[k] == v
    assert get_result["title"] == rn["title"]


def test_private_link_is_returned_only_on_create(api):
    rn = factories.SimpleNumber.dict()
    create_result = api.post(NUMBER_URL, json=rn).json
    get_result = api.get(join(NUMBER_URL, create_result["id"])).json

    assert "private_id" in create_result
    assert "private_id" not in get_result


def test_private_link_can_be_used_on_retrieve(api):
    rn = factories.PublicNumber.dict()
    create_result = api.post(NUMBER_URL, json=rn).json
    get_result = api.get(join(NUMBER_URL, create_result["private_id"])).json

    assert get_result["id"] == create_result["id"]


def test_retrieve_invalid_item_gives_404(api):
    get_result = api.get(join(NUMBER_URL, "clear-fake-id"))

    assert get_result.status_code == 404


def test_toss_draw_with_public_id_not_found(api):
    number = factories.PublicNumber.dict(range_min=5, range_max=6)
    create_result = api.post(NUMBER_URL, json=number).json
    put_result = api.put(join(NUMBER_URL, create_result["id"]))
    assert put_result.status_code == 404


def test_toss_draw_creates_result(api):
    number = factories.PublicNumber.dict(range_min=5, range_max=6)
    create_result = api.post(NUMBER_URL, json=number).json
    put_result = api.put(join(NUMBER_URL, create_result["private_id"])).json

    assert 1 == len(put_result["results"])
    assert put_result["results"][0]["value"][0] in range(5, 7)


def test_multiple_toss(api):
    number = factories.PublicNumber.dict(range_min=0, range_max=5000000000)
    create_result = api.post(NUMBER_URL, json=number).json
    put_result1 = api.put(join(NUMBER_URL, create_result["private_id"])).json
    put_result2 = api.put(join(NUMBER_URL, create_result["private_id"])).json
    get_result = api.get(join(NUMBER_URL, create_result["private_id"])).json

    # Two results were generated
    assert 2 == len(get_result["results"])

    # Retrieve matches toss
    assert get_result == put_result2

    # Check order, first result should be second on retrieve
    assert get_result["results"][1] == put_result1["results"][0]
