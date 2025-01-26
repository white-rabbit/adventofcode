import argparse
from functools import reduce


def parse(line):
    position, velocity = line.split(' ')
    position = position.split('=')[1].split(',')
    velocity = velocity.split('=')[1].split(',')

    position = (int(position[0]), int(position[1]))
    velocity = (int(velocity[0]), int(velocity[1]))
    return position, velocity


def solve(f, params):
    lines = list(f)

    robots = []

    for line in lines:
        p, v = parse(line)
        robots.append((p, v))

    time = 0

    width = 11
    height = 7

    if len(lines) > 100:
        width = 101
        height = 103

    def show_matrix(matrix):
        for line in matrix:
            for l in line:
                print(l, end='')
            print()

    def move_robots(robots):
        n = len(robots)
        for i in range(n):
            pos, vel = robots[i]
            next_pos = (
                    (pos[0] + vel[0]) % width,
                    (pos[1] + vel[1]) % height)
            robots[i] = (next_pos, vel)

    def calc_dispersion(robots):
        n = len(robots)
        avg_x = sum([r[0][0] for r in robots]) / n
        avg_y = sum([r[0][1] for r in robots]) / n

        std_x = sum([(r[0][0] - avg_x) ** 2 for r in robots]) / n
        std_y = sum([(r[0][1] - avg_x) ** 2 for r in robots]) / n

        return std_x + std_y

    # Assume the average dispersion is way less than
    # the dispersion for the tree picture
    avg_dispersion = 0

    for i in range(100):
        time += 1
        move_robots(robots)
        avg_dispersion += calc_dispersion(robots)

    avg_dispersion /= 100
    
    def calc_safety_factor(robots):
        quadrant_score = {}

        w_middle = width // 2
        h_middle = height // 2

        for pos, _ in robots:
            if pos[0] == w_middle or pos[1] == h_middle:
                continue
            key = (pos[0] > w_middle, pos[1] > h_middle)

            if key in quadrant_score:
                quadrant_score[key] += 1
            else:
                quadrant_score[key] = 1

        return reduce(lambda x, y: x * y, quadrant_score.values())

    print("Answer 1: ", calc_safety_factor(robots))

    def is_christmass_tree(robots, avg_dispersion):
        dispersion = calc_dispersion(robots)
        # assume that if the dispersion is less than half of
        # the average dispersion, it means there is something
        # unusual and likely the christmass tree
        return dispersion < 0.5 * avg_dispersion

    while not is_christmass_tree(robots, avg_dispersion):
        time += 1
        move_robots(robots)

    def show(robots):
        matrix = []
        for i in range(height):
            matrix.append(['.'] * width)

        for p, _ in robots:
            matrix[p[1]][p[0]] = '*'

        for line in matrix:
            for l in line:
                print(l, end='')
            print()

    if params.show_result:
        show(robots)

    print("Answer 2: ", time)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
            '--input', type=str, default='input.txt')
    arg_parser.add_argument(
            '--show-result', default=False, action='store_true', dest='show_result')

    params = arg_parser.parse_args()
    input_data = params.input

    with open(input_data, 'r') as f:
        solve(f, params)
