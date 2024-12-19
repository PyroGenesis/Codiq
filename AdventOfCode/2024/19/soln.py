import os

here = os.path.dirname(os.path.abspath(__file__))


# read input
def read_data(filename: str):
    global here

    filepath = os.path.join(here, filename)
    with open(filepath, mode="r", encoding="utf8") as f:
        return f.read()


class Trie:
    class TrieNode:
        def __init__(self) -> None:
            self.children = {}  # connections to other TrieNode
            self.end = False  # whether this node indicates an end of a pattern

    def __init__(self) -> None:
        self.root = Trie.TrieNode()

    def add(self, pattern: str):
        node = self.root
        # add the pattern to the trie, one character at a time
        for color in pattern:
            if color not in node.children:
                node.children[color] = Trie.TrieNode()
            node = node.children[color]
        # mark the node as the end of a pattern
        node.end = True


def soln(filename: str):
    data = read_data(filename)
    patterns, design_data = data.split("\n\n")

    # build the Trie
    trie = Trie()
    for pattern in patterns.split(", "):
        trie.add(pattern)

    designs = design_data.splitlines()

    # saves the design / sub-design -> number of component pattern combinations
    memo = {}

    def backtrack(design: str):
        nonlocal trie

        # if design is empty, we have successfully
        #   matched the caller design / sub-design
        if design == "":
            return 1
        # use memo if available
        if design in memo:
            return memo[design]

        # start matching a new pattern from here
        node = trie.root
        # number of pattern combinations for this design
        pattern_comb_count = 0
        for i in range(len(design)):
            # if design[0 : i+1] is not a valid pattern,
            #   we are done matching characters
            if design[i] not in node.children:
                break
            # move along the pattern
            node = node.children[design[i]]
            # we reached the end of a pattern
            if node.end:
                # get the pattern combinations count for the rest of the design / sub-design
                # all of them count for this design / sub-design
                pattern_comb_count += backtrack(design[i + 1 :])

        # save the pattern combinations count for this design / sub-design
        memo[design] = pattern_comb_count
        return pattern_comb_count

    pattern_comb_counts = []
    for design in designs:
        pattern_comb_counts.append(backtrack(design))
    return pattern_comb_counts


assert sum(1 for dc in soln("sample.txt") if dc > 0) == 6
print("Part 1:", sum(1 for dc in soln("input.txt") if dc > 0))

assert sum(soln("sample.txt")) == 16
print("Part 2:", sum(soln("input.txt")))
