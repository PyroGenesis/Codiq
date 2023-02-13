# LeetCode import
from typing import List


class Solution:
    def beautifulArray(self, n: int) -> List[int]:
        return self.beautifulArray_DaC_Iterative(n)
    
    ''' Remaining
            The amazing alternates soln
    '''
        
    def beautifulArray_DaC_Iterative(self, n: int) -> List[int]:
        beautiful = [1]
        
        while(len(beautiful) < n):
            beautiful = [x*2-1 for x in beautiful] + [x*2 for x in beautiful]
            
        return [x for x in beautiful if x <= n]
    
    
    '''
        TLE
    '''
    def beautifulArrayBacktracking(self, n: int) -> List[int]:
        beautiful = []
        available = set(range(1, n+1))
        
        def backtrack():
            nonlocal available, beautiful
            
            if len(available) == 0:
                return True
            
            for pick in list(available):
                for prev in beautiful:
                    if (pick*2 - prev) in available:
                        break
                else:
                    # all prev were satisfied
                    available.remove(pick)
                    beautiful.append(pick)
                    
                    result = backtrack()
                    if result: return result
                    
                    beautiful.pop()
                    available.add(pick)
            return False
            
        backtrack()
        return beautiful