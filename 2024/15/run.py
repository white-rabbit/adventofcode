import argparse
from collections import defaultdict


SHIFTS = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0)
}


def get(pos, mx):
    i, j = pos
    if i < 0 or i >= len(mx):
        return None
    if j < 0 or j >= len(mx[i]):
        return None
    return mx[i][j]


def set_mx(pos, mx, s):
    mx[pos[0]][pos[1]] = s


def next_pos(pos, shift):
    return (pos[0] + shift[0], pos[1] + shift[1])


def check_can_move(pos, matrix, visited, shift):
    moved_pos = next_pos(pos, shift)

    if moved_pos in visited:
        return True

    next_cell = get(moved_pos, matrix)

    if next_cell == ']' and (moved_pos[0], moved_pos[1] - 1) in visited:
        return True

    if next_cell == '#':
        return False

    can_move = True

    if next_cell == '[':
        can_move = check_can_move(moved_pos, matrix, visited, shift)
        if can_move:
            adjacent_pos = moved_pos[0], moved_pos[1] + 1
            can_move &= check_can_move(adjacent_pos, matrix, visited, shift)
        if can_move:
            visited.add(moved_pos)

    if next_cell == ']':
        can_move = check_can_move(moved_pos, matrix, visited, shift)
        if can_move:
            adjacent_pos = moved_pos[0], moved_pos[1] - 1
            can_move &= check_can_move(adjacent_pos, matrix, visited, shift)
        if can_move:
            visited.add(adjacent_pos)

    if next_cell == '.':
        can_move = True

    return can_move


def parse_matrix(f):
    matrix = []

    robot_pos = None

    for i, line in enumerate(f):
        if not line.strip():
            break

        matrix.append([])

        for j, s in enumerate(line.strip()):
            matrix[i].append(s)
            if s == '@':
                robot_pos = (i, j)

    return matrix, robot_pos


def parse_moves(f):
    moves = []

    for line in f:
        moves += [s for s in line.strip()]

    return moves


def convert_to_wide_box_matrix(input_matrix):
    matrix = []

    for i, line in enumerate(input_matrix):
        matrix.append([])

        for s in line:
            mark = '..'

            if s == '@':
                mark = '@.'
            elif s == 'O':
                mark = '[]'
            elif s == '#':
                mark = '##'

            l, r = mark

            matrix[i].append(l)
            matrix[i].append(r)

    return matrix


def show(matrix):
    for line in matrix:
        for s in line:
            print(s, end='')
        print()


def simulate_robot_normal_blocks(matrix, start_pos, moves):
    robot = start_pos

    for move in moves:
        shift = SHIFTS[move]

        place_to_shift = next_pos(robot, shift)
        while get(place_to_shift, matrix) == 'O':
            place_to_shift = next_pos(place_to_shift, shift)

        cell_to_shift = get(place_to_shift, matrix)

        if cell_to_shift == '#':
            continue
        else:
            assert cell_to_shift == '.'

            set_mx(robot, matrix, '.')
            robot = next_pos(robot, shift)
            set_mx(robot, matrix, '@')

            box_pos = robot
            while box_pos != place_to_shift:
                box_pos = next_pos(box_pos, shift)
                set_mx(box_pos, matrix, 'O')


def simulate_robot_wide_blocks(matrix, start_pos, moves):
    robot = start_pos

    for move in moves:
        shift = SHIFTS[move]

        if move == '<' or move == '>':
            place_to_shift = next_pos(robot, shift)
            while get(place_to_shift, matrix) == ']' or get(place_to_shift, matrix) == '[':
                place_to_shift = next_pos(place_to_shift, shift)

            cell_to_shift = get(place_to_shift, matrix)

            if cell_to_shift == '#':
                continue
            else:
                assert cell_to_shift == '.'

                set_mx(robot, matrix, '.')
                robot = next_pos(robot, shift)
                set_mx(robot, matrix, '@')

                box_pos = robot
                while box_pos != place_to_shift:
                    box_pos = next_pos(box_pos, shift)
                    s1, s2 = '[]'
                    if move == '<':
                        s1, s2 = ']['
                    set_mx(box_pos, matrix, s1)
                    box_pos = next_pos(box_pos, shift)
                    set_mx(box_pos, matrix, s2)
        else:
            assert move == '^' or move == 'v'
            visited = set()

            if check_can_move(robot, matrix, visited, shift):
                # erase all the touched positions
                for x, y in visited:
                    set_mx((x, y), matrix, '.')
                    set_mx((x, y + 1), matrix, '.')

                set_mx(robot, matrix, '.')
                robot = next_pos(robot, shift)
                set_mx(robot, matrix, '@')

                # fill all the visited positions
                for x, y in visited:
                    set_mx(next_pos((x, y), shift), matrix, '[')
                    set_mx(next_pos((x, y + 1), shift), matrix, ']')


def compute_score(matrix, box_start='O'):
    score = 0
    factor = 100

    for i, line in enumerate(matrix):
        for j, s in enumerate(line):
            if s == box_start:
                score += i * factor + j
    return score


def solve(f, params):
    matrix, start_pos = parse_matrix(f)
    moves = parse_moves(f)

    wide_matrix = convert_to_wide_box_matrix(matrix)
    wide_matrix_start_pos = (start_pos[0], start_pos[1] * 2)

    # simulate robot moves
    simulate_robot_normal_blocks(matrix, start_pos, moves)
    print("Answer 1: ", compute_score(matrix, box_start='O'))
    if params.show_result:
        show(matrix)

    # simulate robot moves in case of wide blocks
    simulate_robot_wide_blocks(wide_matrix, wide_matrix_start_pos, moves)
    print("Answer 2: ", compute_score(wide_matrix, box_start='['))
    if params.show_result:
        show(wide_matrix)
 

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input', type=str, default='input.txt')
    arg_parser.add_argument('--show-result', default=False, action='store_true')

    params = arg_parser.parse_args()
    input_file = params.input

    with open(input_file, 'r') as f:
        solve(f, params)
