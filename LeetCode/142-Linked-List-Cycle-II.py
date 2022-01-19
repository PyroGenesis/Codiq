# LeetCode imports
from LeetCode.GlobalStructures import ListNode

class Solution:
    def detectCycle(self, head: ListNode) -> ListNode:
        return self.detectCycleFloydAlg(head)
        
    '''
        Floyd's Algorithm
        =================
        
        Suppose we have such a linked list, with L-long line concatenating with a C-long cycle. And initially we have two pointers fast and slow pointing at the head of the linked list. fast's stride is 2 and slow's stride is 1. If there is a cycle, fast will meet slow again in the cycle since fast will start to catch up with slow when slow enters the cycle (later than fast) one step each time (fast'stride - slow'stride = 1).

        And suppose fast and slow meet at point X and the entry of the cycle is E. By saying |EX|=D (in forwarding direction), slow has moved a distance of L+D while fast has moved a distance of L+D+KC where K (K>0) is the times that fast has been cycling.
        Note: why is K != 1? Because if L is a very long chain which a small loop C, fast will complete the cycle many times before slow reaches even the start of the cycle
        Since fast's stride is the double of slow's, we have L+D+KC = 2L+2D or L+D=KC. So L = C-D +(K-1)C.

        Now |XE| is what left for slow to reach E (cycle's entry) again. Remember |EX|=D, so |XE|=C-D. Thus, if slow moves a distance of L, which is C-D +(K-1)C, it will be at E. And if we have another pointer cycle_start move simultaneously with slow but start at the head of linked list, cycle_start will walked through the line whose length is L and also reach the entry point E. So slow and cycle_start will meet there, or their meeting point is the entry of the cycle.
        
        Picture here: https://leetcode.com/problems/linked-list-cycle-ii/discuss/249727/Python-Two(Three)-Pointers
        
        Time: O(n)
        Space: O(1)
    '''
    def detectCycleFloydAlg(self, head: ListNode) -> ListNode:
        # sanity check
        if not head:
            return None
        
        slow = fast = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            if slow == fast:
                # list is cyclic
                break
        else:
            # list is acyclic
            return None
        
        # cover L distance and meet at cycle intersect
        cycle_start = head
        while slow != cycle_start:
            slow = slow.next
            cycle_start = cycle_start.next
        
        return cycle_start
        
        
    
    '''
        Use a set
        O(n), O(n)
    '''
    def detectCycleNaive(self, head: ListNode) -> ListNode:
        # sanity check
        if not head:
            return None
        
        seen = set()
        
        while head:
            if head in seen:
                return head
            
            seen.add(head)
            head = head.next
            
        return None
        