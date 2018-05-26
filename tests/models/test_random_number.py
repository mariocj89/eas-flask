from .. import factories

from eas import models


def test_generate_result():
    MIN = 500
    MAX = 9999999
    rn = factories.SimpleNumber.create(range_min=MIN, range_max=MAX)
    for _ in range(models.RandomNumber._RESULT_LIMIT):
        rn.toss()

    assert all(MIN <= res_item <= MAX
               for r in rn.results for res_item in r.value)

