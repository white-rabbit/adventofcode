import argparse
from collections import defaultdict


SHIFTS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def get(pos, mx):
    i, j = pos
    if i < 0 or i >= len(mx):
        return None
    if j < 0 or j >= len(mx[i]):
        return None
    return mx[i][j]


def get_vertices(pos, mx, inner=False):
    vertices = set()
    c = get(pos, mx)

    for i in [-1, 1]:
        for j in [-1, 1]:
            diag = c != get((pos[0] + i, pos[1] + j), mx)
            a = pos[0] + i, pos[1]
            b = pos[0], pos[1] + j
            side1 = c == get(a, mx)
            side2 = c == get(b, mx)

            if not inner:
                side1 = not side1
                side2 = not side2

            if (side1 and side2) and (not inner or diag):
                vertices.add((a, b))

    return vertices


def get_edges_count(pos, mx):
    cell = get(pos, mx)

    count = 0

    for shift in SHIFTS:
        ng_pos = (pos[0] + shift[0], pos[1] + shift[1])
        ng_cell = get(ng_pos, mx)
        
        if cell != ng_cell:
            count += 1

    return count


def dfs(pos, mx, used):
    area = 0

    vertices = set()
    cur_cell = get(pos, mx)
    vertices |= get_vertices(pos, mx, inner=False)
    vertices |= get_vertices(pos, mx, inner=True)

    edges_count = get_edges_count(pos, mx)

    for shift in SHIFTS:
        new_pos = (pos[0] + shift[0], pos[1] + shift[1])
        new_cell = get(new_pos, mx)

        if new_cell == cur_cell and new_cell is not None:
            if used[new_pos[0]][new_pos[1]]:
                continue

            used[new_pos[0]][new_pos[1]] = True
            new_area, new_edges_count, new_vertices = dfs(new_pos, mx, used)
            area += new_area
            edges_count += new_edges_count
            vertices |= new_vertices

    return area + 1, edges_count, vertices



def solve(f):
    matrix = []
    used = []

    for line in f:
        matrix.append([x for x in line.strip()])
        used.append([False for _ in line.strip()])

    fences_simple_cost = 0
    fences_discount_cost = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if not used[i][j]:
                used[i][j] = True
                area, edges_count, vertices = dfs((i, j), matrix, used)
                fences_simple_cost += area * edges_count
                fences_discount_cost += area * len(vertices)

    print("Answer 1: ", fences_simple_cost)
    print("Answer 2: ", fences_discount_cost)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input', type=str, default='input.txt')

    input_file = arg_parser.parse_args().input

    with open(input_file, 'r') as f:
        solve(f)



