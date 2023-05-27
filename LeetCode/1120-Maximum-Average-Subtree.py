# LeetCode imports
from LeetCode.GlobalStructures import TreeNode
from typing import Optional


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def maximumAverageSubtree(self, root: Optional[TreeNode]) -> float:
        '''
        Initial and Optimal
        '''
        max_avg = 0
        
        def AvgUsingDFS(node):
            nonlocal max_avg
            
            if not node:
                return 0, 0
            
            left_count, left_sum = AvgUsingDFS(node.left)
            right_count, right_sum = AvgUsingDFS(node.right)
            curr_count = left_count + 1 + right_count
            curr_sum = left_sum + node.val + right_sum
            
            max_avg = max(max_avg, curr_sum / curr_count)
            return curr_count, curr_sum
        
        AvgUsingDFS(root)
        return max_avg