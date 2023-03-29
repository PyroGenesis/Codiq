from typing import List


class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        return self.minPathSum1D(grid)
    

    def minPathSum1D(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])

        row_dp = [0]*n
        row_dp[0] = grid[0][0]
        for j in range(1, n):
            row_dp[j] = row_dp[j-1] + grid[0][j]
        
        for i in range(1, m):
            row_dp[0] += grid[i][0]
            for j in range(1, n):
                row_dp[j] = grid[i][j] + min(row_dp[j], row_dp[j-1])
        
        return row_dp[n-1]



    def minPathSum2D(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])

        dp = [[0 for _ in range(n)] for _ in range(m)]
        dp[0][0] = grid[0][0]
        for i in range(1, m):
            dp[i][0] = dp[i-1][0] + grid[i][0]
        for j in range(1, n):
            dp[0][j] = dp[0][j-1] + grid[0][j]

        for row in range(1, m):
            for col in range(1, n):
                dp[row][col] = grid[row][col] + min(dp[row-1][col], dp[row][col-1])
        
        return dp[m-1][n-1]
