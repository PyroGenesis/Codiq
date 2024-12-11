import os

# paths
here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, 'input.txt')

# read input
with open(filepath, mode='r', encoding='utf8') as f:
    data = f.read()

from collections import deque
import math

def count_digits(x: int):
    if x < 10:
        return 1
    return math.ceil(math.log10(x+1))

def split_stone(x: int):
    n = count_digits(x)
    divider = 10**(n//2)
    return x // divider, x % divider

def part1():
    queue = deque(int(stone) for stone in data.strip().split(" "))
    for i in range(75):
        n = len(queue)
        for _ in range(n):
            stone = queue.popleft()
            if stone == 0:
                queue.append(1)
            elif count_digits(stone) % 2 == 0:
                stone1, stone2 = split_stone(stone)
                queue.append(stone1)
                queue.append(stone2)
            else:
                queue.append(stone * 2024)
        print(f"{i+1}: {len(queue)}")
    print(len(queue))

def part2():    
    memo = {}
    def iterate_stone(stone, blinks):
        if blinks == 0:
            return 1
        if (stone, blinks) in memo:
            return memo[(stone, blinks)]
        
        if stone == 0:
            res = iterate_stone(1, blinks-1)
        elif count_digits(stone) % 2 == 0:
            stone1, stone2 = split_stone(stone)
            res = iterate_stone(stone1, blinks-1) + iterate_stone(stone2, blinks-1)
        else:
            res = iterate_stone(stone*2024, blinks-1)
        
        memo[(stone, blinks)] = res
        return res
    
    print(sum(iterate_stone(int(stone), 75) for stone in data.strip().split(" ")))

# part1()
part2()