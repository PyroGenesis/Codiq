import os

here = os.path.dirname(os.path.abspath(__file__))


# read input
def read_data(filename: str):
    global here

    filepath = os.path.join(here, filename)
    with open(filepath, mode="r", encoding="utf8") as f:
        return f.read()


from collections import defaultdict


def part1(filename: str):
    data = read_data(filename)

    graph: defaultdict[str, list[str]] = defaultdict(list)
    for edges in data.splitlines():
        a, b = edges.split("-")
        graph[a].append(b)
        graph[b].append(a)

    unique_triplets = set()
    for computer in graph:
        if not computer.startswith("t"):
            continue
        connected = graph[computer]
        n = len(connected)
        for i in range(n - 1):
            for j in range(i + 1, n):
                if connected[i] not in graph[connected[j]]:
                    continue
                triplet = tuple(sorted([computer, connected[i], connected[j]]))
                unique_triplets.add(triplet)
    return len(unique_triplets)


assert part1("sample.txt") == 7
print("Part 1:", part1("input.txt"))


def part2(filename: str):
    data = read_data(filename)

    graph: defaultdict[str, set[str]] = defaultdict(set)
    for edges in data.splitlines():
        a, b = edges.split("-")
        graph[a].add(b)
        graph[b].add(a)

    max_clique_size, best_clique = 0, None

    def BronKerboschSimple(clique: set, candidates: set, exclude: set):
        nonlocal graph, max_clique_size, best_clique

        if not candidates and not exclude:
            if len(clique) > max_clique_size:
                max_clique_size = len(clique)
                best_clique = list(sorted(clique))
            return
        for computer in candidates.copy():
            BronKerboschSimple(clique | {computer}, candidates & graph[computer], exclude & graph[computer])
            candidates.remove(computer)
            exclude.add(computer)

    BronKerboschSimple(set(), set(graph.keys()), set())
    return ",".join(best_clique)


assert part2("sample.txt") == "co,de,ka,ta"
print("Part 2:", part2("input.txt"))
