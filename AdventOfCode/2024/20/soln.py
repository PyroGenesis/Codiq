import os

here = os.path.dirname(os.path.abspath(__file__))


# read input
def read_data(filename: str):
    global here

    filepath = os.path.join(here, filename)
    with open(filepath, mode="r", encoding="utf8") as f:
        return f.read()


from collections import defaultdict
from dataclasses import dataclass
import heapq as hq


@dataclass(frozen=True)
class Point2D:
    i: int
    j: int


# up right down left
DIRECTIONS = [(-1, 0), (0, +1), (1, 0), (0, -1)]


def part1(filename: str):
    data = read_data(filename)
    race_track = data.splitlines()
    m, n = len(race_track), len(race_track[0])

    start, end = None, None
    for i in range(m):
        for j in range(n):
            match race_track[i][j]:
                case "S":
                    start = Point2D(i, j)
                case "E":
                    end = Point2D(i, j)
    assert start is not None
    assert end is not None

    visited = set()
    # graph = {}
    min_dist = {}
    min_dist[start] = 0
    prev_point = {}
    prev_point[start] = None
    min_heap = [(0, id(start), start)]

    while min_heap:
        dist_to_point, _, point = hq.heappop(min_heap)
        if point in visited:
            continue
        visited.add(point)

        neighbors = []
        for di, dj in DIRECTIONS:
            if race_track[point.i + di][point.j + dj] != "#":
                neighbors.append(Point2D(point.i + di, point.j + dj))
        assert len(neighbors) <= 2, "there were more than 2 neighbors!"

        for neighbor in neighbors:
            dist_to_neighbor = dist_to_point + 1
            if dist_to_neighbor < min_dist.get(neighbor, m * n):
                min_dist[neighbor] = dist_to_neighbor
                prev_point[neighbor] = point
                hq.heappush(min_heap, (dist_to_neighbor, id(neighbor), neighbor))

    cheats = defaultdict(int)
    point = end
    while point is not None:
        for di, dj in DIRECTIONS:
            if race_track[point.i + di][point.j + dj] != "#":
                continue
            wall_skip_point = Point2D(point.i + di * 2, point.j + dj * 2)
            # if not (0 <= wall_skip_point.i < m) or not (0 <= wall_skip_point.j < n):
            #     continue
            # if race_track[wall_skip_point.i][wall_skip_point.j] == "#":
            #     continue
            if wall_skip_point not in min_dist:
                # since every point has to be in min_dist for this racetrack
                continue
            time_saved = min_dist[wall_skip_point] - (min_dist[point] + 2)
            if time_saved > 0:
                cheats[min(time_saved, 100)] += 1

        point = prev_point[point]

    return cheats


sample_cheats = part1("sample.txt")
assert sample_cheats[2] == 14
assert sample_cheats[4] == 14
assert sample_cheats[6] == 2
assert sample_cheats[8] == 4
assert sample_cheats[10] == 2
assert sample_cheats[12] == 3
assert sample_cheats[20] == 1
assert sample_cheats[36] == 1
assert sample_cheats[38] == 1
assert sample_cheats[40] == 1
assert sample_cheats[64] == 1

print(part1("input.txt")[100])
