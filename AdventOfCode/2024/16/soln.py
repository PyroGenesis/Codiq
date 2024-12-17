import os

# paths
here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, "input.txt")

# read input
with open(filepath, mode="r", encoding="utf8") as f:
    data = f.read()

from collections import defaultdict
from dataclasses import dataclass
import heapq as hq
import math

# up, right, down left
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


# Represent a node using its location and the direction
@dataclass(frozen=True)
class Node:
    i: int
    j: int
    dir: int


maze = data.splitlines()
m, n = len(maze), len(maze[0])

# we always start from bottom-left corner (facing east)
start_node = Node(m - 2, 1, 1)
# we always end in top-right corner (direction doesn't matter)
end_node = Node(1, n - 2, -1)

# the graph will be updated lazily because it is too much processing
#   to completely populate it beforehand
graph = defaultdict(list)
# track nodes whose all edges have been explored
visited = set()
# heap to choose next node to explore
# need to add id as middle tuple element so that nodes dont get compared
min_heap = [(0, id(start_node), start_node)]
# min distance from start_node to node so far
# missing values are treated as math.inf
min_dist = {}
min_dist[start_node] = 0
# keep track of all previous nodes for making path
prev_nodes = defaultdict(list)


# utility method for debugging (prints the map)
def print_map(current_node, prev_nodes):
    pns = set((n.i, n.j) for n in prev_nodes)
    for i in range(m):
        for j in range(n):
            if i == current_node.i and j == current_node.j:
                print("X", end="")
            elif (i, j) in pns:
                print("O", end="")
            else:
                print(maze[i][j], end="")
        print()


# Run Dijkstra's algo
while min_heap:
    cost_to_node, _, node = hq.heappop(min_heap)
    if node in visited:
        continue
    visited.add(node)

    # early exit in the case we have explored all paths to the finish
    if node.i == end_node.i and node.j == end_node.j:
        # assign end so that we know which direction end was reached by
        end_node = node
        break

    # update adjacency graph from current node
    di, dj = DIRECTIONS[node.dir]
    if maze[node.i + di][node.j + dj] != "#":
        moved_node = Node(node.i + di, node.j + dj, node.dir)
        graph[node].append((moved_node, 1))
    for x in range(3):
        rotated_node = Node(node.i, node.j, (node.dir + x + 1) % 4)
        graph[node].append((rotated_node, 1000))

    # explore edges
    for neighbor, cost in graph[node]:
        cost_to_neighbor = cost_to_node + cost
        # The following condition was changed from > to >= because we also want to explore
        #   paths with the same cost, not just better cost
        if min_dist.get(neighbor, math.inf) >= cost_to_neighbor:
            min_dist[neighbor] = cost_to_neighbor
            prev_nodes[neighbor].append(node)
            # need to add id as middle tuple element so that nodes dont get compared
            hq.heappush(min_heap, (cost_to_neighbor, id(neighbor), neighbor))

print(f"Part 1: {min_dist[end_node]}")

# PART II: Run through the path backwards, making note of all coords

visited = set([start_node])
path_locs = set([(start_node.i, start_node.j)])  # all unique locations in path
stack = [end_node]

while stack:
    node = stack.pop()
    if node in visited:
        continue
    visited.add(node)

    path_locs.add((node.i, node.j))

    for prev_node in prev_nodes[node]:
        stack.append(prev_node)

print(f"Part 2: {len(path_locs)}")
