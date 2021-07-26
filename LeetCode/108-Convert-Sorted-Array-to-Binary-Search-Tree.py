# LeetCode imports
from LeetCode.GlobalStructures import TreeNode
from typing import List

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

'''
    Skipped:
        Recursive soln but choosing right middle as root every time
            Guide
            O(n), O(logn) / O(n)
        Recursive soln but choosing random middle from left or right middles as root
            Guide
            O(n), O(logn) / O(n)
        Recursive with no helper fn
            Slicing nums increases time complexity, so this soln is suboptimal
            O(nlogn), O(n)
'''

'''
    Initial, Optimal, Guide
    If the input is sorted, the best node as a root to that range would the num in the middle
    This is because it divides the list into two parts of (almost) equal elements
        guaranteeing that both subtrees will have (almost) equal heights
    The above divides the problem into 2 smaller subproblems which can be solved the same way
    This leads to the recursive solution
    
    Time:  O(n) - Every node is visited once
    Space: O(logn) - If you ignore output (recursion length) OR
           O(n)    - If you don't
'''


class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> TreeNode:
        # start and end are inclusive here
        def convertRangeToBST(start, end):
            nonlocal nums
            
            if start > end:
                # no nodes in this subtree
                return None
            elif start == end:
                # this subtree has a leaf node
                return TreeNode(nums[start])
            
            # the middle root node idx
            # this might be unsafe if the length of nums was big
            # in that case, you should use start + (end - start) // 2
            # but here the input length will be safe to double
            # so we use this easy syntax
            # >> 2 is yet another optimization
            mid = (start + end) // 2
            
            # return the root, recursively creating the left and right subtrees
            return TreeNode(nums[mid], convertRangeToBST(start, mid-1), convertRangeToBST(mid+1, end))
        
        # return the tree passing in the entire nums list
        return convertRangeToBST(0, len(nums)-1)