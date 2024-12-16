import os

here = os.path.dirname(os.path.abspath(__file__))


def read_data(filename: str):
    global here

    # paths
    filepath = os.path.join(here, filename)
    # read input
    with open(filepath, mode="r", encoding="utf8") as f:
        return f.read()


import re

pattern = re.compile(r"X.(\d+), Y.(\d+)")


class Point2D:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def offset_by(self, val: int):
        self.x += val
        self.y += val

    def __repr__(self):
        return f"Point({self.x},{self.y})"

    def __add__(self, other):
        assert isinstance(other, Point2D)
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        assert isinstance(other, Point2D)
        return Point2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        assert isinstance(other, int)
        return Point2D(self.x * other, self.y * 100)

    def __lt__(self, other):
        assert isinstance(other, Point2D)
        return self.x < other.x or self.y < other.y

    def __gt__(self, other):
        assert isinstance(other, Point2D)
        return self.x > other.x or self.y > other.y

    def __eq__(self, other):
        assert isinstance(other, Point2D)
        return self.x == other.x and self.y == other.y


def part1(filename: str):
    data = read_data(filename)

    tokens = 0

    for machine_desc in data.split("\n\n"):
        button_a_desc, button_b_desc, prize_desc = machine_desc.splitlines()
        button_a = Point2D(*(int(x) for x in pattern.search(button_a_desc).groups()))
        button_b = Point2D(*(int(x) for x in pattern.search(button_b_desc).groups()))
        prize = Point2D(*(int(x) for x in pattern.search(prize_desc).groups()))
        # print(button_a, button_b, prize)

        # 300 for 100 A presses
        # 100 for 100 B presses
        # +1
        min_tokens = 401

        a_presses = 0
        pos = button_b * 100
        for b_presses in range(100, -1, -1):
            while pos < prize:
                a_presses += 1
                pos += button_a
            while pos > prize:
                a_presses -= 1
                pos -= button_a
            if pos == prize:
                min_tokens = min(min_tokens, a_presses * 3 + b_presses)
            pos -= button_b

        tokens += min_tokens if min_tokens < 401 else 0

    return tokens


def part2(filename: str):
    data = read_data(filename)

    tokens = 0

    for machine_desc in data.split("\n\n"):
        button_a_desc, button_b_desc, prize_desc = machine_desc.splitlines()
        button_a = Point2D(*(int(x) for x in pattern.search(button_a_desc).groups()))
        button_b = Point2D(*(int(x) for x in pattern.search(button_b_desc).groups()))
        prize = Point2D(*(int(x) for x in pattern.search(prize_desc).groups()))
        # print(button_a, button_b, prize)

        prize.offset_by(10000000000000)

        b_presses = (button_a.y * prize.x - button_a.x * prize.y) / (button_a.y * button_b.x - button_a.x * button_b.y)
        if not b_presses.is_integer():
            continue
        a_presses = (prize.x - button_b.x * b_presses) / button_a.x
        if not a_presses.is_integer():
            continue

        tokens += a_presses * 3 + b_presses

    return int(tokens)


assert part1("sample.txt") == 480
print(part2("input.txt"))
# print(part2("input.txt"))
