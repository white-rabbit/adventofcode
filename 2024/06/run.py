import argparse

SHIFTS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def move(pos, shift_index):
    shift = SHIFTS[shift_index]
    return (pos[0] + shift[0], pos[1] + shift[1])


def set_val(pos, mx, value='X'):
    i, j = pos
    mx[i][j] = value


def get(pos, mx):
    i, j = pos

    if i < 0 or i >= len(mx):
        return 'x'

    if j < 0 or j >= len(mx[i]):
        return 'x'

    return mx[i][j]


def is_loop(matrix, pos, shift, visited):
    cell = None

    while cell != 'x':
        next_pos = move(pos, shift)
        next_cell = get(next_pos, matrix)

        if next_cell == '#':
            shift = (shift + 1) % 4
            continue

        cell = next_cell
        pos = next_pos

        if (pos, shift) in visited:
            return True

        visited.add((pos, shift))

    return False


def solve(f):
    start_position = None
    matrix = []

    for i, line in enumerate(f):
        row = []
        for j, c in enumerate(line):
            if c == '^':
                start_position = (i, j)
            row.append(c)
        matrix.append(row)

    assert start_position is not None

    shift_index = 0
    position = start_position

    prev_pos, prev_shift = None, None

    # Compute visited cells count and obstacle candidates
    # (there is no sense to add obstacle out of the initial path)
    visited_cells = 0
    obstacle_candidate = []

    while get(position, matrix) != 'x':
        if get(position, matrix) != 'X':
            if prev_pos is not None:
                obstacle_candidate.append(
                    ((prev_pos, prev_shift), position))
            set_val(position, matrix, value='X')
            visited_cells += 1

        prev_pos, prev_shift = position, shift_index

        while get(move(position, shift_index), matrix) == '#':
            shift_index = (shift_index + 1) % 4

        position = move(position, shift_index)

    # Compute number of obstacles that creates loops
    succeed_obstacles = 0

    for (start, shift), obstacle in obstacle_candidate:
        set_val(obstacle, matrix, value='#')
        if is_loop(matrix, start, shift, set()):
            succeed_obstacles += 1
        set_val(obstacle, matrix, value='.')

    print("Answer 1: ", visited_cells)
    print("Answer 2: ", succeed_obstacles)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input', type=str, default='input.txt')

    input_file = arg_parser.parse_args().input

    with open(input_file, 'r') as f:
        solve(f)
