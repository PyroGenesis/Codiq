import os

here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, "input.txt")

# get text from file
with open(filepath, mode="r", encoding="utf8") as f:
    data = f.read()

rules, updates = data.split("\n\n")

from collections import defaultdict

befores = defaultdict(set)
for rule in rules.splitlines():
    a, b = map(int, rule.split("|"))
    befores[b].add(a)


def isUpdateValid(pages: list[int]) -> bool:
    for i in range(1, len(pages)):
        if pages[i - 1] not in befores[pages[i]]:
            return False
    return True


def part1():
    ans = 0
    for update in updates.splitlines():
        pages = list(map(int, update.split(",")))
        n = len(pages)
        assert n % 2 == 1

        if isUpdateValid(pages):
            ans += pages[n // 2]

    print(f"{ans=}")


def part2():
    ans = 0
    for update in updates.splitlines():
        pages = list(map(int, update.split(",")))
        n = len(pages)
        assert n % 2 == 1

        if not isUpdateValid(pages):
            for i in range(n - 1):
                for j in range(n - i - 1):
                    if pages[j] not in befores[pages[j + 1]]:
                        pages[j], pages[j + 1] = pages[j + 1], pages[j]

            ans += pages[n // 2]

    print(f"{ans=}")


# part1()
part2()
