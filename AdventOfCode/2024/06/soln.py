import os
from collections import defaultdict

# paths
here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, 'input.txt')

# read input
with open(filepath, mode='r', encoding='utf8') as f:
    data = f.read()
rows = data.splitlines()

# bounds
m = len(rows)
n = len(rows[0])

# directions following 90 degree clockwise turns
#   up, right, down, left
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# find position of guard
guard_i, guard_j = -1, -1
for i in range(m):
    for j in range(n):
        if rows[i][j] == '^':
            guard_i, guard_j = i, j
            break
    if guard_i != -1:
        break


def part1(guard_i, guard_j):
    # keep track of visited positions
    visited = set()
    visited.add((guard_i, guard_j))

    dir_idx = 0     # current direction index

    # loop while guard is in map
    while True:
        delta_i, delta_j = DIRECTIONS[dir_idx]
        next_gi, next_gj = guard_i + delta_i, guard_j + delta_j   # next pos
        
        # if out of bounds, we are done
        if not (0 <= next_gi < m) or not (0 <= next_gj < n):
            break
        # change direction when obstacle encountered
        if rows[next_gi][next_gj] == "#":
            dir_idx = (dir_idx + 1) % 4
            continue
        # update position and visited
        guard_i, guard_j = next_gi, next_gj
        visited.add((guard_i, guard_j))

    print(f"{len(visited)=}")


def part2(guard_i, guard_j):
    # keep track of visited positions
    visited = set()
    visited.add((guard_i, guard_j))

    dir_idx = 0 # current direction index
    loops = 0   # loops encountered

    # walk through the path
    while True:
        delta_i, delta_j = DIRECTIONS[dir_idx]
        next_gi, next_gj = guard_i + delta_i, guard_j + delta_j # next pos
        
        # if out of bounds, we are done
        if not (0 <= next_gi < m) or not (0 <= next_gj < n):
            break
        # change direction when obstacle encountered
        if rows[next_gi][next_gj] == "#":
            dir_idx = (dir_idx + 1) % 4
            continue
        # if a position is not already in path,
        # put a obstacle there and see if guard will loop
        if (next_gi, next_gj) not in visited and willLoop(guard_i, guard_j, dir_idx):
            loops += 1
        # update position and visited
        guard_i, guard_j = next_gi, next_gj
        visited.add((guard_i, guard_j))
    
    print(f"{loops=}")

# used in part 2
# returns whether placing an obstacle on next pos causes a loop or not
def willLoop(guard_i, guard_j, dir_idx) -> bool:
    # obstacle pos
    obs_i, obs_j = guard_i + DIRECTIONS[dir_idx][0], guard_j + DIRECTIONS[dir_idx][1]

    # keep track of visited pos and the direction of travel
    visited: defaultdict[tuple[int, int], list[int]] = defaultdict(list)
    visited[(guard_i, guard_j)].append(dir_idx)
    
    # walk until guard exits map or loops
    while True:
        delta_i, delta_j = DIRECTIONS[dir_idx]
        next_gi, next_gj = guard_i + delta_i, guard_j + delta_j # next pos
        
        # if out of bounds, no loop
        if not (0 <= next_gi < m) or not (0 <= next_gj < n):
            return False
        # change direction when obstacle encountered
        if rows[next_gi][next_gj] == "#" or (next_gi == obs_i and next_gj == obs_j):
            dir_idx = (dir_idx + 1) % 4
            continue
        # we are looping if we encounter a visited pos in a visited direction
        if (next_gi, next_gj) in visited and dir_idx in visited[(next_gi, next_gj)]:
            return True
        
        # update position and visited
        guard_i, guard_j = next_gi, next_gj        
        visited[(guard_i, guard_j)].append(dir_idx)
    
    assert False


part1(guard_i, guard_j)
part2(guard_i, guard_j)
