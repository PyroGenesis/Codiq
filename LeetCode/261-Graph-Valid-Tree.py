# LeetCode imports
from typing import List
# custom datastructure
from LeetCode.GlobalStructures import DSU

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
            