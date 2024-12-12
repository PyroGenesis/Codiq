import os
from collections import defaultdict

# paths
here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, "input.txt")

# read input
with open(filepath, mode="r", encoding="utf8") as f:
    data = f.read()
# setup input vars
garden = data.splitlines()
m, n = len(garden), len(garden[0])


def part1():
    visited = set()

    def calcFenceCostFrom(i, j):
        """Calculates the fencing cost of the region starting from coords (i, j)"""
        global garden, m, n

        plant_type = garden[i][j]
        stack = [(i, j)]
        area, perimeter = 0, 0

        while stack:
            ci, cj = stack.pop()
            if (ci, cj) in visited:
                continue
            visited.add((ci, cj))

            # add cell to area
            area += 1

            # check top cell
            if ci > 0 and garden[ci - 1][cj] == plant_type:
                stack.append((ci - 1, cj))
            else:
                # if no top cell, add the edge to perimeter
                perimeter += 1

            # check left cell
            if cj > 0 and garden[ci][cj - 1] == plant_type:
                stack.append((ci, cj - 1))
            else:
                # if no left cell, add the edge to perimeter
                perimeter += 1

            # check bottom cell
            if ci < m - 1 and garden[ci + 1][cj] == plant_type:
                stack.append((ci + 1, cj))
            else:
                # if no bottom cell, add the edge to perimeter
                perimeter += 1

            # check right cell
            if cj < n - 1 and garden[ci][cj + 1] == plant_type:
                stack.append((ci, cj + 1))
            else:
                # if no right cell, add the edge to perimeter
                perimeter += 1

        return area * perimeter

    # calculate fencing cost for every region
    fencing_cost = 0
    for i in range(m):
        for j in range(n):
            if (i, j) in visited:
                continue
            fencing_cost += calcFenceCostFrom(i, j)

    print(fencing_cost)


def part2():
    visited = set()

    def calcFenceCostFrom(i, j):
        """Calculates the fencing cost of the region starting from coords (i, j)"""
        global garden, m, n

        plant_type = garden[i][j]
        stack = [(i, j)]
        area = 0

        # keep track of all distinct, non-intersecting horizontal and vertical segments
        segments = {
            "H": defaultdict(set),
            "V": defaultdict(set)
        }  # fmt: skip

        while stack:
            ci, cj = stack.pop()
            if (ci, cj) in visited:
                continue
            visited.add((ci, cj))

            # add cell to area
            area += 1

            # check top cell
            if ci > 0 and garden[ci - 1][cj] == plant_type:
                stack.append((ci - 1, cj))
            else:
                # record edge segment
                ei = ci - 0.25  # push out the horizontal segment
                segment_set = segments["H"][ei]
                ej_from, ej_to = cj - 0.5, cj + 0.5  # extend the segment to connect with neighbors
                merge_segments(segment_set, ej_from, ej_to)  # merge with current segment set

            # check left cell
            if cj > 0 and garden[ci][cj - 1] == plant_type:
                stack.append((ci, cj - 1))
            else:
                # record edge segment
                ej = cj - 0.25  # push out the vertical segment
                segment_set = segments["V"][ej]
                ei_from, ei_to = ci - 0.5, ci + 0.5  # extend the segment to connect with neighbors
                merge_segments(segment_set, ei_from, ei_to)  # merge with current segment set

            # check bottom cell
            if ci < m - 1 and garden[ci + 1][cj] == plant_type:
                stack.append((ci + 1, cj))
            else:
                # record edge segment
                ei = ci + 0.25  # push out the horizontal segment
                segment_set = segments["H"][ei]
                ej_from, ej_to = cj - 0.5, cj + 0.5  # extend the segment to connect with neighbors
                merge_segments(segment_set, ej_from, ej_to)  # merge with current segment set

            # check right cell
            if cj < n - 1 and garden[ci][cj + 1] == plant_type:
                stack.append((ci, cj + 1))
            else:
                # record edge segment
                ej = cj + 0.25  # push out the vertical segment
                segment_set = segments["V"][ej]
                ei_from, ei_to = ci - 0.5, ci + 0.5  # extend the segment to connect with neighbors
                merge_segments(segment_set, ei_from, ei_to)  # merge with current segment set

        # number of distinct segments == number of sides
        sides = sum(len(segment_set) for seg_dict in segments.values() for segment_set in seg_dict.values())
        return area * sides

    def merge_segments(segment_set: set, idx_from: int, idx_to: int):
        """Merge segment into existing segment set"""
        # find any overlapping / intersecting segments before and after current
        former_segment, latter_segment = None, None
        for s_from, s_to in segment_set:
            if s_from < idx_from and s_to >= idx_from:
                former_segment = (s_from, s_to)
            if s_to > idx_to and s_from <= idx_to:
                latter_segment = (s_from, s_to)

        if former_segment is None and latter_segment is None:
            # there is no overlapping segment
            segment_set.add((idx_from, idx_to))
        elif former_segment == latter_segment:
            # the overlap segment contains our full segment
            pass
        elif former_segment is None:
            # there is a latter segment only
            segment_set.remove(latter_segment)
            segment_set.add((idx_from, latter_segment[1]))
        elif latter_segment is None:
            # there is a former segment only
            segment_set.remove(former_segment)
            segment_set.add((former_segment[0], idx_to))
        else:
            # both are disconnected segments
            segment_set.remove(former_segment)
            segment_set.remove(latter_segment)
            segment_set.add((former_segment[0], latter_segment[1]))

    fencing_cost = 0
    for i in range(m):
        for j in range(n):
            if (i, j) in visited:
                continue
            fencing_cost += calcFenceCostFrom(i, j)

    print(fencing_cost)


part1()
part2()
