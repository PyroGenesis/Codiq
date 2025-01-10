import os

here = os.path.dirname(os.path.abspath(__file__))


# read input
def read_data(filename: str):
    global here

    filepath = os.path.join(here, filename)
    with open(filepath, mode="r", encoding="utf8") as f:
        return f.read()


from dataclasses import dataclass
from operator import and_, or_, xor
from typing import Callable


@dataclass(frozen=True)
class Gate:
    operand1: str
    operand2: str
    op: Callable
    result: str


def part1(filename: str):
    data = read_data(filename)
    initial_data, gates_data = data.split("\n\n")

    nodes = {}
    for node_data in initial_data.splitlines():
        node, val = node_data.split(": ")
        val = int(val)
        nodes[node] = val

    operator_map = {
        "AND": and_,
        "OR": or_,
        "XOR": xor,
    }  # fmt: skip

    gates: set[Gate] = set()
    for gate_data in gates_data.splitlines():
        lhs, rhs = gate_data.split(" -> ")
        operand1, op, operand2 = lhs.split(" ")
        #  be mindful of the arguments order here
        gates.add(Gate(operand1, operand2, operator_map[op], rhs))

    while gates:
        unresolved = set()
        for gate in gates:
            if gate.operand1 not in nodes or gate.operand2 not in nodes:
                unresolved.add(gate)
                continue
            nodes[gate.result] = gate.op(nodes[gate.operand1], nodes[gate.operand2])
        gates = unresolved

    ans = 0
    i = 0
    while True:
        name = f"z{i:02}"
        if name not in nodes:
            break
        if nodes[name] == 1:
            ans |= 1 << i
        i += 1

    return ans


assert part1("sample1.txt") == 4
assert part1("sample2.txt") == 2024
print(part1("input.txt"))
