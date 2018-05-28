import pytest
from .. import factories

from eas.schemas import FacebookRaffle, ValidationError


def test_create_successfully():
    schema = FacebookRaffle(strict=True)

    res, err = schema.load(factories.FacebookRaffle.dict())

    assert not err
    assert res is not None
    assert hasattr(res, "facebook_token")


@pytest.mark.parametrize("values", [
    dict(prices=None, facebook_object_id="anything", facebook_token="fdjkgh3"),
    dict(prices=[], facebook_object_id="anything", facebook_token="fdjkgh3"),
    dict(prices=["a", "b"], facebook_object_id=None, facebook_token="123aa"),
    dict(prices=["a", "b"], facebook_object_id="hey", facebook_token=None),
])
def test_invalid_inputs(values):
    schema = FacebookRaffle(strict=True)

    with pytest.raises(ValidationError) as err:
        schema.load(factories.FacebookRaffle.dict(**values))

    assert any(k in str(err) for k in values)


def test_dumping_facebook_raffle(app):
    schema = FacebookRaffle()
    rn = factories.FacebookRaffle.create(prices=["a", "b"],
                                         facebook_object_id="object_id")
    expected = {
        'facebook_object_id': "object_id",
        'prices': ["a", "b"],
    }
    result, errors = schema.dump(rn)
    assert not errors
    for k, v in expected.items():
        assert v == result[k]

    rn.toss()
    result, errors = schema.dump(rn)
    assert not errors
    assert len(result["results"]) == 1
    assert result["results"][0]["value"] == [
        ("a", "Jorge"),
        ("b", "Jorge"),
    ]

