import argparse
import copy
import pprint
from collections import defaultdict, deque

INF = int(1e9)
SHIFTS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def get(pos, mx):
    i, j = pos
    if i < 0 or i >= len(mx):
        return "#"
    if j < 0 or j >= len(mx[i]):
        return "#"
    return mx[i][j]


def set_mx(pos, mx, s):
    mx[pos[0]][pos[1]] = s


def move(pos, shift):
    return (pos[0] + shift[0], pos[1] + shift[1])


def bfs(matrix, dist, start):
    q = deque()
    q.append((start))
    dist[start[0]][start[1]] = 0

    while q:
        pos = q.popleft()

        for shift in SHIFTS:
            new_pos = move(pos, shift)
            if get(new_pos, matrix) != "#" and dist[new_pos[0]][new_pos[1]] == INF:
                dist[new_pos[0]][new_pos[1]] = dist[pos[0]][pos[1]] + 1
                q.append(new_pos)


def solve(f):
    # Note: if you don't wnat to wait a couple of
    # seconds of the execution, please use pypy
    matrix = []

    start = None
    end = None

    for i, line in enumerate(f):
        if not line.strip():
            break

        matrix.append([])

        for j, s in enumerate(line.strip()):
            if s == "S":
                start = (i, j)
            elif s == "E":
                end = (i, j)

            matrix[i].append(s)

    n = len(matrix)
    m = len(matrix[0])

    cheats = []

    for i, l in enumerate(matrix):
        for j in range(len(l)):
            if i == 0 or i == n - 1:
                continue
            if j == 0 or j == m - 1:
                continue
            if matrix[i][j] != "#":
                cheats.append((i, j))

    # find distances from the start position
    # to all other positions
    to_start_dist = [[INF for _ in range(m)] for _ in range(n)]
    bfs(matrix, to_start_dist, start)

    # also find distances from the end position
    # to all other positions
    to_end_dist = [[INF for _ in range(m)] for _ in range(n)]
    bfs(matrix, to_end_dist, end)

    # sanity check the distances are consistent
    assert to_start_dist[end[0]][end[1]] == to_end_dist[start[0]][start[1]]

    # the distance between start and end with no cheats
    no_cheat_path = to_end_dist[start[0]][start[1]]

    def count_cheats(cheat_max_shift):
        # relative positions to which one can teleport
        # becuase of the cheat
        cheat_shift_mask = []
        for i in range(-cheat_max_shift, cheat_max_shift + 1):
            for j in range(-cheat_max_shift, cheat_max_shift + 1):
                dist = abs(i) + abs(j)
                if dist <= cheat_max_shift:
                    cheat_shift_mask.append((i, j, dist))

        nice_cheats_count = 0

        for cheat_from in cheats:
            for cx, cy, dist in cheat_shift_mask:
                cheat_pos = move(cheat_from, (cx, cy))

                # don't go to the wall
                if get(cheat_pos, matrix) == "#":
                    continue

                new_path = (
                    get(cheat_from, to_start_dist) + get(cheat_pos, to_end_dist) + dist
                )
                diff = no_cheat_path - new_path

                if no_cheat_path - new_path >= 100:
                    nice_cheats_count += 1

        return nice_cheats_count

    print("Answer 1", count_cheats(2))
    print("Answer 2", count_cheats(20))


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("input", type=str, default="input.txt")

    input_file = arg_parser.parse_args().input

    with open(input_file, "r") as f:
        solve(f)
