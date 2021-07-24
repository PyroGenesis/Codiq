# LeetCode import
from LeetCode.GlobalStructures import TreeNode

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

'''
    Skipped
        Iterative method: Overcomplicated and not really worth it
        Maybe just for knowledge
        https://leetcode.com/problems/binary-tree-pruning/discuss/178955/Python-postorder-traversal-solution
        O(n), O(n)        
'''

class Solution:
    def pruneTree(self, root: TreeNode) -> TreeNode:
        return self.pruneTreeNoInnerMethod(root)
    
    '''
        Not any more efficient than normal recursion but maybe more elegant-looking
        Can only be used as a follow-up ans                
        Time:  O(n)
        Space: O(n)        
    '''
    def pruneTreeNoInnerMethod(self, root):
        # if current node is empty, nothing can be done
        if not root: return None
        # assign the left subtree based on its validity
        root.left = self.pruneTree(root.left)
        # assign the right subtree based on its validity
        root.right = self.pruneTree(root.right)
        # current is valid if any 3 (val, left, right) are valid else not
        return root if root.val or root.left or root.right else None
    
    
    '''
        Initial and Optimal and Guide
        The idea is simple, the problem can be reduced as follows:
            A null node will obviously not be used
            A leaf node will only be used if its value is 1
            A parent node will only be used if
                Its left subtree has a 1 OR
                Its right subtree has a 1 OR
                Its own value is 1
        This is a very good opportunity for a recursive solution
        The recursive method checks exactly these properties
            decides whether to keep the left subtree
            decides whether to keep the right subtree
            decides whether itself is a valid node based on
                its own value AND
                the above two results
        and relays them to the parent
        
        Time:  O(n)
        Space: O(n)
    '''
    def pruneTreeRecursive(self, root: TreeNode) -> TreeNode:
        def recurse(node):
            # an empty node is out of consideration
            if not node:
                return False
            
            # Check if any node in the left subtree contains a 1
            left_is_valid = recurse(node.left)
            # Check if any node in the right subtree contains a 1
            right_is_valid = recurse(node.right)
            
            # If the left subtree does not contain a 1, prune the subtree
            if not left_is_valid:
                node.left = None
            # If the right subtree does not contain a 1, prune the subtree
            if not right_is_valid:
                node.right = None
            
            # Return True if the current node or its left or right subtree contains a 1
            return left_is_valid or right_is_valid or node.val
        
        # run algorithm recursively and capture whether its useful or not
        non_empty_tree = recurse(root)
        # return appropriately
        return root if non_empty_tree else None
