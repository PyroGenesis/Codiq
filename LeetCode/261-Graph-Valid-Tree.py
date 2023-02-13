# LeetCode imports
from typing import List

class DSU:
    # !! UNOPTIMIZED !!
    def __init__(self, size):
        self.parent = list(range(size))
    
    def find(self, x):
        while x != self.parent[x]:
            x = self.parent[x]
        return x
    
    def union(self, x, y):
        self.parent[self.find(x)] = self.find(y)

class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) < n-1:
            return False
        
        dsu = DSU(n)
        
        for edge in edges:
            a, b = edge
            if a > b: a,b = b,a
            
            if dsu.find(a) == dsu.find(b):
                return False
            
            dsu.union(a, b)
        return True
            