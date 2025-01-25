import argparse
import collections


def to_disk(line):
    disk = []

    positions = collections.defaultdict(list)
    file_size = {}

    for i, s in enumerate(line):
        count = int(s)
        if i % 2 == 0:
            file_index = i // 2
            # file
            for _ in range(count):
                disk.append(file_index)
            file_size[file_index] = count
        else:
            # empty
            empty_start = len(disk)
            for _ in range(count):
                disk.append(-1)

            positions[count].append(empty_start)

    return disk, positions, file_size


def calculate_checksum(disk):
    checksum = 0
    for i, val in enumerate(disk):
        if val != -1:
            checksum += i * val
    return checksum


def solve(f):
    line = [c for c in f.read().strip()]

    disk, positions, file_size = to_disk(line)

    # First type defragmentation
    fixed_disk = disk.copy()

    l = 0
    r = len(disk) - 1

    while l < r:
        if fixed_disk[l] != -1:
            l += 1
            continue

        if fixed_disk[r] == -1:
            r -= 1
            continue

        fixed_disk[l], fixed_disk[r] = fixed_disk[r], fixed_disk[l]
        l += 1
        r -= 1

    print("Result 1: ", calculate_checksum(fixed_disk))

    # Second type defragmentation (move the whole files)
    r = len(disk) - 1
    moved_files = set()

    while r > 0:
        cur_file_id = disk[r]

        if cur_file_id == -1:
            r -= 1
            continue

        cur_file_size = file_size[cur_file_id]

        moved = False

        if cur_file_id not in moved_files:

            fit_index = None
            first_pos = None

            # find the most suitable place
            for fi in range(cur_file_size, 10):
                if len(positions[fi]) > 0:
                    best_pos = positions[fi][0]

                    if first_pos is None or first_pos > best_pos:
                        first_pos = best_pos
                        fit_index = fi

            if first_pos is not None and first_pos < r - cur_file_size + 1:
                # place file in the empty space
                for i in range(cur_file_size):
                    disk[r] = -1
                    disk[first_pos + i] = cur_file_id
                    r -= 1

                if fit_index != cur_file_size:
                    new_empty_block_start = first_pos + cur_file_size
                    remaining = fit_index - cur_file_size
                    positions[remaining].append(new_empty_block_start)
                    positions[remaining] = sorted(positions[remaining])

                positions[fit_index].pop(0)
                # each file is moved only once!
                moved_files.add(cur_file_id)
                moved = True

        if not moved:
            r -= cur_file_size

    print("Result 2: ", calculate_checksum(disk))


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input', type=str, default='input.txt')

    input_file = arg_parser.parse_args().input

    with open(input_file, 'r') as f:
        solve(f)
