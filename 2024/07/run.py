import argparse


def can_compute(result, current, operands, allow_concat):
    if not operands:
        return current == result

    if current > result:
        return False

    first = operands[0]
    rest = operands[1:]

    if can_compute(result, current + first, rest, allow_concat):
        return True

    if can_compute(result, current * first, rest, allow_concat):
        return True

    if allow_concat:
        concat = int(str(current) + str(first))
        return can_compute(result, concat, rest, allow_concat)

    return False


def solve(f):
    result_add_mul = 0
    result_add_mul_concat = 0

    for line in f:
        result, operands = line.split(':')

        result = int(result)
        operands = [int(x) for x in operands.split()]

        if can_compute(result, operands[0], operands[1:], False):
            result_add_mul += result
            result_add_mul_concat += result
        elif can_compute(result, operands[0], operands[1:], True):
            result_add_mul_concat += result

    print("Result +, *: ", result_add_mul)
    print("Result +, *, ||: ", result_add_mul_concat)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input', type=str, default='input.txt')

    input_file = arg_parser.parse_args().input

    with open(input_file, 'r') as f:
        solve(f)
