# Leetcode imports
from typing import Optional
from LeetCode.GlobalStructures import ListNode
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        return self.swapPairsIterative(head)
    
    '''
    Iterative Approach, Initial and Optimal
        We start with adding a dummy node to the start of the list (as first anchor)
        Then we iterate over the list keeping in mind 3 nodes are always valid
            head            (anchor) [guranteed to be valid, explanation in comments]
            head.next       (first node to swap)
            head.next.next  (second node to swap)
        Now that we have the nodes, move the links around so that the nodes are swapped:
            anchor -> second
            second -> first
            first  -> (old) second.next
            Make sure to do this in opp order so as to not lose second.next
        The loop ends when we do not have enough nodes to swap
        
        Time:  O(n)
        Space: O(1)
    '''
    def swapPairsIterative(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return None
        
        # Prepended a node at start of link list to act as the initial anchor (prev node)
        head = ListNode(next=head)
        # keep a copy of the dummy start so that we can return the actual start
        root = head
        
        # There should be at least 2 nodes after anchor to swap
        # Why don't we check head?
        #   Well, there is a sanity check at the start which checks for root head validity
        #   Later in the loop, we make head jump to head.next.next which will only happen if head.next.next
        #       is already valid (loop condition)
        #   Therefore head is always a valid node
        while head.next and head.next.next:
            # Assign the anchor, first and second nodes
            # It is not necessary to use 3 variables (1 is enough), but this makes code more readable and simpler
            anchor, first, second = head, head.next, head.next.next
            
            # Do the swaps
            # Make sure the order follows starting with assigning the node after second to first
            #   Otherwise the link to that node will be lost
            # Then follow backwards fixing all links until the anchor
            first.next = second.next
            second.next = first
            anchor.next = second
            
            # Moving 2 nodes ahead to the next anchor
            head = head.next.next
        
        # Note, if there was a copy of head iterating instead of head itself,
        #   you cannot return head here directly since head originally points to node 1 (which will be node 2 after swap)
        # You have to pass the next node of the dummy root instead
        return root.next
    
    
    '''
    Recursive Approach
        Strictly worse than iterative approach, written here for educational purpose.
        Recursive solution works here because after removing two nodes from the front, the subproblem
            becomes the same problem but with a shorter sub-list
        Base condition becomes 0 or 1 node left where we simply return
        Penultimate base becomes a simple swap with the rest of 0/1 nodes assigned directly after call
        This way, we can freely swap current two nodes, assuming later recursion will return the correct sub-list to be attached
        
        Time:  O(n)
        Space: O(n)
    '''
    def swapPairsRecursive(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # If the list has no node or has only one node left, return because we can no longer swap
        if not head or not head.next:
            return head
        
        # Convenience variables for nodes to be swapped
        # We can do this without extra variables 
        first, second = head, head.next
        # Swapping
        # Note that first node gets the recursive call since it will be the last node after swap
        first.next = self.swapPairsRecursive(second.next)
        second.next = first
        
        # Now the head is the second node
        return second