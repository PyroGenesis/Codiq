# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
from typing import Optional

from LeetCode.GlobalStructures import ListNode


class Solution:
    '''
    Two-pointers, Single pass, Optimized
        Finding the kth node is simple, just iterate (k-1) times starting from the first node
        But can we find the (n-k)th node in a single pass? Without knowing the length?
            Yes, we can!
        By keeping two pointers at a distance of k from each other while moving both ahead at the same time,
            when the pointer ahead encounters the last node, the pointer before will be on the (n-k)th node
        Luckily, since we used a pointer to find the kth node, that pointer will be at a distance k from
            any pointer starting at head. Therefore we can simply reuse it.
        
        Time:  O(n)
        Space: O(1)        
    '''
    def swapNodes(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        # the pointer responsible for finding the kth node + acting as ahead scout for (n-k)th node
        fast = head
        # find the kth node
        # we don't check if fast is valid because of the constraint k <= n
        for _ in range(k-1):
            fast = fast.next        
        node1 = fast
        
        # the pointer responsible for finding the (n-k)th node
        # it lags behind fast pointer at a distance of k, so that it immediately identify the node when fast reaches the end
        slow = head
        # find the (n-k)th node
        # we iterate until fast is on the last node
        #   when that is true, slow will be automatically at the (n-k)th node due to maintaining distance of k
        while fast.next:
            fast = fast.next
            slow = slow.next
        node2 = slow
        
        # swap values
        node1.val, node2.val = node2.val, node1.val
        # return head (which was never changed)
        return head
    
    '''
    Skipped:
        3-pass: one pass for length, one pass for kth node, one pass for (n-k)th node
        2-pass: one pass for length, one pass for kth and (n-k)th node
        Swapping nodes:
            Here we need pre_left and pre_right along with left (kth) and right ((n-k)th) nodes
            https://leetcode.com/problems/swapping-nodes-in-a-linked-list/discuss/1054370/Python-3-or-Swapping-NODES-or-Swapping-Values-or-One-Pass-or-Fully-explained
        
        All of these are also O(n), O(1)
    '''
