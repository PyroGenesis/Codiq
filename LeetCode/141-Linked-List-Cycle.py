# LeetCode imports
from LeetCode.GlobalStructures import ListNode

class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        return self.hasCycle2Ptr(head)
                
    ''' 
    Two Pointer / Floyd's Cycle Finding Algorithm
        Use two pointers, fast and slow
        At each iteration, the fast one moves 2 steps while the slow one moves 1
        if there's a loop, the fast one will finally "catch" the slow one. 
            (the distance between these 2 pointers will decrease one every iteration after fast has gone through the loop link.)
        if there's no loop, the fast runner will reach the end of linked list. (NULL)
        
        Time:  O(n+k) where k -> cyclic length (the nodes fast to travel again to "catch" slow)
               But since k <= n, complexity becomes O(n)
        Space: O(1)
    '''
    def hasCycle2Ptr(self, head: ListNode) -> bool:
        # both pointers start at head
        slow = head
        fast = head
        
        # continue loop if there are at least 2 nodes ahead for fast to travel to
        # if there are < 2 nodes, there is no loop
        while fast and fast.next:
            # move the pointers
            slow = slow.next
            fast = fast.next.next
            
            # check equality (catch) condition
            # we do this after moving because initially both pointers are on same node (head)
            if slow == fast: return True
            
        ''' Alternative solution by Stefan the absolute madman
            "Easier to ask for forgiveness than permission."
        try:
            slow = head
            fast = head.next
            while slow is not fast:
                slow = slow.next
                fast = fast.next.next
            return True
        except:
            return False
        '''
        
        # there is no loop
        return False
        
    
    
    '''
        Destructive methods: Following algorithms give a solution but destroy the input LL in the process
            Reversing list - Skipped
                https://leetcode.com/problems/linked-list-cycle/discuss/44498/Just-reverse-the-list
                When we reverse the Linked List in-place as we go along, we will end up at the root node at the end
                    because of the loop
                If head == reversed(head) + some edge conditions, then there is a loop
            
            Mark node - Explanation and algorithm below
    '''
        
    '''
    Marker node - Destructive solution
        After encountering a node, point its next to a special node called marker
        If we encounter a node already pointing to marker, that node has been seen so it's a loop
        Time:  O(n)
        Space: O(1)
    '''
    def hasCycleMarkNode(self, head: ListNode) -> bool:
        # make the marker node
        marker = ListNode(0)
        
        while head:
            # check if current node is marker
            # if so, we looped
            if head is marker:
                return True
            
            # change head to be the next node AND
            # change curr head.next to point to marker
            # in the same statement
            head.next, head = marker, head.next
        
        # there is no loop
        return False
    
        
    '''
    Hashset - Simple solution
        Check if current node already in seen set. If so, there is a loop.
        Time:  O(n)
        Space: O(n)
    '''
    def hasCycleHashmap(self, head: ListNode) -> bool:
        seen = set()    # seen nodes
        
        # if LL ends before we find a loop, there is no loop
        while head:
            # if we looped back to a seen node
            if head in seen:
                return True
            
            # mark current node as seen and move ahead
            seen.add(head)
            head = head.next
        
        return False