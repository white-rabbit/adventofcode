import argparse


def get(mx, pos):
    i, j = pos
    if i < 0 or i >= len(mx):
        return 100
    if j < 0 or j >= len(mx[i]):
        return 100
    return mx[i][j]


def next_pos(pos, shift):
    return (pos[0] + shift[0], pos[1] + shift[1])


def dfs(matrix, paths, position):
    if get(paths, position) is not None:
        return get(paths, position)

    cur = get(matrix, position)

    count = 0
    reachable = set()

    for shift in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
        next_position = next_pos(position, shift)
        if cur + 1 == get(matrix, next_position):
            dcount, dreachable = dfs(matrix, paths, next_position)
            count += dcount
            reachable |= dreachable

    if cur == 9:
        assert count == 0
        reachable.add(position)
        count = 1

    paths[position[0]][position[1]] = count, reachable

    return count, reachable


def solve(f):
    matrix = []
    paths = []

    for line in f:
        matrix.append([int(x) for x in line.strip()])
        paths.append([None for _ in line.strip()])

    non_unique_paths = 0
    unique_paths = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                score, reachable = dfs(matrix, paths, (i, j))
                unique_paths += score
                non_unique_paths += len(reachable)

    print("Answer 1: ", non_unique_paths)
    print("Answer 2: ", unique_paths)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input', type=str, default='input.txt')

    input_file = arg_parser.parse_args().input

    with open(input_file, 'r') as f:
        solve(f)
