import os

here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, 'input.txt')

# get text from file
def readfile():
    global filepath
    with open(filepath, mode='r', encoding='utf8') as f:
        return f.read()

import re

# pattern that matches mul(a,b) calls
# re.DOTALL here made no difference here because mu\nl wouldn't match anyway
mul_pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)", re.DOTALL)

def part1():
    total = 0
    # findall will return list of tuples of groups
    #   [(a1, b1), (a2, b2) ...]
    for a, b in mul_pattern.findall(readfile()):
        total += int(a) * int(b)

    print(f"\n{total=}", flush=True)

# pattern that matches the don't() sections (to be removed from consideration)
# either match a don't()-do() pair, or match the last don't() till the end
# re.DOTALL is necessary here as a don't() on one line is not auto disabled on the next (learnt it the hard way)
conditional_pattern = re.compile(r"(?:don't\(\).*?do\(\))|(?:don't\(\).*)", re.DOTALL)

def part2():
    total = 0
    # remove the don't() sections from the input
    corrected_line = conditional_pattern.sub("--", readfile())
    # findall will return list of tuples of groups
    #   [(a1, b1), (a2, b2) ...]
    for a, b in mul_pattern.findall(corrected_line):
        total += int(a) * int(b)

    print(f"\n{total=}", flush=True)

part1()
part2()
