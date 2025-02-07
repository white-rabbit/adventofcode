from collections import defaultdict


def dfs(graph, v, visited):
    visited.add(v)

    next_u = []

    cur_vis = visited.copy()

    for u in sorted(graph[v]):
        if u not in visited:
            if visited <= graph[u]:
                dfs(graph, u, visited)


def check_lan(graph, lan):
    for v in lan:
        for u in lan:
            if u != v:
                if v not in graph[u]:
                    return False
    return True


def solve(f):
    graph = defaultdict(set)

    for l in f:
        u, v = l.split("-")
        u = u.strip()
        v = v.strip()
        graph[u].add(v)
        graph[v].add(u)

    vertices = list(graph)
    terminals = list(filter(
        lambda x: x.startswith("t"),
        vertices
    ))

    triples = set()

    for t in terminals:
        for u in graph[t]:
            for v in graph[u]:
                if v != t and t in graph[v]:
                    a, b, c = sorted([t, u, v])
                    triples.add((a, b, c))

    print("Answer 1:", len(triples))

    components = []

    for v in graph:
        visited = set()
        dfs(graph, v, visited)
        if check_lan(graph, visited):
            components.append(visited)

    largest_lan = set()

    counter = {}
    for lan in components:
        if len(lan) > len(largest_lan):
            largest_lan = lan

        counter[len(lan)] = 1 + counter.get(len(lan), 0)

    assert check_lan(graph, largest_lan)

    print("Answer 2:", ",".join(sorted(largest_lan)))


if __name__ == "__main__":
    input_file = "input.txt"

    with open(input_file, "r") as f:
        solve(f)
