# Created on iPad
from functools import cache

SHIFTS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

KEY_SHIFTS = ['>', '<', 'v', '^']

NUMERIC_KEYPAD = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    ['.', '0', 'A']
]

DIRECTIONAL_KEYPAD = [
    ['.', '^', 'A'],
    ['<', 'v', '>']
]

NUMERIC = 0
DIRECTIONAL = 1

KEYPADS = {
    NUMERIC: NUMERIC_KEYPAD,
    DIRECTIONAL: DIRECTIONAL_KEYPAD
}


def get(pos, mx):
    i, j = pos
    if i < 0 or i >= len(mx):
        return "."
    if j < 0 or j >= len(mx[i]):
        return "."
    return mx[i][j]


def move(pos, shift):
    return (pos[0] + shift[0], pos[1] + shift[1])


@cache
def get_position_map(keypad_index):
    map = {}
    keypad = KEYPADS[keypad_index]
    for i, l in enumerate(keypad):
        for j, s in enumerate(l):
            map[s] = (i, j)

    return map


def dfs(pos, end, matrix, path, visited, all_paths):
    if pos == end:
        all_paths.append(path + ["A"])
        return

    for shift, key in zip(SHIFTS, KEY_SHIFTS):
        next_pos = move(pos, shift)
        next_symbol = get(next_pos, matrix)

        if next_symbol != "." and next_pos not in visited:
            visited.add(next_pos)
            dfs(next_pos, end, matrix, path + [key], visited, all_paths)
            visited.remove(next_pos)


@cache
def get_shortests_paths(keypad_index, start, end):
    keypad = KEYPADS[keypad_index]
    position_map = get_position_map(keypad_index)

    start_position = position_map[start]
    end_position = position_map[end]

    # brute force all path from start key to the end key
    all_paths = []
    dfs(start_position, end_position, keypad, [], {start_position}, all_paths)

    all_paths = sorted(all_paths, key=lambda x: len(x))

    if len(all_paths) == 0:
        return all_paths

    # filter out all paths except of the shortests
    shortest_len = len(all_paths[0])
    shortest_paths = list(filter(lambda x: len(x) == shortest_len, all_paths))

    return shortest_paths


# type a code on the numeric keypad
# the result is the sequence on the directional keypad
def type_code(code, index, path, all_paths):
    if index == len(code):
        all_paths.append(path)
        return

    prev_symbol = code[index - 1] if index > 0 else "A"
    symbol = code[index]

    possible_paths = get_shortests_paths(NUMERIC, prev_symbol, symbol)

    for next_path in possible_paths:
        type_code(code, index + 1, path + next_path, all_paths)


@cache
def move_cost(fst, scd, robots_count):
    # all shortest paths from one key to the other
    # on the numeric keypad
    all_paths = get_shortests_paths(DIRECTIONAL, fst, scd)

    # the last robot is controlled directly
    # so the path doesnt matter
    if robots_count == 1:
        return len(all_paths[0])

    shortest = None

    # traverse all the shortest paths for the intermediate
    # robot, the cost of each transition from one key to the
    # other is computed accounting the remaining robots
    for path in all_paths:
        cur = 0
        for i, s in enumerate(path):
            prev_s = path[i - 1] if i > 0 else "A"
            cur += move_cost(prev_s, s, robots_count - 1)

        shortest = cur if shortest is None else min(shortest, cur)

    return shortest


def code_best_cost(code, robots=2):
    first_paths = []

    # all shortest paths on the numeric pad
    type_code(code, 0, [], first_paths)

    shortest = None

    for fp in first_paths:
        # compute the cost of all transitions from one symbol
        # to the next one on the numeric pad by the
        # chain of robots that use the directional pad
        cur = 0
        for i, cur_s in enumerate(fp):
            prev_s = fp[i - 1] if i > 0 else "A"
            cur += move_cost(prev_s, cur_s, robots)

        if shortest is None or cur < shortest:
            shortest = cur

    code_num = int(code[:-1])

    return shortest * code_num


def solve(f):
    lines = list(f)
    result = 0
    for code in lines:
        result += code_best_cost(code.strip())

    print("Result 1", result)

    result = 0
    for code in lines:
        result += code_best_cost(code.strip(), robots=25)

    print("Result 2", result)


if __name__ == "__main__":
    input_file = "input.txt"

    with open(input_file, "r") as f:
        solve(f)
