from .. import factories


def test_single_price_raffle():
    raffle = factories.FacebookRaffle.create(prices=(
        "Super price!",
    ))

    raffle.toss()

    assert len(raffle.results) == 1
    assert len(raffle.results[0].value) == 1
    price, winner = raffle.results[0].value[0]
    assert price == raffle.prices[0]


def test_multiple_price_raffle():
    NUMBER_PRICES = 10
    prices = ["Price"] * NUMBER_PRICES
    raffle = factories.FacebookRaffle.create(prices=prices)

    raffle.toss()

    assert len(raffle.results) == 1
    assert len(raffle.results[0].value) == NUMBER_PRICES

    # Check all prices are present
    results_prices = [r[0] for r in raffle.results[0].value]
    assert all(price in results_prices for price in raffle.prices)


def test_draw_with_repeated_prices():
    prices = ["Sample price"] * 2
    raffle = factories.FacebookRaffle.create(prices=prices)

    raffle.toss()

    assert len(raffle.results[0].value) == 2


def test_add_price():
    NUMBER_PRICES = 10
    raffle = factories.FacebookRaffle.create(prices=[])
    for i in range(NUMBER_PRICES):
        raffle.add_price(f"Price {i}")

    raffle.toss()

    assert len(raffle.results) == 1
    assert len(raffle.results[0].value) == NUMBER_PRICES


def test_build_with_prices_in_init():
    NUMBER_PRICES = 50
    raffle = factories.FacebookRaffle.create(prices=(
        f"price {i}" for i in range(NUMBER_PRICES)
    ))

    raffle.toss()

    assert len(raffle.results) == 1
    assert len(raffle.results[0].value) == NUMBER_PRICES
