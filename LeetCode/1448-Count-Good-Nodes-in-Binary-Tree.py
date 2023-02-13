# LeetCode imports
from LeetCode.GlobalStructures import TreeNode

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        good_nodes = 0
        maxes = [float('-inf')]
        
        def dfs(node):
            nonlocal good_nodes, maxes
            
            if not node:
                return
            
            is_good_node = node.val >= maxes[-1]
            
            if is_good_node:
                good_nodes += 1
                maxes.append(node.val)
                
            dfs(node.left)
            dfs(node.right)
            
            if is_good_node:
                maxes.pop()
        
        dfs(root)
        return good_nodes
