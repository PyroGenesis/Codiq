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
    Recursive Traversal
        Simply traverse through a DFS manner, following some simple rules to truncate subtrees and ou-of-bounds middle nodes:
         - If the root is smaller than the low limit, we know that both the root and its left subtree cannot be part of solution
           Therefore, we skip to the root.right node and try again
         - If the root is larger than the high limit, we know that both the root and its right subtree cannot be part of solution
           Therefore, we skip to the root.left node and try again
         - If the root is within [low, high] range, root node is part of solution and nodes from both left and right subtrees
            might be part of the solution, so we recurse on both subtrees and reassign to parent before returning it
        
        Time:  O(n)
        Space: O(n)          
    '''
    def trimBST(self, root: Optional[TreeNode], low: int, high: int) -> Optional[TreeNode]:
        # if there is no node, return nothing
        if not root:
            return None
        
        if root.val < low:
            # if root < low, root and root.left are definitely out of bounds
            # but maybe root.right will be in-bound, so recursively run on it and return it
            return self.trimBST(root.right, low, high)
        elif root.val > high:
            # if root > high, root and root.right are definitely out of bounds
            # but maybe root.left will be in-bound, so recursively run on it and return it
            return self.trimBST(root.left, low, high)
        else:
            # root is in-bound, so both root.left and root.right also have a chance to be in-bounds
            # run recursively on both branches
            root.left = self.trimBST(root.left, low, high)
            root.right = self.trimBST(root.right, low, high)
            # return the root this time
            return root
