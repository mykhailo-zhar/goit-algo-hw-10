import heapq
import timeit
from collections import Counter


def find_coins_greedy(coins: list[int], sum: int) -> dict[int, int]:
    """
    Python program to find minimum of coins using greedy algorithm.

    Complexity ~ O(C log C)

    Args:
        coins (list[int]): coins to use
        summ (int): summ to optimize

    Returns:
        dict[int, int]: resulting coins distribution
    """
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
    """
    Recursively find the minimum number of coins for a given sum.

    Explores take / not-take choices for coins[coin_index] without memoization.

    Complexity ~ O(2^(S/min(C))) in the worst case

    C - len(coins)
    S - sum

    Args:
        coins (list[int]): available coin denominations
        sum (int): remaining amount to make
        coin_index (int): index of the coin currently considered

    Returns:
        list: [coin_count, list_of_chosen_coins]; coin_count is inf if impossible
    """
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
    """
    Recursively find the minimum number of coins with top-down memoization.

    Same take / not-take recursion as `_min_coins_recursive`, but caches
    results for each (coin_index, sum) pair.

    Complexity ~ O(C * S)

    C - len(coins)
    S - sum

    Args:
        coins (list[int]): available coin denominations
        sum (int): remaining amount to make
        coin_index (int): index of the coin currently considered
        memo (list[list]): cache of [coin_count, coins_list] or -1 if unset

    Returns:
        list: [coin_count, list_of_chosen_coins]; coin_count is inf if impossible
    """
    if sum == 0:
        return [0, []]

    if sum < 0 or coin_index == len(coins):
        return [float("inf"), []]

    if memo[coin_index][sum] != -1:
        # Return a copy to avoid mutating the cached coin list downstream.
        return memo[coin_index][sum]

    take = _min_coins_recursive_memo(coins, sum - coins[coin_index], coin_index, memo)
    no_take = _min_coins_recursive_memo(coins, sum, coin_index + 1, memo)
    if take[0] != float("inf"):
        take[1].append(coins[coin_index])
        take[0] = len(take[1])

    min_value = min(take, no_take, key=lambda item: item[0])
    memo[coin_index][sum] = [min_value[0], min_value[1][:]]
    return memo[coin_index][sum]


def find_min_coins_recursive(coins: list[int], sum: int) -> dict[int, int]:
    """
    Find the minimum number of coins using memoized recursion.

    Complexity ~ O(C * S)

    C - len(coins)
    S - sum

    Args:
        coins (list[int]): coins to use
        sum (int): sum to optimize

    Returns:
        dict[int, int]: resulting coins distribution
    """
    # result = Counter(_min_coins_recursive(coins, sum, 0)[1])
    memo = [[-1] * (sum + 1) for _ in range(len(coins))]
    result = _min_coins_recursive_memo(coins, sum, 0, memo)
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


def benchmark(
    coins: list[int] | None = None, amount: int = 113, number: int = 1000
) -> None:
    """Run timeit benchmarks for greedy and DP coin-change functions."""
    if coins is None:
        coins = [50, 25, 10, 5, 2, 1]

    benchmarks = [
        ("find_coins_greedy", lambda: find_coins_greedy(coins, amount)),
        ("find_min_coins_recursive", lambda: find_min_coins_recursive(coins, amount)),
        ("find_min_coins", lambda: find_min_coins(coins, amount)),
    ]

    print(f"Benchmark (coins={coins}, amount={amount}, number={number})")
    print("-" * 60)
    for name, fn in benchmarks:
        elapsed = timeit.timeit(fn, number=number)
        print(f"{name:28} {elapsed:.6f}s  ({elapsed / number * 1e6:.2f} µs/call)")


if __name__ == "__main__":
    benchmark()
