import os

here = os.path.dirname(os.path.abspath(__file__))


def read_data(filename: str):
    global here

    # paths
    filepath = os.path.join(here, filename)
    # read input
    with open(filepath, mode="r", encoding="utf8") as f:
        return f.read()


from dataclasses import dataclass
from itertools import islice
from typing import Iterable, TypeVar, Generator

T = TypeVar("T")


def batched(iterable: Iterable[T], n: int) -> Generator[tuple[T, ...], None, None]:
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


@dataclass
class ProgramState:
    A: int = 0
    B: int = 0
    C: int = 0

    ip: int = 0
    program: list[int] = None

    def read_instruction(self) -> tuple[int, int] | None:
        if self.ip == len(self.program):
            return None
        ins = (self.program[self.ip], self.program[self.ip + 1])
        self.ip += 2
        return ins

    def combo_op(self, operand: int):
        if operand < 4:
            return operand
        return (self.A, self.B, self.C)[operand - 4]


def get_state(filename: str):
    data = read_data(filename)
    lines = data.splitlines()

    state = ProgramState()
    state.A = int(lines[0][12:])
    state.B = int(lines[1][12:])
    state.C = int(lines[2][12:])

    state.program = [int(x) for x in lines[4][9:].split(",")]
    return state


def part1(state: ProgramState):
    output = []

    while (ins := state.read_instruction()) is not None:
        opcode, operand = ins
        if opcode in (0, 6, 7):
            # adv, bdv, cdv
            res = state.A // (2 ** state.combo_op(operand))
            if opcode == 0:
                state.A = res
            elif opcode == 6:
                state.B = res
            else:
                state.C = res
        elif opcode in (1, 4):
            # bxl, bxc
            state.B = state.B ^ (operand if opcode == 1 else state.C)
        elif opcode in (2, 5):
            # bst, out
            res = state.combo_op(operand) % 8
            if opcode == 2:
                state.B = res
            else:
                output.append(str(res))
        elif opcode == 3:
            # jnz
            if state.A != 0:
                state.ip = operand

    return ",".join(output), state


t1 = ProgramState(C=9, program=[2, 6])
assert part1(t1)[1].B == 1
t2 = ProgramState(A=10, program=[5, 0, 5, 1, 5, 4])
assert part1(t2)[0] == "0,1,2"
t3 = ProgramState(A=2024, program=[0, 1, 5, 4, 3, 0])
t3_res = part1(t3)
assert t3_res[0] == "4,2,5,6,7,7,7,7,3,1,0"
assert t3_res[1].A == 0
t4 = ProgramState(B=29, program=[1, 7])
assert part1(t4)[1].B == 26
t5 = ProgramState(B=2024, C=43690, program=[4, 0])
assert part1(t5)[1].B == 44354

sample = part1(get_state("sample.txt"))
assert sample[0] == "4,6,3,5,6,3,5,2,1,0"

print("Part 1:", part1(get_state("input.txt"))[0])


def part2(state: ProgramState):
    A = 0
    for o in reversed(state.program):
        A <<= 3
        # x = 1
        while True:
            state.A = A
            state.B = 0
            state.C = 0
            state.ip = 0
            if int(part1(state)[0][0]) == o:
                if A == 0:
                    A += 1
                break
            A += 1
    return A


# state = get_state("sample2.txt")
# for A in range(500):
#     state.A = A
#     state.B = 0
#     state.C = 0
#     state.ip = 0
#     print(A, part1(state)[0])

assert part2(get_state("sample2.txt")) == 117440
print("Part 2:", part2(get_state("input.txt")))

print("All Done!")
