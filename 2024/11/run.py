import argparse
import collections


class Stone:
    def __init__(self, value, count):
        self.value = value
        self.count = count

    def __add__(self, other):
        return Stone(self.value + other.value, self.count + other.count)

    def __iadd__(self, other):
        self.count += other.count
        return self

    def __eq__(self, other):
        return self.value == other.value

    def split(self):
        n = len(self.value)
        assert n % 2 == 0
        left_value, right_value = self.value[:n//2], self.value[n//2:]

        def trim(value):
            start_index = 0
            for s in value:
                if s == '0':
                    start_index += 1
                else:
                    break

            ret = value[start_index:]
            if ret == '':
                ret = '0'

            return ret

        left_value = trim(left_value)
        right_value = trim(right_value)

        return Stone(left_value, self.count), Stone(right_value, self.count)


def put(stone, line):
    if stone.value in line:
        line[stone.value] += stone
    else:
        line[stone.value] = stone


def compute_stone_count(stone_line):
    result = 0
    for stone in stone_line.values():
        result += stone.count
    return result


def do_blinks(stone_line, count):
    for step in range(count):
        new_line = {}

        for stone in stone_line.values():
            if stone.value == '0':
                stone.value = '1'
                put(stone, new_line)
            elif len(stone.value) % 2 == 0:
                left_stone, right_stone = stone.split()
                put(left_stone, new_line)
                put(right_stone, new_line)
            else:
                stone.value = str(int(stone.value) * 2024)
                put(stone, new_line)

        stone_line = new_line

    return stone_line


def solve(f):
    line = {}

    for x in f.readline().strip().split():
        put(Stone(x, 1), line)

    line = do_blinks(line, 25)
    result1 = compute_stone_count(line)
    print("Result 1: ", result1)

    line = do_blinks(line, 50)
    result2 = compute_stone_count(line)
    print("Result 2: ", result2)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input', type=str, default='input.txt')

    input_file = arg_parser.parse_args().input

    with open(input_file, 'r') as f:
        solve(f)
