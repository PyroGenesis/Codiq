# these are the data structures I defined myself

class DSU:    
    def __init__(self, size: int) -> None:
        self.parent = list(range(size)) # ith value is the parent node to node i
        self.rank = [1] * size          # max depth of subtree rooted here (used for union by rank)
        
    def find(self, x: int) -> int:
        # if the node is not its own parent, we need to recurse on parent
        if x != self.parent[x]:
            # path compression
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def isConnected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)
    
    # returns a boolean whether or not union was needed
    def union(self, x: int, y: int) -> bool:
        rootX = self.find(x)
        rootY = self.find(y)        
        
        if rootX == rootY:
            # no union needed
            return False
        
        if self.rank[rootX] > self.rank[rootY]:
            # rootX has deeper subtree, therefore set it as parent to rootY (and its subtree)
            self.parent[rootY] = rootX
        elif self.rank[rootX] < self.rank[rootY]:
            # rootY has deeper subtree, therefore set it as parent to rootX (and its subtree)
            self.parent[rootX] = rootY
        else:
            # both subtrees are of equal depth, therefore choose either one of them as the parent of the other
            # here we chose rootX as the parent of rootY, therefore rootX depth increases by 1
            self.parent[rootY] = rootX
            self.rank[rootX] += 1
        
        # union complete
        return True

class Trie:    
    class TrieNode:
        def __init__(self):
            self.children = {}
            self.end = False

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = Trie.TrieNode()

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        """
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = Trie.TrieNode()
            node = node.children[c]
        node.end = True

    def search(self, word: str) -> bool:
        """
        Returns if the word is in the trie.
        """
        node = self.root
        for c in word:
            if c not in node.children:
                return False
            node = node.children[c]
        return node.end
        

    def startsWith(self, prefix: str) -> bool:
        """
        Returns if there is any word in the trie that starts with the given prefix.
        """
        node = self.root
        for c in prefix:
            if c not in node.children:
                return False
            node = node.children[c]
        return True
