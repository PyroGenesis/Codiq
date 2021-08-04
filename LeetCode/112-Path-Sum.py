# LeetCode imports
from LeetCode.GlobalStructures import TreeNode

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    
    ''' Skipped
        Recursive DFS
            Guide, https://leetcode.com/problems/path-sum/discuss/36470/u3010Pythonu3011Recursive-solution-with-explanation-and-thinking-process
            O(n), (Worst: O(n), Best: O(logn))
    '''
    
    '''
        Initial, Optimal, Iterative DFS
        Idea is pretty simple, you maintain a DFS which includes current path
        (With a twist that the current sum, [or the remainder], also have to be part of the stack)
        Now when you get to a node where sum == target and its a leaf node, you found it
        
        Time:  O(n)     for iterating over all nodes once
        Space: O(logn)) if tree is balanced        
               O(n)     if tree is unbalanced
        
    '''
    def hasPathSum(self, root: TreeNode, targetSum: int) -> bool:
        # sanity check (they changed it!)
        if root is None:
            return False
        
        # path nodes, sum
        route = []
        route.append([root, root.val])
        
        while route:
            node, total = route.pop()
            # We dont do this becoz of -ve values in tree that could lower sum
            # if total > targetSum:
            #     continue
            if total == targetSum:
                if node.left is None and node.right is None:
                    return True
            
            # only put back valid nodes into stack
            if node.left: route.append([node.left, total+node.left.val])
            if node.right: route.append([node.right, total+node.right.val])
        
        # no child node resulted in targetSum
        return False