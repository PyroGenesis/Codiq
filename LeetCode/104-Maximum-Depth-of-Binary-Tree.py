from collections import deque
from typing import Optional

from LeetCode.GlobalStructures import TreeNode
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        return self.maxDepthIterativeBFS(root)
    
    def maxDepthIterativeBFS(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        
        queue = deque([root])
        depth = 0
        
        while queue:
            depth += 1
            n = len(queue)
            for _ in range(n):
                node = queue.popleft()
                if node.left: queue.append(node.left)
                if node.right: queue.append(node.right)
        
        return depth
        
    def maxDepthRecursiveDFS(self, root: Optional[TreeNode]) -> int:
        
        def getMaxDepth(node):
            if not node:
                return 0            
            return 1 + max(getMaxDepth(node.left), getMaxDepth(node.right))
            
        return getMaxDepth(root)
        