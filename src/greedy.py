import heapq
from collections import Counter


def find_coins_greedy(coins: list[int], sum: int) -> dict[int, int]:
    result = {}
    heap = [-el for el in coins]  # O(N) - ітерація по масиву
    heapq.heapify(heap)  # O(logN)

    # Почати Із монети найбільшого номіналу
    while heap:  # O(NlogN)
        coin = -heapq.heappop(heap)
        # Якщо можливо відняти від суми монету номіналу
        # Записати результат у якості цілочисленого ділення на монету номіналу
        # В сумі залишити залишок ділення на номінал
        if sum // coin <= 0:
            continue

        result[coin] = sum // coin
        sum %= coin

    return result


def _min_coins_recursive(coins: list[int], sum: int, coin_index):
    if sum == 0:
        return [0, []]

    if sum < 0 or coin_index == len(coins):
        return [float("inf"), []]

    take = _min_coins_recursive(coins, sum - coins[coin_index], coin_index)
    not_take = _min_coins_recursive(coins, sum, coin_index + 1) or []
    if take[0] != float("inf"):
        take[1].append(coins[coin_index])
        take[0] = len(take[1])

    return min(take, not_take, key=lambda item: item[0])


def _min_coins_recursive_memo(coins: list[int], sum: int, coin_index: int, memo: dict):
    if sum == 0:
        return [0, []]

    if sum < 0 or coin_index == len(coins):
        return [float("inf"), []]

    if memo[coin_index][sum] != -1:
        return memo[coin_index][sum]

    take = _min_coins_recursive_memo(coins, sum - coins[coin_index], coin_index, memo)
    no_take = _min_coins_recursive_memo(coins, sum, coin_index + 1, memo)
    if take[0] != float("inf"):
        take[1].append(coins[coin_index])
        take[0] = len(take[1])

    min_value = min(take, no_take, key=lambda item: item[0])
    memo[coin_index][sum] = [min_value[0], min_value[1][:]]
    return memo[coin_index][sum]


def find_min_coins(coins: list[int], sum: int) -> dict[int, int]:

    # result = Counter(_min_coins_recursive(coins, sum, 0)[1])
    memo = [[-1] * (sum + 1) for _ in range(len(coins))]
    result = _min_coins_recursive_memo(coins, sum, 0, memo)
    print(result[0])
    result = Counter(result[1])

    return dict(result)
