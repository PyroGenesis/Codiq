import os

here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, 'input.txt')

with open(filepath, mode='r', encoding='utf8') as f:
    data = f.read()
lines = data.splitlines()

m = len(lines)
n = len(lines[0])

def part1():
    def findXmasesFrom(i, j):
        global lines, m, n
        found = 0

        for delta_i in (0, +1, -1):
            for delta_j in (0, +1, -1):
                if delta_i == 0 and delta_j == 0:
                    continue

                if not (0 <= i + delta_i*3 < m):
                    continue
                if not (0 <= j + delta_j*3 < n):
                    continue
                
                new_i, new_j = i + delta_i, j + delta_j
                if lines[new_i][new_j] != "M":
                    continue
                
                new_i += delta_i
                new_j += delta_j
                if lines[new_i][new_j] != "A":
                    continue
                
                new_i += delta_i
                new_j += delta_j
                if lines[new_i][new_j] != "S":
                    continue

                found += 1
        
        return found

    xmases = 0
    for i in range(m):
        for j in range(n):
            if lines[i][j] == 'X':
                xmases += findXmasesFrom(i, j)

    print(f"\n{xmases=}")

def part2():
    variations = set(["SM", "MS"])
    def IsXMasCenter(i, j) -> bool:
        global lines, m, n
        nonlocal variations

        if i == 0 or i == m-1 or j == n-1:
            return False
        
        diag1 = lines[i-1][j-1] + lines[i+1][j+1]
        diag2 = lines[i-1][j+1] + lines[i+1][j-1]
        return diag1 in variations and diag2 in variations

    x_mases = 0
    for i in range(m):
        for j in range(n):
            if lines[i][j] == 'A':
                if IsXMasCenter(i, j):
                    x_mases += 1

    print(f"\n{x_mases=}")

# part1()
part2()
