import os

here = os.path.dirname(os.path.abspath(__file__))


# read input
def read_data(filename: str):
    global here

    filepath = os.path.join(here, filename)
    with open(filepath, mode="r", encoding="utf8") as f:
        return f.read()


from collections import deque, defaultdict
from dataclasses import dataclass

# numpad_graph = {
#     -1: [0, 3],
#     0: [-1, 2],
#     1: [2, 4],
#     2: [0, 1, 3, 5],
#     3: [-1, 2, 6],
#     4: [1, 5, 7],
#     5: [2, 4, 6, 8],
#     6: [3, 5, 9],
#     7: [4, 8],
#     8: [5, 7, 9],
#     9: [6, 8],
# }


@dataclass(frozen=True)
class Point2D:
    i: int
    j: int


# up right down left
DIRECTIONS = [(-1, 0), (0, +1), (1, 0), (0, -1)]
DIRECTION_PAD = ["^", ">", "v", "<"]

numpad_remote = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [None, '0', 'A']
]  # fmt: skip

directional_remote = [
    [None, "^", "A"],
    ["<", "v", ">"],
]  # fmt: skip

RemoteType = list[list[str | None]]
MoveMapType = dict[str, dict[str, list[str]]]


def build_move_map(remote_grid: RemoteType) -> MoveMapType:
    m, n = len(remote_grid), len(remote_grid[0])
    mapping = {}
    symbols = set(sym for row in remote_grid for sym in row if sym is not None)
    for i in range(m):
        for j in range(n):
            if remote_grid[i][j] is None:
                continue
            current_sym_map = defaultdict(list)
            queue = deque([(Point2D(i, j), [])])
            dests_visited = set()
            while len(dests_visited) < len(symbols):
                nq = len(queue)
                dests_current = set()
                for _ in range(nq):
                    point, moves = queue.popleft()
                    dest_sym = remote_grid[point.i][point.j]
                    if dest_sym not in dests_visited:
                        dests_current.add(dest_sym)
                        current_sym_map[dest_sym].append("".join(moves) + "A")

                    for (di, dj), move in zip(DIRECTIONS, DIRECTION_PAD, strict=True):
                        new_point = Point2D(point.i + di, point.j + dj)
                        if not (0 <= new_point.i < m) or not (0 <= new_point.j < n):
                            continue
                        if remote_grid[new_point.i][new_point.j] is None:
                            continue
                        queue.append((new_point, moves + [move]))
                dests_visited.update(dests_current)
            mapping[remote_grid[i][j]] = current_sym_map
    return mapping


numpad_move_map = build_move_map(numpad_remote)
directional_move_map = build_move_map(directional_remote)


def get_button_sequences(move_map: MoveMapType, code: str):
    sequences = deque([""])
    curr = "A"
    for ch in code:
        new_moves = move_map[curr][ch]
        ns = len(sequences)
        for _ in range(ns):
            old_seq = sequences.popleft()
            for new_moveset in new_moves:
                sequences.append(old_seq + new_moveset)
        curr = ch
    return sequences


from tqdm import tqdm, trange


def get_sequence_lens(code: str, intermediate_robots=2):
    robot1_moves = get_button_sequences(numpad_move_map, code)
    optimal_lens = [min(len(m) for m in robot1_moves)]
    robot_moves = [m for m in robot1_moves if len(m) == optimal_lens[-1]]

    for _ in trange(intermediate_robots, desc="Intermediate", leave=False):
        next_robot_moves = []
        for rm in tqdm(robot_moves, desc="Move", leave=False):
            seqs = get_button_sequences(directional_move_map, rm)
            next_robot_moves.extend(seqs)
        optimal_lens.append(min(len(m) for m in next_robot_moves))
        robot_moves = [m for m in next_robot_moves if len(m) == optimal_lens[-1]]

    return optimal_lens


def get_code_complexity(code: str, intermediate_robots=2):
    lens = get_sequence_lens(code, intermediate_robots)
    return lens[-1] * int(code[:-1])


l1_029A, l2_029A, l3_029A = get_sequence_lens("029A")
assert l1_029A == len("<A^A>^^AvvvA")
assert l2_029A == len("v<<A>>^A<A>AvA<^AA>A<vAAA>^A")
assert l3_029A == len("<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A")

assert get_code_complexity("029A") == 68 * 29


def soln(filename: str, intermediate_robots=2):
    data = read_data(filename)
    complexity = 0
    for code in tqdm(data.splitlines(), desc=filename + " Code"):
        complexity += get_code_complexity(code, intermediate_robots)
    return complexity


assert soln("sample.txt") == 126384
assert soln("input.txt") == 128962

# print(soln("input.txt", 25))

print("All done!")
