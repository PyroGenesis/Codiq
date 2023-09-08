from typing import List


class Solution:
    '''
    Iterative DP
        Believe it or not, this solution counts as a Dynamic Programming one
        Just create the Pascal's triangle row by row based on its property
            First row can be hardcoded as [1] to make logic simpler
        Each row starts as [1], then the sums, then ends as [1]

        Time:   O(rows^2)
            The rows are of size 1,2,3 ... rows
            => (rows)(rows+1) / 2
            => O(rows^2)
        Space:  O(1) if you don't count output space
                O(rows^2) if you do
    '''
    def generate(self, numRows: int) -> List[List[int]]:
        # The triangle 
        # First row hardcoded
        pascal = [[1]]
        last = pascal[0]    # The last pascal triangle row created

        for _ in range(numRows-1):
            # create new row
            curr = [1]
            for i in range(1, len(last)):
                curr.append(last[i-1] + last[i])
            curr.append(1)

            # append it and update last
            pascal.append(curr)
            last = curr
        
        # return the triangle
        return pascal
