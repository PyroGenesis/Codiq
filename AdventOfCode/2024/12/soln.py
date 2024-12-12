import os

# paths
here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, 'input.txt')

# read input
with open(filepath, mode='r', encoding='utf8') as f:
    data = f.read()

garden = data.splitlines()
m, n = len(garden), len(garden[0])

def part1():
    done = set()

    def fenceRegionFrom(i, j):
        global garden, m, n

        plant = garden[i][j]
        stack = [(i, j)]
        area, perimeter = 0, 0

        while stack:
            ci, cj = stack.pop()
            if (ci, cj) in done:
                continue
            done.add((ci, cj))

            area += 1
            if ci > 0 and garden[ci-1][cj] == plant:
                stack.append((ci-1, cj))
            else:
                perimeter += 1
            if cj > 0 and garden[ci][cj-1] == plant:
                stack.append((ci, cj-1))
            else:
                perimeter += 1
            if ci < m-1 and garden[ci+1][cj] == plant:
                stack.append((ci+1, cj))
            else:
                perimeter += 1
            if cj < n-1 and garden[ci][cj+1] == plant:
                stack.append((ci, cj+1))
            else:
                perimeter += 1
        
        return area * perimeter

    fences = 0
    for i in range(m):
        for j in range(n):
            if (i, j) in done:
                continue
            fences += fenceRegionFrom(i, j)

    print(fences)

from collections import deque

def part2():
    done = set()

    def fenceRegionFrom(i, j):
        global garden, m, n

        plant = garden[i][j]
        queue = deque([(i, j)])
        area, sides = 0, 0
        edges = set()

        while queue:
            ci, cj = queue.popleft()
            if (ci, cj) in done:
                continue
            done.add((ci, cj))

            area += 1

            # top
            if ci > 0 and garden[ci-1][cj] == plant:
                queue.append((ci-1, cj))
            else:
                ei, ej = ci-0.5, cj
                if (ei, ej-1) not in edges and (ei, ej+1) not in edges:
                    sides += 1
                    # print(ci, cj, "top")
                edges.add((ei, ej))
                # edges.add((ei, ej+0.5))
                # edges.add((ei, ej-0.5))

            # left
            if cj > 0 and garden[ci][cj-1] == plant:
                queue.append((ci, cj-1))
            else:
                ei, ej = ci, cj-0.5
                if (ei-1, ej) not in edges and (ei+1, ej) not in edges:
                    sides += 1
                    # print(ci, cj, "left")
                edges.add((ei, ej))
                # edges.add((ei+0.5, ej))
                # edges.add((ei-0.5, ej))

            # bottom
            if ci < m-1 and garden[ci+1][cj] == plant:
                queue.append((ci+1, cj))
            else:
                ei, ej = ci+0.5, cj
                if (ei, ej-1) not in edges and (ei, ej+1) not in edges:
                    sides += 1
                    # print(ci, cj, "bottom")
                edges.add((ei, ej))
                # edges.add((ei, ej+0.5))
                # edges.add((ei, ej-0.5))
            
            # right
            if cj < n-1 and garden[ci][cj+1] == plant:
                queue.append((ci, cj+1))
            else:
                ei, ej = ci, cj+0.5
                if (ei-1, ej) not in edges and (ei+1, ej) not in edges:
                    sides += 1
                    # print(ci, cj, "right")
                edges.add((ei, ej))
                # edges.add((ei+0.5, ej))
                # edges.add((ei-0.5, ej))
        
        return area * sides

    fences = 0
    for i in range(m):
        for j in range(n):
            if (i, j) in done:
                continue
            fences += fenceRegionFrom(i, j)

    print(fences)

# part1()
part2()
