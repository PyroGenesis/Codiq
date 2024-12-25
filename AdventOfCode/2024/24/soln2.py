import os

here = os.path.dirname(os.path.abspath(__file__))


# read input
def read_data(filename: str):
    global here

    filepath = os.path.join(here, filename)
    with open(filepath, mode="r", encoding="utf8") as f:
        return f.read()


from dataclasses import dataclass


@dataclass
class Gate:
    operand1: "str | Gate"
    operand2: "str | Gate"
    op: str
    result: str

    def __post_init__(self):
        a = self.operand1 if isinstance(self.operand1, str) else self.operand1.result
        b = self.operand2 if isinstance(self.operand2, str) else self.operand2.result
        if a > b:
            self.operand1, self.operand2 = self.operand2, self.operand1

    def has_operand(self, name: str) -> bool:
        a = self.operand1 if isinstance(self.operand1, str) else self.operand1.result
        b = self.operand2 if isinstance(self.operand2, str) else self.operand2.result
        return name == a or name == b

    def swap_with(self, other: "Gate"):
        # since only result is used in eq and hash, we can freely swap the other attributes
        self.operand1, other.operand1 = other.operand1, self.operand1
        self.operand2, other.operand2 = other.operand2, self.operand2
        self.op, other.op = other.op, self.op

    def __repr__(self) -> str:
        # {self.result} :=
        return f"({repr(self.operand1)} {self.op} {repr(self.operand2)})"

    def __hash__(self) -> int:
        return hash(self.result)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Gate):
            return False
        return self.result == __value.result


def part2(filename: str):
    data = read_data(filename)
    nodes_data, gates_data = data.split("\n\n")

    nodes = {}
    all_resolved_nodes = {}
    for node_data in nodes_data.splitlines():
        node, val = node_data.split(": ")
        nodes[node] = int(val)
        all_resolved_nodes[node] = node

    gate_to_node = {}
    node_to_gate: dict[str, Gate] = {}

    gates_raw = set(gates_data.splitlines())
    while gates_raw:
        unresolved = set()
        for gate_raw in gates_raw:
            lhs, rhs = gate_raw.split(" -> ")
            operand1, op_raw, operand2 = lhs.split(" ")
            if operand1 not in all_resolved_nodes or operand2 not in all_resolved_nodes:
                unresolved.add(gate_raw)
                continue
            gate = Gate(all_resolved_nodes[operand1], all_resolved_nodes[operand2], op_raw, rhs)
            all_resolved_nodes[rhs] = gate
            node_to_gate[rhs] = gate
            gate_to_node[(gate.operand1, gate.operand2, gate.op)] = rhs

        gates_raw = unresolved

    # We are using the following rules to find discrepancies
    # there are two variants for a 1 bit adder
    # 1. Only one of (only one of current x,y is 1) or (carry is 1)
    #       (xi XOR yi) XOR (carry)
    # 2. (only one of current x,y is 1) or (both of x,y is 1 and carry is 1)
    #       (xi XOR yi) OR ((xi AND yi) AND (carry))
    # I believe this problem treats the second instance as wrong, so we only use rule 1
    # So the rules we get are:
    #   zi has to have an operand (xi XOR yi)
    #   zi has to have the operator XOR
    # So we swap based on what we find
    #   First, a swap is necessary if the z gate is not an xor OR
    #       the z gate does not have (xi xor yi) as an operand
    #   Then we decide what to swap
    #       If the z_gate does not have an XOR, swapping operands will not fix it.
    #           In this case, swap the entire z_gate with the one that has (xi xor yi) as an operand
    #       Otherwise, we need to swap our non-carry operand for the (xi xor yi) one
    # the carry is calculated like so
    # Either both of xi, yi is 1 or (only? one of xi, yi is 1 and c[i-1] is 1)
    #   ci = (xi AND y1) OR ((xi XOR yi) AND c[i-1])

    swapped = []
    for i in range(45):
        name = f"z{i:02}"
        z_gate = node_to_gate[name]
        # print(name, "->", z_gate)
        current_bit_xor_gate = gate_to_node[(f"x{i:02}", f"y{i:02}", "XOR")]
        if i == 0:
            assert current_bit_xor_gate == name
        else:
            if not z_gate.has_operand(current_bit_xor_gate) or z_gate.op != "XOR":
                # this is for if one of xi, y1 is 1
                # we have a mismatch
                # we need to find the gate which has (current_bit_xor_gate XOR something)
                swap_candidates = [
                    gate
                    for gate in node_to_gate.values()
                    if gate.has_operand(current_bit_xor_gate) and gate.op in ["XOR", "OR"]
                ]
                assert len(swap_candidates) == 1
                swap_candidate = swap_candidates[0]
                if z_gate.op != "XOR":
                    # we can swap the z with the gate having the XOR gate
                    z_gate.swap_with(swap_candidate)
                    swapped.append(name)
                    swapped.append(swap_candidate.result)
                else:
                    # then our gate has to be an xor
                    assert z_gate.op == "XOR"
                    # we need to find the non-carry to swap
                    # the carry one will have an and of last bits as top level operand
                    #   and an or to (an xor of last bits and carry of prev bits)
                    last_bit_and_gate = gate_to_node[(f"x{i-1:02}", f"y{i-1:02}", "AND")]
                    z_non_carry_operand = None
                    if isinstance(z_gate.operand1, Gate) and z_gate.operand1.has_operand(last_bit_and_gate):
                        z_non_carry_operand = z_gate.operand2
                    else:
                        assert isinstance(z_gate.operand2, Gate) and z_gate.operand2.has_operand(last_bit_and_gate)
                        z_non_carry_operand = z_gate.operand1
                    z_non_carry_operand.swap_with(node_to_gate[current_bit_xor_gate])
                    swapped.append(z_non_carry_operand.result)
                    swapped.append(current_bit_xor_gate)

    assert len(swapped) == 8
    swapped.sort()
    return ",".join(swapped)


print(part2("input.txt"))
