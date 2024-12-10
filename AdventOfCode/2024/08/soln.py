import os

# paths
here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, 'input.txt')

# read input
with open(filepath, mode='r', encoding='utf8') as f:
    data = f.read()
rows = data.splitlines()

from collections import defaultdict

m = len(rows)
n = len(rows[0])
antennas = defaultdict(list)

for i in range(m):
    for j in range(n):
        ch = rows[i][j]
        if ch != '.':
            antennas[ch].append((i, j))

def part1():
    antinodes = set()
    for antenna_locs in antennas.values():
        n_antennas = len(antenna_locs)
        if n_antennas < 2:
            continue
        for a in range(n_antennas-1):
            for b in range(a+1, n_antennas):
                loc_a_i, loc_a_j = antenna_locs[a]
                loc_b_i, loc_b_j = antenna_locs[b]
                delta_i = loc_b_i - loc_a_i
                delta_j = loc_b_j - loc_a_j
                new_antenna_1 = (loc_b_i + delta_i, loc_b_j + delta_j)
                new_antenna_2 = (loc_a_i - delta_i, loc_a_j - delta_j)
                if (0 <= new_antenna_1[0] < m) and (0 <= new_antenna_1[1] < n):
                    antinodes.add(new_antenna_1)
                if (0 <= new_antenna_2[0] < m) and (0 <= new_antenna_2[1] < n):
                    antinodes.add(new_antenna_2)

    print(len(antinodes))

def part2():
    antinodes = set()

    def add_pos(pos1, pos2):
        return (pos1[0] + pos2[0], pos1[1] + pos2[1])
    
    def subtract_pos(pos1, pos2):
        return (pos1[0] - pos2[0], pos1[1] - pos2[1])
    
    def is_pos_valid(pos):
        return (0 <= pos[0] < m) and (0 <= pos[1] < n)

    def record_antinodes(start_pos, delta):
        prev_pos = subtract_pos(start_pos, delta)
        next_pos = add_pos(start_pos, delta)

        antinodes.add(start_pos)
        while is_pos_valid(prev_pos):
            antinodes.add(prev_pos)
            prev_pos = subtract_pos(prev_pos, delta)
        while is_pos_valid(next_pos):
            antinodes.add(next_pos)
            next_pos = add_pos(next_pos, delta)
        
    for antenna_locs in antennas.values():
        n_antennas = len(antenna_locs)
        if n_antennas < 2:
            continue
        for a in range(n_antennas-1):
            for b in range(a+1, n_antennas):
                delta_i = antenna_locs[b][0] - antenna_locs[a][0]
                delta_j = antenna_locs[b][1] - antenna_locs[a][1]
                record_antinodes(antenna_locs[a], (delta_i, delta_j))
    
    print(len(antinodes))

# part1()
part2()