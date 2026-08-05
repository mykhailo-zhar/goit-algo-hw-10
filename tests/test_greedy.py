import pytest

from src.greedy import find_coins_greedy, find_min_coins


@pytest.fixture
def coins():
    return [50, 25, 10, 5, 2, 1]


def test_coins_greedy(coins):
    assert find_coins_greedy(coins, 113) == {50: 2, 10: 1, 2: 1, 1: 1}


def test_min_coins(coins):
    assert find_min_coins(coins, 113) == {50: 2, 10: 1, 2: 1, 1: 1}
