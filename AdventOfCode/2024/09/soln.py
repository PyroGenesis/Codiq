import os

# paths
here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, 'input.txt')

# read input
with open(filepath, mode='r', encoding='utf8') as f:
    data = f.read()

def part1():
    disk = [int(x) for x in data.strip()]
    n = len(disk)
    checksum = 0
    block = 0

    i = 0
    # j should always be on a valid file block
    j = n-1 if n%2==1 else n-2
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
    def next_node(self):
        return self._next_node
    
    @next_node.setter
    def next_node(self, other: "FileNode | None"):
        self._next_node = other
        if other is not None:
            other._prev_node = self
    
    @property
    def prev_node(self):
        return self._prev_node
    
    @prev_node.setter
    def prev_node(self, other: "FileNode | None"):
        self._prev_node = other
        if other is not None:
            other._next_node = self


def part2():
    head = FileNode(-1, 0)
    node = head
    for i, ch in enumerate(data.strip()):
        size = int(ch)
        if size == 0:
            continue

        if i % 2 == 0:
            # file
            node.next_node = FileNode(i // 2, size)
        else:
            # space
            node.next_node = FileNode(-i, size)
        node = node.next_node
    tail = node

    # first space is immediately after first node
    space_node = head.next_node

    min_file_size = 1
    while space_node:
        if space_node.size < min_file_size:            
            while space_node and space_node.id >= 0:
                if space_node.id == file_node.id:
                    space_node = None
                else:
                    space_node = space_node.prev_node
            continue

        file_node = tail
        while file_node:
            while file_node and file_node.id < 0:
                if file_node.id == space_node.id:
                    file_node = None
                else:
                    file_node = file_node.prev_node
            if not file_node:
                break

            if file_node.size <= space_node.size:




    
