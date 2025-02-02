# Created on iPad

import argparse
import copy
import pprint
from collections import defaultdict, deque

MOD = 16777216


def calc_secret_number(n):
    n = n ^ (n << 6) % MOD
    n = n ^ (n >> 5) % MOD
    n = n ^ (n << 11) % MOD
    return n


def calc_price(number, bananas_for_condition):
    price_diffs = deque()
    price_changes = deque()
    price_changes.append(number % 10)

    used = set()

    for step in range(2000):
        number = calc_secret_number(number)

        price = number % 10
        price_changes.append(price)

        if len(price_changes) > 1:
            price_diff = 10 + price_changes[-1] - price_changes[-2]
            price_diffs.append(price_diff)

        if len(price_diffs) > 3:
            condition_index = price_diffs[0] * 8000 + price_diffs[1] * 400 + price_diffs[2] * 20 + price_diffs[3]

            if condition_index not in used:
                bananas_for_condition[condition_index] += price
                used.add(condition_index)

            price_changes.popleft()
            price_diffs.popleft()

    return number


def solve(f):
    total_secret_number = 0
    bananas_for_condition = [0 for _ in range(500000)]

    for n in list(f):
        secret_number = calc_price(int(n), bananas_for_condition)
        total_secret_number += secret_number

    print("Result 1:", total_secret_number)
    print("Result 2:", max(bananas_for_condition))


if __name__ == "__main__":
    input_file = "input.txt"

    with open(input_file, "r") as f:
        solve(f)
