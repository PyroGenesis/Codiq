from typing import List

class Solution:
    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        return self.transposeSimple(matrix)
    
    '''
    One-liner
        Python3 has zip, which takes in elements from multiple streams one at a time and combines them
        If we give zip a list of rows, it will return a list of columns as it takes one element at a time from each row
        Treating the output of zip as new rows will give us the transpose of the matrix
                
        Time:  O(m*n)
        Space: O(m*n)
    '''
    def transposeOneLiner(self, matrix: List[List[int]]) -> List[List[int]]:
        # All below solutions work and are shorter but do not return the correct format
        # zip(*matrix)              returns a generator (of tuples)
        # list(zip(*matrix))        returns a list of tuples
        # map(list, zip(*matrix))   returns a generator (of lists)
        return list(map(list, zip(*matrix)))

    '''
    Simple and optimal
        Make a transpose matrix with inverted dimensions
        Copy all values in transpose matix
        
        Time:  O(m*n)
        Space: O(m*n)
    '''
    def transposeSimple(self, matrix: List[List[int]]) -> List[List[int]]:
        # dimensions of input matrix
        m, n = len(matrix), len(matrix[0])        
        # making transpose matrix with swapped dimensions
        transpose = [[0]*m for _ in range(n)]
        
        # loop through all elements and assign them to their swapped loc in matrix
        for i in range(m):
            for j in range(n):
                transpose[j][i] = matrix[i][j]
        
        # return transpose matrix
        return transpose