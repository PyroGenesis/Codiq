# LeetCode imports
from typing import Optional
from LeetCode.GlobalStructures import ListNode

class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        return self.detectCycleFloydAlg(head)
        
    '''
        Floyd's Algorithm
        =================
        
        Suppose we have such a linked list, with L-long line concatenating with a C-long cycle.

        Initially we have two pointers fast and slow pointing at the head of the linked list. 
            fast's stride is 2 and slow's stride is 1. 
        If there is a cycle, fast will meet slow again in the cycle 
          since fast will start to catch up with slow when 
          slow enters the cycle (later than fast) one step each time 
            (fast'stride - slow'stride = 1).

        Now,    L -> length of nodes before cycle
                C -> length of cycle        
        Suppose fast and slow meet at point X and the entry of the cycle is E. 
            (these are points, not distances)
        Also, lets say that before meeting, slow has completed M cycles and fast has completed N cycles
        By saying |EX|=D (in forwarding direction), 
            slow has moved a distance of L + MC + D while 
            fast has moved a distance of L + NC + D 
                where N > M because there is no way slow and fast meet without fast looping around.
        Note: why is K != 1? Because if L is a very long chain which a small loop C, 
              fast will complete the cycle many times before slow reaches even the start of the cycle
        Since fast's stride is the double of slow's, we get:
            2 (L + MC + D) = L + NC + D
            2L + 2MC + 2D = L + NC + D
            L = NC - 2MC - D
            L = C (N - 2M) - D
            L = ZC - D                  where Z -> N-2M, Z >= 0

        Now |XE| is what left for slow to reach E (cycle's entry) again. 
        Remember |EX|=D, so |XE|=C-D. Thus, if slow moves a distance of L, which is ZC - D, it will be at E. 
        This is because,    slow's current position + L
                        =>  D + [ZC - D]
                        =>  ZC
        since, this is a multiple of C, this is right back to the start of the cycle, or E
        And if we have another pointer cycle_start move simultaneously with slow but start at the head of linked list, 
          cycle_start will walked through the line whose length is L and also reach the entry point E. 
        So slow and cycle_start will meet there, or their meeting point is the entry of the cycle.
                
        Time: O(n)
        Space: O(1)
    '''
    def detectCycleFloydAlg(self, head: Optional[ListNode]) -> Optional[ListNode]:
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
    def detectCycleNaive(self, head: Optional[ListNode]) -> Optional[ListNode]:
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
