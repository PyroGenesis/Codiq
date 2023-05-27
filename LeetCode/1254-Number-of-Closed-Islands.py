from typing import List

'''
Skipped: BFS
    Same as DFS but DFS feels more intuitive
'''

class Solution:
    '''
    DFS
        Basically, we need to count all islands completely surrounded by water
        Now, the first intuition is that any island that touches the border cannot be valid.
            Also, the inverse is true: Any island not touching the border is valid.
        So one way would be to count all islands first, then eliminate the ones touching the boundary
        But for me, the other way is better:
            Eliminate any land (and connected islands) touching the boundary
            Then simply count the islands
        
        For elimination, simply filling that land up with water seems to be the best idea
        For counting, we could've used a visited grid / set to keep track of visited land
            But here too, autofilling any land visited seems to have no downsides
        
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
    def closedIsland(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        # make a copy of the grid so as to not modify the input
        copy = [[grid[i][j] for j in range(n)] for i in range(m)]

        # recursive dfs
        def dfs(i, j):
            nonlocal m, n, copy

            if i < 0 or i >= m or j < 0 or j >= n:
                # if the cell is out of bounds, forget about it
                return
            if copy[i][j]:
                # if the cell is already water, simply return
                return
            
            # change current land cell to water
            copy[i][j] = 1
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
        
        closed_islands = 0
        # since we've already processed the edges, we only loop through the middle cells
        for i in range(1, m-1):
            for j in range(1, n-1):
                if copy[i][j] == 0:
                    # if land found, register an island
                    closed_islands += 1
                    # then fill it with water
                    dfs(i, j)
        
        return closed_islands
