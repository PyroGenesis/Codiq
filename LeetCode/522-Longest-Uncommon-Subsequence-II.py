# LeetCode imports
from typing import List

class Solution:
    def findLUSlength(self, strs: List[str]) -> int:
        n = len(strs)
        
        strs.sort(key=len)
        strs.reverse()
        
        def isSubSeq(string, parent):
            i, j = 0, 0
            while i < len(string) and j < len(parent):
                if string[i] == parent[j]:
                    i += 1
                j += 1
            # print(f'isSubSeq - string: {string}, parent: {parent}, {i == len(string)}')
            return i == len(string)
        
        for string_idx in range(n):
            string = strs[string_idx]
            
            is_subseq = False
            for potential_parent_idx in range(n):
                if string_idx == potential_parent_idx:
                    continue
                
                potential_parent = strs[potential_parent_idx]
                if len(potential_parent) < len(string):
                    break
                
                if isSubSeq(string, potential_parent):
                    is_subseq = True
                    break
            
            if not is_subseq:
                return len(string)
            
        return -1
                