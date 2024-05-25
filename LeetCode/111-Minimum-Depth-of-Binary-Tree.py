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
    
    '''
        Init and Optimal - BFS
        The worst tree for BFS here is a complete tree, since all the leaves will be in the last level
        We will only access the upper n/2 nodes + 1 last level node before returning at max
        
        Time: n/2 = O(n)
        Space: n/2 = O(n)
    '''
    def minDepth(self, root: Optional[TreeNode]) -> int:
        # no nodes, depth = 0
        if not root:
            return 0
        
        # utility method foe checking if node is leaf
        def isLeaf(node):
            return node.left is None and node.right is None
        
        # basic BFS with a leaf check
        # this is guaranteed to catch the min depth node
        queue = deque([root])
        depth = 1
        
        while queue:
            nodes_at_level = len(queue)
            for _ in range(nodes_at_level):
                node = queue.popleft()
                if isLeaf(node):
                    return depth
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            depth += 1
        
        # execution will never reach here
        return -1
