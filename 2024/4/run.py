import argparse


def solve(f):
    matrix = []

    for line in f:
        matrix.append(line)

    def get(x, y):
        if x < 0 or x >= len(matrix):
            return '.'
        if y < 0 or y >= len(matrix[x]):
            return '.'

        return matrix[x][y]

    xmas_count = 0
    x_count = 0

    for i in range(len(matrix)):
        for j, mij in enumerate(matrix[i]):
            if mij == 'X':
                for shift_i in [-1, 0, 1]:
                    for shift_j in [-1, 0, 1]:
                        for k, s in enumerate('MAS', start=1):
                            if get(i + shift_i * k, j + shift_j * k) != s:
                                break
                            if s == 'S':
                                xmas_count += 1

            if mij == 'A':
                diag1 = {get(i + 1, j + 1), get(i - 1, j - 1)}
                diag2 = {get(i + 1, j - 1), get(i - 1, j + 1)}

                if diag1 == {'M', 'S'} and diag2 == {'M', 'S'}:
                    x_count += 1


    print('XMAS count', xmas_count)
    print('X count', x_count)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input', type=str, default='input.txt')
    input_file = arg_parser.parse_args().input

    with open(input_file, 'r') as f:
        solve(f)
