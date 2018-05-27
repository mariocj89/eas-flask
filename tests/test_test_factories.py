from .factories import SimpleNumber, PublicNumber
from .factories import FacebookRaffle


def test_simple_number():
    n = SimpleNumber.dict()
    assert "range_min" in n
    assert "range_max" in n


def test_public_number():
    n = PublicNumber.dict()
    assert "range_min" in n
    assert "range_max" in n
    assert "title" in n
    assert "description" in n


def test_facebook_raffle():
    r = FacebookRaffle.dict(
        prices=(
            "one",
            "two"
        )
    )
    assert "prices" in r
    assert "facebook_object_id" in r
    assert len(r["prices"]) > 1
