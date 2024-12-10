import os

# paths
here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, 'input.txt')

# read input
with open(filepath, mode='r', encoding='utf8') as f:
    data = f.read()

area = [[int(x) for x in row] for row in data.splitlines()]
m, n = len(area), len(area[0])

from collections import deque, defaultdict

def part1():
    def countTrailEndsFrom(root_i: int, root_j: int):
        queue = deque([(root_i, root_j)])
        seen = set()
        curr = 0
        while curr < 9 and queue:
            nq = len(queue)
            for _ in range(nq):
                i, j = queue.popleft()
                if (i, j) in seen:
                    continue
                seen.add((i, j))

                if i > 0 and area[i-1][j] == curr + 1:
                    queue.append((i-1, j))
                if j > 0 and area[i][j-1] == curr + 1:
                    queue.append((i, j-1))
                if i < m-1 and area[i+1][j] == curr + 1:
                    queue.append((i+1, j))
                if j < n-1 and area[i][j+1] == curr + 1:
                    queue.append((i, j+1))
            curr += 1
        return len(set(queue))

    score = 0
    for i in range(m):
        for j in range(n):
            if area[i][j] == 0:
                score += countTrailEndsFrom(i, j)

    print(score)

def part2():
    queue = deque()
    rank = defaultdict(int)
    seen = set()

    for i in range(m):
        for j in range(n):
            if area[i][j] == 0:
                queue.append((i, j))
                rank[(i, j)] = 1
    
    curr = 0
    while curr < 9 and queue:
        nq = len(queue)
        for _ in range(nq):            
            i, j = queue.popleft()
            if (i, j) in seen:
                continue
            seen.add((i, j))

            if i > 0 and area[i-1][j] == curr + 1:
                queue.append((i-1, j))
                rank[(i-1, j)] += rank[(i, j)]
            if j > 0 and area[i][j-1] == curr + 1:
                queue.append((i, j-1))
                rank[(i, j-1)] += rank[(i, j)]
            if i < m-1 and area[i+1][j] == curr + 1:
                queue.append((i+1, j))
                rank[(i+1, j)] += rank[(i, j)]
            if j < n-1 and area[i][j+1] == curr + 1:
                queue.append((i, j+1))
                rank[(i, j+1)] += rank[(i, j)]
        curr += 1
    
    rating = 0
    for i, j in queue:
        if (i, j) in seen:
            continue
        seen.add((i, j))
        rating += rank[(i, j)]
    
    print(rating)

part2()