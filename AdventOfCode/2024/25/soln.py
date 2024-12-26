import os

here = os.path.dirname(os.path.abspath(__file__))


# read input
def read_data(filename: str):
    global here

    filepath = os.path.join(here, filename)
    with open(filepath, mode="r", encoding="utf8") as f:
        return f.read()


def soln(filename: str):
    data = read_data(filename)
    schematics = data.split("\n\n")

    locks, keys = [], []
    for schematic in schematics:
        rows = schematic.splitlines()
        heights = [0] * 5
        for i in range(1, len(rows) - 1):
            for j in range(5):
                if rows[i][j] == "#":
                    heights[j] += 1

        if schematic.startswith("#####"):
            locks.append(heights)
        else:
            keys.append(heights)

    fit = 0
    for lock in locks:
        for key in keys:
            for i in range(5):
                if lock[i] + key[i] > 5:
                    break
            else:
                # no-break
                fit += 1

    return fit


print(soln("input.txt"))
