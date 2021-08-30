# LeetCode imports
from typing import List


class Solution:
    
    '''
        Skipped Brute-force solution:
            Count the number of cells with value = value at cell (0,0) after simulating all operations
            Guide
            O(k * m * n), where k -> len of operations
    '''
    
    def maxCount(self, m: int, n: int, ops: List[List[int]]) -> int:
        '''
        This problem becomes very simple when you realize few simple facts.
         - Every operation increments 1 or more cells
           Thereby, [0, 0] will always be the max
         - For any operation [m, n], all below indices ([0,0], [1,1] ... [m-1,n-1]) also get incremented
        This makes it so that if a cell is not inc in any single operation,
         it will never catch to up to its peers in subset selections because
         any future operation that selects the cell, will also apply to all its lower peers every time
         keeping them always > cell

        Therefore, if we can find the farthest cell from [0, 0] such that it was incremented on every operation,
         that cell will mark the lower right corner of the rect starting from [0, 0] where all nums have the
         same max value

        So if we take the min of the rows and cols of all operations, we get the max row and col such that
         all operations were applied to it
            An easy way to visualize this is to consider two operations, one "long" and the other "tall", 
             and see what happens to their intersection

        The final step is to multiply this "best" row and col to get the number of cells with the max value

So we need to find minimum of all x coordinates and multiply it by minimum of all y coordinates. If we have empty update list, we need to return m * n (because all elements still equal to 0) so we can add it to our ops.

Complexity

        Time:  O(k), where k is number of updates
        Space: O(1)            
        '''
        best_m, best_n = m, n
        
        for op_m, op_n in ops:
            best_m = min(best_m, op_m)
            best_n = min(best_n, op_n)
        
        return best_m * best_n
        # NOTE: Sure you can use list comprehensions or zip to reduce to single line 
        #       but that makes copies which increases the time complexity