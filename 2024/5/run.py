import argparse
import collections


def is_order_correct(pages, parent_set):
    next_parents = set()

    for page in pages:
        if page in next_parents:
            return False
        next_parents = parent_set[page]

    return True


def get_fixed_order(pages, parent_set):
    next_parents = set()

    ordered = []

    fixed = False

    for i, page in enumerate(pages):
        ordered.append(page)

        if page in next_parents:
            fixed = True

            for j in range(i, 0, -1):
                if page in parent_set[ordered[j - 1]]:
                    ordered[j - 1], ordered[j] = ordered[j], ordered[j - 1]
        else:
            next_parents = parent_set[page]

    assert is_order_correct(ordered, parent_set)

    return fixed, ordered


def solve(f):
    parent_set = collections.defaultdict(set)

    # parse tree
    for line in f:
        if not line.strip():
            # the input is split in two parts
            # divided by an empty string
            break

        parent, child = tuple(map(int, line.split('|')))
        parent_set[child].add(parent)

    # process pages
    correct_pages = 0
    corrected_pages = 0

    for line in f:
        pages = list(map(int, line.split(',')))

        if is_order_correct(pages, parent_set):
            correct_pages += pages[len(pages) // 2]

        fixed, ordered_pages = get_fixed_order(
            pages, parent_set)

        if fixed:
            middle_page = ordered_pages[len(pages) // 2]
            corrected_pages += middle_page

    print("Correct pages: ", correct_pages)
    print("Corrected pages: ", corrected_pages)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input', type=str, default='input.txt')
    input_file = arg_parser.parse_args().input

    with open(input_file, 'r') as f:
        solve(f)

