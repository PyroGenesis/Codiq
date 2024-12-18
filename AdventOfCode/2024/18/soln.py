import os

here = os.path.dirname(os.path.abspath(__file__))


def read_data(filename: str):
    global here

    # paths
    filepath = os.path.join(here, filename)
    # read input
    with open(filepath, mode="r", encoding="utf8") as f:
        return f.read()


from dataclasses import dataclass
import heapq as hq
import sys


@dataclass(frozen=True)
class Point2D:
    i: int
    j: int


# up right down left
DIRECTIONS = [(-1, 0), (0, +1), (1, 0), (0, -1)]


def getShortestPathLen(n_grid: int, bytes: list[str], n_bytes: int):
    blocked = set()
    for bi in range(n_bytes):
        j, i = (int(x) for x in bytes[bi].split(","))
        blocked.add((i, j))

    start, end = Point2D(0, 0), Point2D(n_grid, n_grid)
    visited = set()
    min_dist = {}
    min_dist[start] = 0
    min_heap = [(0, id(start), start)]

    while min_heap:
        dist_to_point, _, point = hq.heappop(min_heap)
        if point in visited:
            continue
        visited.add(point)

        if point == end:
            break

        for di, dj in DIRECTIONS:
            neighbor = Point2D(point.i + di, point.j + dj)
            if not (0 <= neighbor.i <= n_grid) or not (0 <= neighbor.j <= n_grid):
                continue
            if (neighbor.i, neighbor.j) in blocked:
                continue
            neigh_dist = dist_to_point + 1
            if neigh_dist < min_dist.get(neighbor, sys.maxsize):
                min_dist[neighbor] = neigh_dist
                hq.heappush(min_heap, (neigh_dist, id(neighbor), neighbor))

    return min_dist.get(end, sys.maxsize)


def part1(filename: str, n_grid: int, n_bytes: int):
    data = read_data(filename)
    bytes = data.splitlines()
    return getShortestPathLen(n_grid, bytes, n_bytes)


assert part1("sample.txt", 6, 12) == 22
assert part1("input.txt", 70, 1024) == 298


def part2(filename: str, n_grid: int):
    data = read_data(filename)
    bytes = data.splitlines()

    lo, hi = 0, len(bytes) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        # n_bytes is mid + 1 because it is a count, not an index
        if getShortestPathLen(n_grid, bytes, mid + 1) != sys.maxsize:
            lo = mid + 1
        else:
            hi = mid
    return bytes[lo]


assert part2("sample.txt", 6) == "6,1"
print(part2("input.txt", 70))
print("All done!")
