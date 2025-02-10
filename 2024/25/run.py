from collections import defaultdict


def to_heights(matrix):
    heights = []
    for j in range(len(matrix[0])):
        height = 0
        for i in range(len(matrix)):
            if matrix[i][j] == "#":
                height += 1
        heights.append(height)
    return heights


def is_lock(matrix):
    for j in matrix[0]:
        if j == "#":
            return True
    return False


def fit(key, lock, height):
    for k, l in zip(key, lock):
        if k + l > height:
            return False
    return True


def solve(f):
    locks = []
    keys = []
    n, m = None, None

    cur_matrix = []

    for l in f:
        if not l.strip():
            n = len(cur_matrix)
            m = len(cur_matrix[0])
            if is_lock(cur_matrix):
                locks.append(to_heights(cur_matrix))
            else:
                keys.append(to_heights(cur_matrix))

            cur_matrix = []
            continue
        cur_matrix.append(l.strip())

    if is_lock(cur_matrix):
        locks.append(to_heights(cur_matrix))
    else:
        keys.append(to_heights(cur_matrix))

    num_fit = 0

    for k in keys:
        for l in locks:
            if fit(k, l, n):
                num_fit += 1

    print("Answer", num_fit)


if __name__ == "__main__":
    input_file = "input.txt"

    with open(input_file, "r") as f:
        solve(f)
