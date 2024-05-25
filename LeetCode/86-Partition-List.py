from typing import Optional

# Definition for singly-linked list.
from LeetCode.GlobalStructures import ListNode
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    '''
    Basically we create a separate dummy list to which we move nodes that are smaller than x
    In the end we attach the original list at the end of the separate small-numbered list and return the head

    Time:  O(n)
        We iterate through all the nodes in the linked list once
    Space: O(1)
        The dummy nodes count as O(1) space
    '''
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        # If there is 0/1 nodes, no order will change
        if not head or not head.next:
            return head
        
        dummy_small = ListNode(-2)  # dummy node pointing to head of small-numbered linked list
        dummy = ListNode(-1)        # dummy node pointing to head of larger-numbered (original) linked list
        
        # set dummy as parent of head
        dummy.next = head
        # set the prev and curr node to be processed
        prev, curr = dummy, head
        # create a pointer to the end of the small-numbered linked list
        curr_small = dummy_small

        # process every node
        while curr:            
            if curr.val < x:
                # if node val is < x, this node needs to be moved to the small-numbered linked list
                prev.next = curr.next   # set prev node to skip curr node (and point directly to grandchild)
                curr_small.next = curr  # attach curr node to end of small-numbered linked list
                curr.next = None        # unset the next node pointer of the curr node since it is being moved

                curr_small = curr_small.next    # move the pointer to the end of the small-numbered linked list ahead
                # prev = prev
                curr = prev.next                # set the curr to the new node (prev will remain as-is)
            else:
                # curr node is where it should be
                # simply move on to next node, moving both prev and curr ahead
                prev, curr = curr, curr.next
        
        # if the small-numbered linked list has nodes, attach it to the front of the rest of the nodes
        if dummy_small.next:
            curr_small.next = dummy.next    # attach the rest of the nodes to the end of the small-numbered linked list
            dummy.next = dummy_small.next   # attach the small-numbered list as the start of the complete linked list

        # return the entire list, making sure to skip the dummy node
        return dummy.next
