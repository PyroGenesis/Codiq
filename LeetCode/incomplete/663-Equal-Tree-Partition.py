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
    def checkEqualTree(self, root: Optional[TreeNode]) -> bool:
        # first thought was cumulative then pick smaller child
        # second thought was pick self, and cut from parent above (inspired from another soln)
        # third (and last thought) was the cumulative itself is the ans
        # Mistake! keep in mind that root cannot be the cut off node because it has no parent
        
        tree_sum = 0
        def sumTree(node):
            nonlocal tree_sum
            if not node:
                return
            
            tree_sum += node.val
            sumTree(node.left)
            sumTree(node.right)
        
        sumTree(root)
        if tree_sum % 2 == 1: return False
        half_sum = tree_sum // 2
        
        def dfs(node):
            nonlocal half_sum
            if not node:
                return 0, False
            
            s_left, res = dfs(node.left)
            if res: return 0, res
            s_right, res = dfs(node.right)
            if res: return 0, res
            
            s = node.val + s_left + s_right
            return s, s == half_sum
        
        (_, ans1), (_, ans2) = dfs(root.left), dfs(root.right)
        return ans1 or ans2
        