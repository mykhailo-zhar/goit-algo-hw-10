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


def _min_coins(coins: list[int], sum: int, coin_index):
    if sum == 0:
        return [0, []]

    if sum < 0 or coin_index == len(coins):
        return [float("inf"), []]

    take = _min_coins(coins, sum - coins[coin_index], coin_index)
    not_take = _min_coins(coins, sum, coin_index + 1) or []
    if take[0] != float("inf"):
        take[0] += 1
        take[1].append(coins[coin_index])

    return min(take, not_take, key=lambda item: item[0])


def find_min_coins(coins: list[int], sum: int) -> dict[int, int]:
    # Задача полягає у знайденні мінімальної суми монет різного номіналу
    # для видачі певної суми

    # Мінімізація кількості монет - пошук максимальної кількості монет номіналу, що задовольнить суму
    # Беремо монету
    # Якщо можемо відняти - віднімаємо
    # Не можем - берем наступну

    result = Counter(_min_coins(coins, sum, 0)[1])

    return dict(result)
