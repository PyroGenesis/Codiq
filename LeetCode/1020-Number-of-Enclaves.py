from typing import List

'''
Skipped: BFS
    Same as DFS but DFS feels more intuitive
'''

class Solution:
    '''
    DFS
        Basically, we need to count all the land not touching an edge directly or indirectly
        So one way would be to count all land first, then eliminate the land touching the boundary
        But for me, the other way is better:
            Eliminate any land touching the boundary
            Then simply count the land remaining
        
        For elimination, simply filling that land up with water seems to be the best idea
        For counting, it is just a simple 'count all ones' operation
            No need to modify the grid
        
        Time complexity: O(m * n)
            Creating copy
                m * n
            Every cell is visited a constant amount of time
                O(m * n)
        
        Space complexity: O(m * n)
            copy
                m * n
            dfs recursive stack in worse case where entire grid is one big island
                O(m * n)
    '''
    def numEnclaves(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        # make a copy of the grid so as to not modify the input
        copy = [[grid[i][j] for j in range(n)] for i in range(m)]

        # recursive dfs
        def dfs(i, j):
            nonlocal m, n, copy

            if i < 0 or i >= m or j < 0 or j >= n:
                # if the cell is out of bounds, forget about it
                return
            if copy[i][j] == 0:
                # if the cell is already water, simply return
                return
            
            # change current land cell to water
            copy[i][j] = 0
            # run dfs recursive on all 4 neighbors
            # we don't check any bounds here since it looks cleaner to check in start of dfs
            dfs(i-1, j)
            dfs(i+1, j)
            dfs(i, j-1)
            dfs(i, j+1)
        
        # eliminate any land touching the edges (and their connected islands)
        #   by filling it with water
        for i in range(m):
            # processing left and right edges
            dfs(i, 0)
            dfs(i, n-1)
        for j in range(n):
            # processing top and bottom edges
            dfs(0, j)
            dfs(m-1, j)
        # corners are processed twice but it doesn't matter
        
        # since we've already processed the edges, we only loop through the middle cells
        # simply count up all the remaining land
        return sum(sum(row) for row in copy)
