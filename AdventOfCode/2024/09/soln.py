import os

# paths
here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, "input.txt")

# read input
with open(filepath, mode="r", encoding="utf8") as f:
    data = f.read()


def part1():
    disk = [int(x) for x in data.strip()]
    n = len(disk)
    checksum = 0
    block = 0

    i = 0
    # j should always be on a valid file block
    j = n - 1 if n % 2 == 1 else n - 2
    while j > 0 and disk[j] == 0:
        j -= 2

    while i <= j:
        if i % 2 == 0:
            # this is file block
            id = i // 2
            for _ in range(disk[i]):
                checksum += block * id
                block += 1
            i += 1

        elif disk[i] > 0:
            # actual space block
            id = j // 2
            checksum += block * id
            block += 1
            disk[i] -= 1
            disk[j] -= 1
            if disk[j] == 0:
                j -= 2

        else:
            # empty space block
            i += 1

    print(checksum)


class FileNode:
    id: int
    size: int
    _prev_node: "FileNode | None"
    _next_node: "FileNode | None"

    def __init__(self, id: int, size: int):
        self.id = id
        self.size = size
        self._prev_node = None
        self._next_node = None

    @property
    def is_file_node(self):
        return self.id >= 0

    @property
    def is_space_node(self):
        return self.id < 0

    @property
    def next_node(self):
        return self._next_node

    @next_node.setter
    def next_node(self, other: "FileNode | None"):
        # if a <=> c, and connect a to b, self is a
        assert other is not None, "next_node(): other is None"
        # b -> c
        other._next_node = self._next_node
        if other._next_node is not None:
            # b <- c
            other._next_node._prev_node = other
        # a <- b
        other._prev_node = self
        # a -> b
        self._next_node = other

    @property
    def prev_node(self):
        return self._prev_node

    @prev_node.setter
    def prev_node(self, other: "FileNode | None"):
        # if a <=> c, and connect b to c, self is c
        assert other is not None, "prev_node(): other is None"
        # a <- b
        other._prev_node = self._prev_node
        if other._prev_node is not None:
            # a -> b
            other._prev_node._next_node = other
        # b -> c
        other._next_node = self
        # b <- c
        self._prev_node = other

    def detach(self):
        if self._prev_node:
            self._prev_node._next_node = self._next_node
        if self.next_node:
            self._next_node._prev_node = self._prev_node
        self._prev_node = None
        self._next_node = None

    def __repr__(self):
        if self.id < 0:
            this = f"S({self.size})"
        else:
            this = f"F({self.id},{self.size})"
        if self._next_node:
            this += " -> " + repr(self._next_node)
        return this


def part2():
    _dummy = FileNode(-1, 0)
    node = _dummy
    for i, ch in enumerate(data.strip()):
        size = int(ch)
        if i % 2 == 0:
            # file
            node.next_node = FileNode(i // 2, size)
        else:
            # space
            node.next_node = FileNode(-(i + 1), size)
        node = node.next_node
    head = _dummy.next_node
    _dummy.detach()
    tail = node

    # # first space is immediately after first node
    # space_node = head.next_node
    # while space_node:
    #     while space_node and (space_node.id >= 0 or space_node.size < 1):
    #         space_node = space_node.next_node
    #     if not space_node:
    #         break

    #     file_node = tail
    #     # try to find a file node that is smaller than space node
    #     while file_node and (file_node.id < 0 or file_node.size > space_node.size):
    #         if file_node.id == space_node.id:
    #             file_node = None
    #         else:
    #             file_node = file_node.prev_node
    #     if not file_node:
    #         break

    #     if tail == file_node:
    #         tail = file_node.prev_node
    #     file_node.detach()
    #     space_node.prev_node = file_node
    #     space_node.size -= file_node.size

    file_node = tail if tail.is_file_node else tail.prev_node
    while file_node and file_node.prev_node:
        _temp_prev = file_node.prev_node

        space_node = head.next_node
        while space_node and (space_node.is_file_node or space_node.size < file_node.size):
            if space_node.id == file_node.id:
                # there is no satisfyable space
                space_node = None
            else:
                space_node = space_node.next_node

        if space_node:
            if _temp_prev:
                _temp_prev.size += file_node.size
            file_node.detach()
            space_node.prev_node = file_node
            space_node.size -= file_node.size

        file_node = _temp_prev
        while file_node and file_node.is_space_node:
            file_node = file_node.prev_node

    checksum = 0
    block = 0
    node = head
    while node:
        if node.id > 0:
            # Sn    = n/2 [2a + (n-1)d]
            #   Since d == 1
            #       = n/2 [2a + (n-1)]
            #       = na + n(n-1)/2
            checksum += node.id * (node.size * block + (node.size * (node.size - 1) // 2))
        block += node.size
        node = node.next_node

    print(checksum)


# part1()
part2()
