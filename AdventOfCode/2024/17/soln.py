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


def get_state(filename: str, cls: type):
    data = read_data(filename)
    lines = data.splitlines()

    state = cls()
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

sample = part1(get_state("sample.txt", ProgramState))
assert sample[0] == "4,6,3,5,6,3,5,2,1,0"

# print(part1(get_state("input.txt"))[0])

from copy import copy
import math
import sys


@dataclass
class ProgramStateR(ProgramState):
    A_high: int = 0
    B_high: int = sys.maxsize
    C_high: int = sys.maxsize

    def combo_op(self, operand: int) -> list[int]:
        if operand < 4:
            return [operand, operand]
        return ([self.A, self.A_high], [self.B, self.B_high], [self.C, self.C_high])[operand - 4]


def reverse_program(program: list[int]):
    assert program[-2] == 3
    assert program[-1] == 0

    n = len(program)

    i = 0
    inss = []
    while i < n:
        inss.append((program[i], program[i + 1]))
        i += 2
    jmp = inss.pop()
    flattened_rev_ins = [x for ins in reversed(inss) for x in ins]

    rev = []
    for _ in range(n):
        rev.extend(flattened_rev_ins)
        rev.extend(jmp)
    return rev


def part2(state: ProgramStateR):
    expected_output = copy(state.program)

    # reverse program
    state.A = 0
    state.B = 0
    state.C = 0
    state.program = reverse_program(state.program)

    while (ins := state.read_instruction()) is not None:
        opcode, operand = ins
        if opcode in (0, 6, 7):
            # reverse adv, bdv, cdv
            assert operand < 4, "Reverse adv for ranged operand not implemented"
            rev = None
            if opcode == 0:
                rev = [state.A, state.A_high]
            elif opcode == 6:
                rev = [state.B, state.B_high]
            else:
                rev = [state.C, state.C_high]
            denominator = 2**operand
            state.A = rev[0] * denominator
            state.A_high = (rev[1] * denominator) + (denominator - 1)

        elif opcode in (1, 4):
            # reverse bxl, bxc
            b_range = (state.B, state.B_high)
            other_range = (operand, operand) if opcode == 1 else (state.C, state.C_high)
            if (b_range[1] - b_range[0]) > (other_range[1] - other_range[0]):
                # swap to have b_range as the smallest
                b_range, other_range = other_range, b_range

            new_range = [sys.maxsize, 0]

            for b in range(b_range[0], b_range[1] + 1):
                for other in range(other_range[0], other_range[1] + 1):
                    if other & b == b:
                        new_range[0] = min(new_range[0], other ^ b)
                        break
                for other in range(other_range[1], other_range[0] - 1, -1):
                    if other & b == 0:
                        new_range[1] = max(new_range[1], other ^ b)
                        break

            state.B, state.B_high = new_range

        elif opcode == 2:
            # bst, out
            res = state.combo_op(operand) % 8
            # if opcode == 2:
            #     state.B = res
            # else:
            #     output.append(str(res))

        elif opcode == 5:
            # reverse out
            res = expected_output.pop()
            if operand < 4:
                assert res == operand
                continue

            rev = state.combo_op(operand)
            for x in range(rev[0], rev[1] + 1):
                if x % 8 == res:
                    if operand == 4:
                        state.A = x
                        state.A_high = x
                    elif operand == 5:
                        state.B = x
                        state.B_high = x
                    else:
                        state.C = x
                        state.C_high = x
                    break
            else:
                assert False

        elif opcode == 3:
            # reverse jnz
            state.A = max(state.A, 1)

    return state


# assert part2(get_state("sample2.txt", ProgramStateR)).A == 117440
print(part2(get_state("input.txt", ProgramStateR)).A)
print("All Done!")
