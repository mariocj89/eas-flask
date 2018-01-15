from .factories import SimpleNumber, PublicNumber


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
