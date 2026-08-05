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


def find_min_coins(coins: list[int], summ: int) -> dict[int, int]:
    """
    Python program to find minimum of coins.

    Complexity ~ O(C*S^2)

    C - len(coins)
    S - sum

    Args:
        coins (list[int]): coins to use
        summ (int): summ to optimize

    Returns:
        dict[int, int]: resulting coins distribution
    """

    # Initialize a list to store the minimum
    # number of coins for each amount
    dp = [[float("inf"), []] for _ in range(summ + 1)]

    # Base case: 0 coins are needed to make the sum of 0
    dp[0] = [0, []]

    # Iterate over each coin in reverse order O(C) -
    for i in range(len(coins) - 1, -1, -1):
        # Iterate through all amounts from 1 to sum O(S)
        for j in range(1, summ + 1):
            #  variable for the current coin
            take = [float("inf"), []]

            # variable for the current amount
            no_take = [float("inf"), []]

            # If we can take the current coin
            if j - coins[i] >= 0 and coins[i] > 0:
                # Get the minimum coins needed
                # for the remaining amount
                prev_count, prev_coins = dp[j - coins[i]]

                # Build a new candidate solution (do NOT mutate dp[...])
                if prev_count != float("inf"):
                    new_coins = prev_coins + [
                        coins[i]
                    ]  # O(S) - copying of coins array. Proportional to S
                    take = [len(new_coins), new_coins]

            # If there are coins left to consider
            if i + 1 < len(coins):
                # Get the minimum coins needed without
                # taking the current coin
                no_take = dp[j]

            # Store the minimum of taking or not
            # taking the current coin
            min_val = min(take, no_take, key=lambda item: item[0])
            dp[j] = [min_val[0], min_val[1][:]]  # max O(S)

    # Return the result for the given sum,
    # or -1 if it's not possible
    return Counter(dp[summ][1]) if dp[summ][0] != float("inf") else {}
