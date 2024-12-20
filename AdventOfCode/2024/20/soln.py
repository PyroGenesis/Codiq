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


def soln(filename: str, cheat_time: int = 2):
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
        for di in range(-cheat_time, cheat_time + 1):
            dj_range = cheat_time - abs(di)
            for dj in range(-dj_range, dj_range + 1):
                wall_skip_point = Point2D(point.i + di, point.j + dj)
                if wall_skip_point not in min_dist:
                    # since every point has to be in min_dist for this racetrack
                    continue
                time_saved = min_dist[wall_skip_point] - (min_dist[point] + abs(di) + abs(dj))
                if time_saved > 0:
                    cheats[min(time_saved, 100)] += 1

        point = prev_point[point]

    return cheats


sample_cheats = soln("sample.txt")
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

print("Part 1: ", soln("input.txt")[100])

sample_cheats_2 = soln("sample.txt", cheat_time=20)
assert sample_cheats_2[50] == 32
assert sample_cheats_2[52] == 31
assert sample_cheats_2[54] == 29
assert sample_cheats_2[56] == 39
assert sample_cheats_2[58] == 25
assert sample_cheats_2[60] == 23
assert sample_cheats_2[62] == 20
assert sample_cheats_2[64] == 19
assert sample_cheats_2[66] == 12
assert sample_cheats_2[68] == 14
assert sample_cheats_2[70] == 12
assert sample_cheats_2[72] == 22
assert sample_cheats_2[74] == 4
assert sample_cheats_2[76] == 3


print("Part 2: ", soln("input.txt", cheat_time=20)[100])
