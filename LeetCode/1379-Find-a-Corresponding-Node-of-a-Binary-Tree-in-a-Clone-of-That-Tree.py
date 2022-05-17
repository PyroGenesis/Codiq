from LeetCode.GlobalStructures import TreeNode
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    '''
    Simple Iterative DFS - Optimal
        The only better solution possible would be using Morris traversal but since we are not allowed to modify the trees whatsoever,
            Morris traversal is out of the picture
        
        Use a stack to perform DFS on the original tree, making sure to keep the track of the equivalent node in the cloned tree
        When we reach the target node in the original tree, simply return the respective cloned node
        
        Time:  O(n)
        Space: O(n)
    '''
    def getTargetCopy(self, original: TreeNode, cloned: TreeNode, target: TreeNode) -> TreeNode:
        # stack used for DFS
        # also keeps the cloned nodes corresponding to the nodes in the original tree
        stack = [(original, cloned)]
        
        # While we still have nodes to process
        while stack:
            # get the original and cloned nodes out of the bottom of the stack
            og_node, clone_node = stack.pop()
            
            # see if we are at target node and return the corresponding cloned node if we are
            # if repeated values are allowed, you need to compare by reference and not value
            if og_node is target:
                return clone_node
            
            # append all children to the stack
            # make sure to also keep track of the corresponding clone children
            if og_node.left:
                stack.append((og_node.left, clone_node.left))
            if og_node.right:
                stack.append((og_node.right, clone_node.right))
        
        # we will never reach here
        return None
