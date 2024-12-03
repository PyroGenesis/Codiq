import os

here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, 'input.txt')

# yield lines from a file one by one
def readlines(filepath: str):
    with open(filepath, mode='r', encoding='utf8') as f:
        while line := f.readline():
            yield line

# yield nums from a line one by one
def splitnums(line: str):
    for s in line.split(' '):
        yield int(s)

def part1():
    safe_reports = 0

    for report in readlines(filepath):
        direction = None
        prev_level = None
        for level in splitnums(report):
            if prev_level is None:
                prev_level = level
                continue
            if direction is None:
                direction = +1 if prev_level < level else -1
            
            diff = level - prev_level
            if not (1 <= (diff * direction) <= 3):
                break
            prev_level = level
        else:
            # no-break
            safe_reports += 1

    print(f"\nPart 1 {safe_reports=}", flush=True)

def part2():
    from copy import copy
    safe_reports = 0

    def getUnsafeIdx(levels: list[int]) -> int | None:
        direction = None
        for i in range(1, len(levels)):
            if direction is None:
                direction = +1 if levels[i-1] < levels[i] else -1
            diff = levels[i] - levels[i-1]
            if not (1 <= (diff * direction) <= 3):
                return i
        return None

    for report in readlines(filepath):
        levels = list(splitnums(report))

        if (bad_idx := getUnsafeIdx(levels)) is None:
            safe_reports += 1
            continue

        new_levels = copy(levels)
        new_levels.pop(bad_idx)
        if (bad_idx := getUnsafeIdx(new_levels)) is None:            
            safe_reports += 1
            continue

        new_levels = copy(levels)
        new_levels.pop(bad_idx-1)
        if (bad_idx := getUnsafeIdx(new_levels)) is None:
            safe_reports += 1
            continue
        
        if bad_idx <= 1:
            continue
        new_levels = copy(levels)
        new_levels.pop(bad_idx-2)
        if (bad_idx := getUnsafeIdx(new_levels)) is None:
            safe_reports += 1
        else:
            pass

    print(f"\nPart 2 {safe_reports=}", flush=True)

part1()
part2()