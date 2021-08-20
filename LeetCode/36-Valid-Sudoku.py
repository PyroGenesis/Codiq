# LeetCode imports
from typing import List

class Solution:
    '''
    In this problem, there are 3 approaches and 3 techniques for each of those approaches

    Approaches:
    1. Iterate over all rows, then all columns, then all blocks. Check for dups at each stage.
    2. Iterate over all cells once, but keep track of dups in that cell's row, col, block
        at the same time
    3. Iterate over all cells once, use a unique representation of cell row, col, block
        to check for dups (Stefan's soln)
        https://leetcode.com/problems/valid-sudoku/discuss/15472/Short%2BSimple-Java-using-Strings
    Techniques (How do you check for dups):
    1. One fixed-length array per row, col, block
    2. One hashset per row, col, block
    3. One number per row, col, block (bitmasking)

    Complexity matrix:
        
    +----------------------+------------+--------+--------+-------------------------------+
    |       Approach       |  Technique |  Time  |  Space |            Comments           |
    |                      |            |        |        |                               |
    +======================+============+========+========+===============================+
    |                      | Array      | O(N^2) | O(N)   | (Skipped)                     |
    |                      +------------+--------+--------+-------------------------------+
    | Iter thrice          | Hashset    | O(N^2) | O(N)   | Probably the simplest for me  |
    | Check dups each time +------------+--------+--------+-------------------------------+
    |                      | Bitmasking | O(N^2) | O(1)   | Optimal in Space.             |
    |                      |            |        |        |  Time coeff is 3.             |
    +----------------------+------------+--------+--------+-------------------------------+
    |                      | Array      | O(N^2) | O(N^2) | (Skipped)                     |
    |                      +------------+--------+--------+-------------------------------+
    | Iter once            | Hashset    | O(N^2) | O(N^2) | (Skipped)                     |
    | Check dups thrice    +------------+--------+--------+-------------------------------+
    |                      | Bitmasking | O(N^2) | O(N)   | Semi-optimal in Space         |
    |                      |            |        |        |  while being optimal in Time. |
    +----------------------+------------+--------+--------+-------------------------------+
    | Iter once            | Hashset    | O(N^2) | O(N^2) | By Stefan. Uses a large       |
    | Check str dups       |            |        |        |  common Hashset. (Skipped)    |
    +----------------------+------------+--------+--------+-------------------------------+
        
    '''
    
    
    '''
        Initial, modified
        Original version used dictionaries, modified uses a set
            Much more intuitive change but not enough to warrant a separate solution
        Runs through the grid like a Human would
            Check each row for dups
            Check each col for dups
            Check each block for dups
        
        Time:  O(N^2)
        Space: O(N)
    '''
    def isValidSudoku3PassHashSet(self, board: List[List[str]]) -> bool:
        # check a cell
        def checkSingle(r, c, numset):
            nonlocal board
            single = board[r][c]
            if single == '.':
                return True
            
            if not 1 <= int(single) <= 9:
                return False
            
            # (OLD) I'm using the advantage that 
            #   dict['i'] is True if > 0 to weed out the duplicates
            # if freq[single]:
            #     return False            
            if single in numset:
                return False
            
            numset.add(single)
            return True
        
        # check a row
        def checkRow(r):
            nonlocal board
            numset = set()
            
            for j in range(9):
                if not checkSingle(r, j, numset): return False            
            return True
        
        # check a column
        def checkCol(c):
            nonlocal board
            numset = set()
            
            for i in range(9):
                if not checkSingle(i, c, numset): return False            
            return True
        
        # check a block
        def checkBlock(start_r, start_c):
            nonlocal board
            numset = set()
            
            for i in range(start_r, start_r+3):
                for j in range(start_c, start_c+3):
                    if not checkSingle(i, j, numset): return False            
            return True
        
        # check all rows
        for i in range(9):
            if not checkRow(i): return False
        # check all columns
        for j in range(9):
            if not checkCol(j): return False
        
        # check all blocks
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                if not checkBlock(i, j): return False
        
        # everything checks out
        return True
    
    '''
        The most efficient in terms of space
        Same approach as above, moves through the grid like a Human would
        However, it uses a single num instead of a set of keep track of dups
        It can do so by using that num as a bitmask where bit 1 to bit 9
         indicate that num 1-9 has been seen
        
        Time:  O(N^2)
        Space: O(N)
    '''
    def isValidSudoku3PassBitMask(self, board: List[List[str]]) -> bool:
        num = 0
        
        # check a cell
        def checkSingle(r, c):
            nonlocal board, num
            if board[r][c] == '.':
                return True
            
            single = int(board[r][c])
            if not 1 <= single <= 9:
                return False
            
            # (OLD) I'm using the advantage that 
            #   dict['i'] is True if > 0 to weed out the duplicates
            # if freq[single]:
            #     return False
            
            # (OLD) set method
            # if single in numset:
            #     return False
            
            if num & (1 << single):
                return False            
            
            num |= (1 << single)
            return True
        
        # check a row
        def checkRow(r):
            nonlocal board, num
            num = 0
            
            for j in range(9):
                if not checkSingle(r, j): return False            
            return True
        
        # check a column        
        def checkCol(c):
            nonlocal board, num
            num = 0
            
            for i in range(9):
                if not checkSingle(i, c): return False            
            return True
        
        # check a block
        def checkBlock(start_r, start_c):
            nonlocal board, num
            num = 0
            
            for i in range(start_r, start_r+3):
                for j in range(start_c, start_c+3):
                    if not checkSingle(i, j): return False            
            return True
        
        # check all rows
        for i in range(9):
            if not checkRow(i): return False
        # check all columns
        for j in range(9):
            if not checkCol(j): return False
        
        # check all blocks
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                if not checkBlock(i, j): return False
        
        # everything checks out
        return True
    
    '''
        A good middle ground, short as well
        A low time coeff since only one pass and the space isn't bad too
        Runs through each cell only once. For each cell it
            Checks whether its row has a dup
            Checks whether its col has a dup
            Checks whether its block has a dup
        Each row, col, block is represented by a single bitmasked integer
        Therefore in total it uses 3N nums
        
        Time:  O(N^2)
        Space: O(N)
    '''
    def isValidSudoku1PassBitMask(self, board: List[List[str]]) -> bool:
        row_nums = [0]*9       # numbers seen in a row
        col_nums = [0]*9       # numbers seen in a col
        block_nums = [0]*9     # numbers seen in a block
        
        for r in range(9):
            for c in range(9):
                # skip if cell is '.''
                if board[r][c] == '.':
                    continue

                # verify digit constraints
                cell = int(board[r][c])
                if not 1 <= cell <= 9:
                    return False
                
                # you can check this idx by trial and error
                block_idx = (r // 3) * 3 + c // 3
                
                # verify this num is new in this row, col amd block
                if row_nums[r] & (1 << cell): return False
                if col_nums[c] & (1 << cell): return False
                if block_nums[block_idx] & (1 << cell): return False
                
                # add this num as seen in this row, col and block
                row_nums[r] |= (1 << cell)
                col_nums[c] |= (1 << cell)
                block_nums[block_idx] |= (1 << cell)
        
        # everything checks out
        return True
    
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        return self.isValidSudoku1PassBitMask(board)