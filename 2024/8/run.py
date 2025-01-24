import argparse
import collections


def solve(f):
    matrix = []

    antennas = collections.defaultdict(list)

    for i, line in enumerate(f):
        for j, x in enumerate(line.strip()):
            if x != '.':
                antennas[x].append((i, j))
        matrix.append([x for x in line.strip()])

    def valid(pos, mx):
        i, j = pos
        if i < 0 or i >= len(mx):
            return False
        if j < 0 or j >= len(mx[i]):
            return False
        return True


    def get(pos, mx):
        if valid(pos, mx):
            return mx[i][j]

    first_order_antinodes = set()
    antinodes = set()

    for antenna, coordinates in antennas.items():
        n = len(coordinates)
        for i in range(n):
            for j in range(i + 1, n):
                ai = coordinates[i]
                aj = coordinates[j]

                dx = aj[0] - ai[0]
                dy = aj[1] - ai[1]

                def next(pos, dx, dy):
                    return (pos[0] + dx, pos[1] + dy)

                ai_candidate = next(aj, dx, dy)
                if valid(ai_candidate, matrix):
                    first_order_antinodes.add(ai_candidate)

                aj_candidate = next(ai, -dx, -dy)
                if valid(aj_candidate, matrix):
                    first_order_antinodes.add(aj_candidate)

                cur = aj
                while valid(cur, matrix):
                    antinodes.add(cur)
                    cur = next(cur, dx, dy)

                cur = ai
                while valid(cur, matrix):
                    antinodes.add(cur)
                    cur = next(cur, -dx, -dy)

    print("Answer 1: ", len(first_order_antinodes))
    print("Answer 2: ", len(antinodes))


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input', type=str, default='input.txt')

    input_file = arg_parser.parse_args().input

    with open(input_file, 'r') as f:
        solve(f)
