import os

here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, 'input.txt')

def part1():
    list_a = []
    list_b = []

    with open(filepath, mode='r', encoding='utf8') as f:
        for line in f.readlines():
            a, b = map(int, line.split("   "))
            list_a.append(a)
            list_b.append(b)

    list_a.sort()
    list_b.sort()

    total_diff = 0
    for a, b in zip(list_a, list_b, strict=True):
        total_diff += abs(a - b)

    print(f"{total_diff=}", flush=True)

def part2():
    from collections import Counter
    counter_a = Counter()
    counter_b = Counter()

    with open(filepath, mode='r', encoding='utf8') as f:
        for line in f.readlines():
            a, b = map(int, line.split("   "))
            counter_a[a] += 1
            counter_b[b] += 1
    
    similarity_score = 0
    for num in counter_a:
        similarity_score += counter_a[num] * counter_b[num] * num
    
    print(f"{similarity_score=}", flush=True)

part2()
    