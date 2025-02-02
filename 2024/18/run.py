import argparse
from collections import defaultdict, deque

INF = int(1e9)
SHIFTS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def is_corrupted(matrix, pos, time):
    i, j = pos

    if i < 0 or i >= len(matrix):
        return True

    if j < 0 or j >= len(matrix[i]):
        return True

    if time >= matrix[i][j]:
        return True

    return False


def move(pos, shift):
    return (pos[0] + shift[0], pos[1] + shift[1])


def make_matrix(size):
    matrix = []

    for i in range(size):
        # the moment of time when the cell is corrupted
        matrix.append([INF for _ in range(size)])

    return matrix


def shortest_path(matrix, matrix_state_time):
    q = deque()

    size = len(matrix)

    best_time = INF

    visited = set()
    q.append((0, 0, 0))

    while q:
        i, j, time = q.popleft()
        pos = i, j

        if i == size - 1 and j == size - 1:
            best_time = time

        for shift in SHIFTS:
            next_i = i + shift[0]
            next_j = j + shift[1]
            next_pos = next_i, next_j

            if next_pos not in visited and not is_corrupted(
                matrix, next_pos, matrix_state_time
            ):
                visited.add(next_pos)
                q.append((next_i, next_j, time + 1))

    return best_time


def find_block_path_time(matrix, min_time, max_time):
    a = min_time
    b = max_time

    # lower bound is the time when the path disappears
    while a < b:
        c = (a + b) // 2

        if shortest_path(matrix, c) != INF:
            # we are trying to find the first
            # pos where the path is inf, hence + 1
            a = c + 1
        else:
            # we want the second bound to always be
            # in the inf zone, hence, do not add -1
            b = c

    return a


def solve(f):
    raw_data = [line for line in f]
    large_matrix = len(raw_data) > 30
    matrix_size = 71 if large_matrix else 7
    initial_nanoseconds = 1024 if large_matrix else 12

    matrix = make_matrix(matrix_size)

    # update matrix with corrupted cell timings
    time_to_obstacle = {}
    for time_to_corrupt, line in enumerate(raw_data):
        pos = tuple(int(x) for x in line.strip().split(","))
        x, y = pos
        assert matrix[x][y] == INF
        matrix[x][y] = time_to_corrupt
        time_to_obstacle[time_to_corrupt] = pos

    print("Answer 1: ", shortest_path(matrix, initial_nanoseconds))

    # we can start from the initial time as
    # it is known the path exists in this case
    min_time = initial_nanoseconds
    max_time = len(raw_data)

    block_time = find_block_path_time(matrix, min_time, max_time)
    block_x, block_y = time_to_obstacle[block_time]

    print("Answer 2: ", f"{block_x},{block_y}")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--input", type=str, default="input.txt")

    input_file = arg_parser.parse_args().input

    with open(input_file, "r") as f:
        solve(f)
