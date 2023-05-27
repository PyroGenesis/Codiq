# special TrieNode with val
class TrieNode:
    def __init__(self):
        self.children = {}
        self.val = 0
            
# this will be a modified Trie (with vals)
class MapSum:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = TrieNode()
        

    def insert(self, key: str, val: int) -> None:
        node = self.root
        for c in key:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.val = val        

    def sum(self, prefix: str) -> int:
        node = self.root
        for c in prefix:
            if c not in node.children:
                return 0
            node = node.children[c]
        
        res = 0
        stack = [node]
        while stack:
            curr = stack.pop()
            res += curr.val
            for child in curr.children.values():
                stack.append(child)
        
        return res
        


# Your MapSum object will be instantiated and called as such:
# obj = MapSum()
# obj.insert(key,val)
# param_2 = obj.sum(prefix)