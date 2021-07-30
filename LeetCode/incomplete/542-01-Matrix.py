# LeetCode imports
import collections
from typing import List


class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        m = len(mat)
        n = len(mat[0])
        
        DIRECTIONS = {
            'top':    (-1, 0),
            'right':  (0, +1),
            'left':   (0, -1),
            'bottom': (+1, 0),
        }
        
        dp = [[float('inf') for i in range(n)] for j in range(m)]
        frontier = collections.deque()
        
        def addDirectionToIndices(i, j, direction):
            return (i+direction[0], j+direction[1])
        
        def addNeighborsToFrontier(i, j):
            nonlocal DIRECTIONS, frontier
            if i > 0:
                frontier.append(addDirectionToIndices(i, j, DIRECTIONS['top']))
            if j > 0:
                frontier.append(addDirectionToIndices(i, j, DIRECTIONS['left']))
            if i < m-1:
                frontier.append(addDirectionToIndices(i, j, DIRECTIONS['bottom']))
            if j < n-1:
                frontier.append(addDirectionToIndices(i, j, DIRECTIONS['right']))
        
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 0:
                    dp[i][j] = 0
                    addNeighborsToFrontier(i, j)
        
        distance = 1
        while frontier:
            nodes_on_level = len(frontier)
            for i in range(nodes_on_level):
                i, j = frontier.popleft()
                
                if dp[i][j] > distance:
                    dp[i][j] = distance
                    addNeighborsToFrontier(i, j)
            
            distance += 1
        
        return dp