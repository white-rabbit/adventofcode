import argparse
from collections import defaultdict
from collections import deque

INF = int(1e9)
SHIFTS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def get(pos, mx):
    i, j = pos
    if i < 0 or i >= len(mx):
        return None
    if j < 0 or j >= len(mx[i]):
        return None
    return mx[i][j]


def move(pos, shift):
    return (pos[0] + shift[0], pos[1] + shift[1])


def parse_input(f):
    matrix = []

    start = None
    end = None

    for i, line in enumerate(f):
        if not line.strip():
            break

        matrix.append([])

        for j, s in enumerate(line.strip()):
            if s == 'S':
                start = (i, j)
            elif s == 'E':
               end = (i, j)

            matrix[i].append(s)

    return start, end, matrix


def solve(f):
    start, end, matrix = parse_input(f)

    # dijkstra algorithm
    start_v = (start, (0, 1))

    dist = defaultdict(lambda: INF)
    dist[start_v] = 0

    active = set([start_v])
    parent = {}

    while active:
        best_dist = INF
        best_v = None

        # find best vertex
        for v in active:
            if best_dist > dist[v]:
                best_dist = dist[v]
                best_v = v

        assert best_dist != INF

        pos, shift = best_v

        for next_shift in SHIFTS:
            if next_shift == shift:
                # move forward
                next_pos = move(pos, next_shift)
                next_v = (next_pos, next_shift)

                if get(next_pos, matrix) != '#':
                    if dist[next_v] > best_dist + 1:
                        active.add(next_v)
                        dist[next_v] = best_dist + 1
                        parent[next_v] = [best_v]
                    elif dist[next_v] == best_dist + 1:
                        parent[next_v].append(best_v)

            elif next_shift[0] + shift[0] != 0 and next_shift[1] + shift[1] != 0:
                # rotate
                next_v = (pos, next_shift)

                if dist[next_v] > best_dist + 1000:
                    active.add(next_v)
                    dist[next_v] = best_dist + 1000
                    parent[next_v] = [best_v]
                elif dist[next_v] == best_dist + 1000:
                    parent[next_v].append(best_v)

        active.remove(best_v)

    # find shortest path
    shortest_path = INF
    for shift in SHIFTS:
        shortest_path = min(shortest_path, dist[(end, shift)])

    print("Answer 1: ", shortest_path)

    # find all end vertices
    q = deque()
    for shift in SHIFTS:
        if shortest_path == dist[(end, shift)]:
            q.append((end, shift))

    # backtracking
    good_positions = set()

    while q:
        v = q.popleft()
        good_positions.add(v[0])

        for u in parent.get(v, []):
            q.append(u)

    print("Answer 2: ", len(good_positions))
    

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input', type=str, default='input.txt')

    input_file = arg_parser.parse_args().input

    with open(input_file, 'r') as f:
        solve(f)
