import argparse


def parse(line):
    useful = ''.join(
        [x for x in line
        if x.isdigit() or x == ','])

    x, y = (int(x) for x in useful.split(','))
    return x, y


def calc(ax, ay, bx, by, goalx, goaly):
    m = [[ax, bx], [ay, by]]

    det = (m[0][0] * m[1][1]) - (m[1][0] * m[0][1])

    if det != 0:
        m_inv = [
            [m[1][1], -m[0][1]],
            [-m[1][0], m[0][0]]
        ]

        c1 = m_inv[0][0] * goalx + m_inv[0][1] * goaly
        c2 = m_inv[1][0] * goalx + m_inv[1][1] * goaly

        if c1 % det == 0 and c2 % det == 0:
            x = c1 // det
            y = c2 // det
            return x * 3 + y

    return 0


def solve(f):
    lines = list(f)

    dgoal = 10000000000000
    
    result1 = 0
    result2 = 0

    for i in range(0, len(lines), 4):
        ax, ay = parse(lines[i])
        bx, by = parse(lines[i + 1])
        goalx, goaly = parse(lines[i + 2])
        result1 += calc(ax, ay, bx, by, goalx, goaly)
        result2 += calc(ax, ay, bx, by, goalx + dgoal, goaly + dgoal)

    print("Answer 1: ", result1)
    print("Answer 2: ", result2)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input', type=str, default='input.txt')

    input_file = arg_parser.parse_args().input

    with open(input_file, 'r') as f:
        solve(f)
