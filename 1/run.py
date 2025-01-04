import numpy as np
import argparse
from collections import Counter

def solve(f):
    left_column, right_column = [], []
    counter = Counter()
    for line in f:
        left, right = (int(x) for x in line.split())
        left_column.append(left)
        right_column.append(right)
        counter[right] += 1

    left_arr = np.array(sorted(left_column))
    right_arr = np.array(sorted(right_column))

    distance = np.sum(np.abs(left_arr - right_arr))

    print('Distance', distance)

    similarity = 0

    for l in left_column:
        similarity += counter[l] * l

    print('Similarity', similarity)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input', type=str, default='input.txt')
    input_file = arg_parser.parse_args().input

    with open(input_file, 'r') as f:
        solve(f)
