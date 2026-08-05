import pytest

from src.greedy import find_coins_greedy, find_min_coins


@pytest.fixture
def coins():
    return [50, 25, 10, 5, 2, 1]


@pytest.fixture(
    params=[
        [50, 25, 10, 5, 2, 1],
        [1, 2, 5, 10, 25, 50],
        [1, 5, 10, 25, 50, 2],
        [1, 2, 5, 10, 25, 50],
        [1, 2, 5, 10, 25, 50],
    ]
)
def coins_shuffle(request):
    return request.param


@pytest.fixture
def result():
    return {50: 2, 10: 1, 2: 1, 1: 1}


def test_coins_greedy(coins, result):
    assert find_coins_greedy(coins, 113) == result


def test_coins_greedy_shuffle(coins_shuffle, result):
    assert find_coins_greedy(coins_shuffle, 113) == result


def test_min_coins(coins, result):
    assert find_min_coins(coins, 113) == result


def test_min_coins_shuffles(coins_shuffle, result):
    assert find_min_coins(coins_shuffle, 113) == result
