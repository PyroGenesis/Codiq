import os

# paths
here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, "input.txt")

# read input
with open(filepath, mode="r", encoding="utf8") as f:
    data = f.read()

m, n = 103, 101
seconds = 100

import re

pattern_p = re.compile(r"p=(-?\d+),(-?\d+)")
pattern_v = re.compile(r"v=(-?\d+),(-?\d+)")


def part1():
    def position_to_quadrant(i: int, j: int) -> int:
        global m, n
        middle_m, middle_n = m // 2, n // 2
        if i == middle_m or j == middle_n:
            return 0

        quadrant = 1
        if i > middle_m:
            quadrant += 2
        if j > middle_n:
            quadrant += 1
        return quadrant

    count = [0, 0, 0, 0, 0]
    for state in data.splitlines():
        position = tuple(int(x) for x in pattern_p.search(state).groups())
        velocity = tuple(int(x) for x in pattern_v.search(state).groups())
        new_position = (
            (position[0] + velocity[0] * seconds) % n,
            (position[1] + velocity[1] * seconds) % m,
        )
        # print(position, velocity, new_position)
        count[position_to_quadrant(new_position[1], new_position[0])] += 1

    safety_factor = 1
    for i in range(1, 5):
        safety_factor *= count[i]

    print(count)
    print(safety_factor)


# class Robot:
#     def __init__(self, position, velocity) -> None:
#         self.position = position
#         self.velocity = velocity

#     def get_next_position(self):
#         return (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])


def get_next_position(
    position: tuple[int, int], velocity: tuple[int, int]
) -> tuple[int, int]:
    global m, n
    return ((position[0] + velocity[0]) % n, (position[1] + velocity[1]) % m)


from collections import defaultdict
from copy import deepcopy


def part2():
    def create_grid():
        return [[[] for _ in range(n)] for _ in range(m)]

    grid = create_grid()

    for state in data.splitlines():
        position = tuple(int(x) for x in pattern_p.search(state).groups())
        velocity = tuple(int(x) for x in pattern_v.search(state).groups())
        grid[position[1]][position[0]].append((velocity[1], velocity[0]))

    def get_biggest_cluster():
        global m, n
        nonlocal grid
        biggest_cluster = 0
        done = set()
        for i in range(m):
            for j in range(n):
                if (i, j) in done or len(grid[i][j]) == 0:
                    continue
                stack = [(i, j)]
                cluster = 0
                while stack:
                    ci, cj = stack.pop()
                    if (ci, cj) in done:
                        continue
                    done.add((ci, cj))
                    cluster += 1

                    if ci > 0 and len(grid[ci - 1][cj]) > 0:
                        stack.append((ci - 1, cj))
                    if cj > 0 and len(grid[ci][cj - 1]) > 0:
                        stack.append((ci, cj - 1))
                    if ci < m - 1 and len(grid[ci + 1][cj]) > 0:
                        stack.append((ci + 1, cj))
                    if cj < n - 1 and len(grid[ci][cj + 1]) > 0:
                        stack.append((ci, cj + 1))
                biggest_cluster = max(biggest_cluster, cluster)
        return biggest_cluster

    def grid_to_str():
        return "\n".join(
            " ".join(str(len(grid[i][j])) for j in range(n)) for i in range(m)
        )

    max_cluster = {
        "size": 0,
        "grid": "",
        "second": 0
    }  # fmt: skip
    for second in range(m * n + 1):
        # print(second, end=" ")

        biggest_cluster = get_biggest_cluster()
        if biggest_cluster > max_cluster["size"]:
            print(f"{max_cluster['size']} -> {biggest_cluster} for second {second}")
            max_cluster["size"] = biggest_cluster
            max_cluster["grid"] = grid_to_str()
            max_cluster["second"] = second
        next_grid = create_grid()
        for i in range(m):
            for j in range(n):
                for vi, vj in grid[i][j]:
                    next_grid[(i + vi) % m][(j + vj) % n].append((vi, vj))
        grid = next_grid

    print()
    print(f'{max_cluster["second"]=}, {max_cluster["size"]=}')
    print(max_cluster["grid"])


# part1()
part2()
