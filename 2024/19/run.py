import argparse
from collections import defaultdict, deque


class Node:
    def __init__(self):
        self.terminal_count = 0
        self.children = {}

    @property
    def is_terminal(self):
        return self.terminal_count > 0


def can_build(start_node, word):
    generation = {start_node}

    count = 1

    for s in word:
        if not generation:
            return False

        next_generation = set()

        for node in generation:
            if node.is_terminal:
                if s in start_node.children:
                    next_node = start_node.children[s]
                    next_generation.add(next_node)

            if s in node.children:
                next_generation.add(
                        node.children[s])

        generation = next_generation

    return any(node.is_terminal for node in generation)


def calc_path_count(start_node, node, word, symbol_index, cache):
    if (symbol_index, node) in cache:
        return cache[symbol_index, node]

    if symbol_index == len(word):
        if node.is_terminal:
            return node.terminal_count
        return 0

    s = word[symbol_index]

    total_count = 0

    if node.is_terminal and s in start_node.children:
        total_count += (
            calc_path_count(
                start_node, start_node.children[s],
                word, symbol_index + 1, cache)
            * node.terminal_count
        )

    if s in node.children:
        total_count += calc_path_count(
                start_node, node.children[s],
                word, symbol_index + 1, cache)

    cache[(symbol_index, node)] = total_count

    return total_count


def solve(f):
    lines = list(f)

    samples = [w.strip() for w in lines[0].split(",")]

    start = Node()

    # make tree
    for sample in samples:
        cur = start

        for s in sample:
            if s not in cur.children:
                next = Node()
                cur.children[s] = next
                cur = next
            else:
                cur = cur.children[s]

        cur.terminal_count += 1

    count = 0
    path_count = 0

    for word in lines[2:]:
        word = word.strip()
        if can_build(start, word):
            cache = {}
            path_count += calc_path_count(
                    start, start, word, 0, cache)
            count += 1

    print("Answer 1:", count)
    print("Answer 2:", path_count)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--input", type=str, default="input.txt")

    input_file = arg_parser.parse_args().input

    with open(input_file, "r") as f:
        solve(f)
