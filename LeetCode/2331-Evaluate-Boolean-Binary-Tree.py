from typing import Optional
from .GlobalStructures import TreeNode

'''
Simple recursion - Anything else is overcomplicating the solution

Time:  O(n)     where n -> no. of nodes
    we have to go through every node once
Space: O(n)     where n -> no. of nodes
    the depth of a skewed binary tree is n/2
    so O(n/2) = O(n)
'''
class Solution:
    def evaluateTree(self, root: Optional[TreeNode]) -> bool:
        def recurse(node: TreeNode):
            if node.val == 0:
                return False
            elif node.val == 1:
                return True
            elif node.val == 2:
                return recurse(node.left) or recurse(node.right)
            else:
                return recurse(node.left) and recurse(node.right)
        return recurse(root)
