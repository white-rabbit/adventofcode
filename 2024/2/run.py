import argparse


def solve(f):
    def check_safe(values):
        for i in range(0, len(values) - 1):
            diff = values[i + 1] - values[i]

            if diff < 1 or diff > 3:
                return False

        return True

    def check_tolerate_safe(values):
        if not check_safe(values):
            for i in range(len(values)):
                temp_values = values[:i] + values[i + 1:]
                if check_safe(temp_values):
                    return True
            return False
        return True

    count_safe = 0
    count_tolerate_safe = 0

    for line in f:
        values = [int(v) for v in line.split()]

        if check_safe(values) or check_safe(values[::-1]):
            count_safe += 1

        if check_tolerate_safe(values) or check_tolerate_safe(values[::-1]):
            count_tolerate_safe += 1

    print('Count safe', count_safe)
    print('Count tolerate safe', count_tolerate_safe)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input', type=str, default='input.txt')
    input_file = arg_parser.parse_args().input

    with open(input_file, 'r') as f:
        solve(f)
