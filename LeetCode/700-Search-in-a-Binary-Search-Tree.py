# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

from typing import Optional
from LeetCode.GlobalStructures import TreeNode

class Solution:
    '''
    Iterative
        This is just iterating through a BST, it needs no explanation
        Time:  O(H)
                H -> Height of tree O(logn) in best case and O(n) in worst case
        Space: O(1)
    '''
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        # iterate until we run out of nodes to explore
        while root:
            if root.val < val:
                # if current node is less than target, target node has to be in the right subtree
                root = root.right
            elif root.val > val:
                # if current node is greater than target, target node has to be in the left subtree
                root = root.left
            else:
                # we are right on target, return current node
                return root
        
        # we could not find the target
        return None