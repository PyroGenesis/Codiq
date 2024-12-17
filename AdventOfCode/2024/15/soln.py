import os

# paths
here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, "input.txt")

# read input
with open(filepath, mode="r", encoding="utf8") as f:
    data = f.read()

warehouse, moves = data.split("\n\n")
moves = moves.replace("\n", "")
m, n = -1, -1


def get_warehouse_str():
    global warehouse
    return "\n".join(" ".join(warehouse[i][j] for j in range(n)) for i in range(m))


from copy import copy


class Point2D:
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def __copy__(self):
        return Point2D(self.i, self.j)

    def __hash__(self) -> int:
        return hash((self.i, self.j))

    def __eq__(self, __value: object) -> bool:
        assert isinstance(__value, Point2D)
        return self.i == __value.i and self.j == __value.j


def part1():
    global warehouse, m, n
    warehouse = [list(w) for w in warehouse.splitlines()]
    m, n = len(warehouse), len(warehouse[0])

    robot = None
    for i in range(m):
        for j in range(n):
            if warehouse[i][j] == "@":
                robot = Point2D(i, j)
    assert robot is not None

    def perform_move(di, dj):
        global warehouse
        nonlocal robot

        move_to = Point2D(robot.i + di, robot.j + dj)
        curr = copy(move_to)
        while (cell := warehouse[curr.i][curr.j]) != ".":
            if cell == "#":
                return
            curr.i += di
            curr.j += dj

        # move the box
        warehouse[curr.i][curr.j] = warehouse[move_to.i][move_to.j]
        # move the robot
        warehouse[move_to.i][move_to.j] = "@"
        warehouse[robot.i][robot.j] = "."
        robot = move_to

    for move in moves:
        args = None
        if move == "^":
            args = (-1, 0)
        if move == "<":
            args = (0, -1)
        if move == "v":
            args = (+1, 0)
        if move == ">":
            args = (0, +1)
        assert args is not None
        perform_move(*args)
        # print(move)
        # print(get_warehouse_str())
        # print()

    total_gps = 0
    for i in range(m):
        for j in range(n):
            if warehouse[i][j] == "O":
                total_gps += i * 100 + j

    print(total_gps)


# from collections import deque

expand_map = {
    "#": "##",
    "O": "[]",
    ".": "..",
    "@": "@.",
}  # fmt: skip


def part2():
    global warehouse, m, n

    warehouse = [[e for c in w for e in expand_map[c]] for w in warehouse.splitlines()]
    m, n = len(warehouse), len(warehouse[0])

    robot = None
    for i in range(m):
        for j in range(n):
            if warehouse[i][j] == "@":
                robot = Point2D(i, j)
    assert robot is not None

    def check_move(pos: Point2D, di: int, dj: int) -> bool:
        global warehouse

        if warehouse[pos.i][pos.j] == ".":
            return True
        if warehouse[pos.i][pos.j] == "#":
            return False

        success = check_move(Point2D(pos.i + di, pos.j + dj), di, dj)
        if di == 0 or not success:
            return success

        if warehouse[pos.i][pos.j] == "[":
            success = check_move(Point2D(pos.i + di, pos.j + 1), di, dj)
        elif warehouse[pos.i][pos.j] == "]":
            success = check_move(Point2D(pos.i + di, pos.j - 1), di, dj)
        return success

    def do_move(pos: Point2D, di: int, dj: int):
        global warehouse

        if warehouse[pos.i][pos.j] == ".":
            return

        do_move(Point2D(pos.i + di, pos.j + dj), di, dj)
        warehouse[pos.i + di][pos.j + dj] = warehouse[pos.i][pos.j]
        # have to set this to "." so the symbol before it can move up / down
        warehouse[pos.i][pos.j] = "."
        if di == 0:
            return
        assert dj == 0

        # have to check warehouse[pos.i + di][pos.j + dj] instead of warehouse[pos.i][pos.j]
        #   because warehouse[pos.i][pos.j] was already moved
        if warehouse[pos.i + di][pos.j + dj] == "[":
            # have to go right AND up/down because only right will put this into infinite recursion
            #   because left bracket will add a stack for right and vice-versa
            do_move(Point2D(pos.i + di, pos.j + 1), di, dj)
            warehouse[pos.i + di][pos.j + 1] = warehouse[pos.i][pos.j + 1]
            # have to set this to "." so the symbol before it can move up / down
            warehouse[pos.i][pos.j + 1] = "."
        elif warehouse[pos.i + di][pos.j + dj] == "]":
            # have to go left AND up/down because only left will put this into infinite recursion
            #   because left bracket will add a stack for right and vice-versa
            do_move(Point2D(pos.i + di, pos.j - 1), di, dj)
            warehouse[pos.i + di][pos.j - 1] = warehouse[pos.i][pos.j - 1]
            # have to set this to "." so the symbol before it can move up / down
            warehouse[pos.i][pos.j - 1] = "."

    for i, move in enumerate(moves):
        args = None
        if move == "^":
            args = (-1, 0)
        if move == "<":
            args = (0, -1)
        if move == "v":
            args = (+1, 0)
        if move == ">":
            args = (0, +1)
        assert args is not None

        # print(move)
        if check_move(robot, *args):
            do_move(robot, *args)
            robot.i += args[0]
            robot.j += args[1]
        # print(get_warehouse_str())
        # print()

    # print(get_warehouse_str())
    total_gps = 0
    for i in range(m):
        for j in range(n):
            if warehouse[i][j] == "[":
                total_gps += i * 100 + j

    print(total_gps)


part2()
