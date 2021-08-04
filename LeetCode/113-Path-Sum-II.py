# LeetCode imports
from typing import List
from LeetCode.GlobalStructures import TreeNode

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    '''
        Skipped
        
        Iterative solution
            Keeping 3 variables (node, sum, path) in stack is cumbersome
            It also leads to a higher space complexity due to path duplication
    '''
    
    '''
        Initial, Optimal, Recursive DFS ? Backtracking
        We start with the root
        We keep adding it to our current path and sum
        Then we move on to its left node (if possible)
        If it doesn't have a left node, we can pick the right one and keep going
        If it doesn't have either, its a leaf node and we've reached a potential solution
        Check if the cumulative sum == targetSum
            If so, add it to global list of paths
            If not, this path is not possible so never mind
        Now the parent node of this last node we reached might have another subtree to evaluate
        So we remove current node from current path and sum and return
            back to the parent
        The parent (after checking all subtrees) also removes itself from consideration
            and returns to its parent so that the grandparent may explore another subtree
        This cascades throughout the tree and eventually we explore all nodes
        
        The beauty of this solution is that since we explore only one path at a time
            and backtrack when we're done,
            we only have to use one variable to maintain the path and the cumulative sum
        
        Time:  O(n^2)
                Initially you might think the time complexity is O(nlogn)
                    (for complete binary tree)
                But Consider the tree like so:

                          A
                         / \
                        B   C
                           / \
                          D   E
                             / \
                        and so on...

                Let the number of nodes = n
                Therefore depth of tree is approx n/2 and number of leaves are also approx n/2
                Now, potential correct paths are of length: 2, 3, ... n/2
                Copying these n/2 paths n/2 times to the answer arr gives us the complexity O(n*2)

         Space: O(n) [path variable, output ignored]
    '''
    def pathSum(self, root: TreeNode, targetSum: int) -> List[List[int]]:
        # sanity check
        if not root:
            return []
        
        # utility method to check for leaf node
        def isLeafNode(node):
            return not node.left and not node.right
        
        allRoutes = []  # ans
        route = []      # current path
        currentSum = 0  # cumulative sum of current path
        
        def dfs(node):
            nonlocal isLeafNode, route, allRoutes, currentSum
            
            # Add the current node to the path's list
            currentSum += node.val
            route.append(node.val)
            
            # Check if the current node equals our remaining sum and also,
            # if it is a leaf. If it is, we add the path to
            # our list of paths
            if currentSum == targetSum and isLeafNode(node):
                allRoutes.append(list(route))
            
            # we will recurse on the left and the right children
            if node.left: dfs(node.left)
            if node.right: dfs(node.right)
            
            # We need to pop the node once we are done processing ALL of it's subtrees.
            route.pop()
            currentSum -= node.val
        
        dfs(root)
        return allRoutes