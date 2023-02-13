# Leetcode imports
from typing import List

# My imports
import math

class Solution:
    '''
        Brute-force: TLE (no surprises there)
            Increasing k one by one until it satisfies the condition
            O(n*m) where    n -> number of piles
                            m -> max number of bananas in a pile (highest / worst eating speed)
    '''
    
    '''
        Binary search
        Let's say Koko needs to eat bananas at rate x which is min optimal before the guards return
        There is a limited eating range starting at 1 and ending at max(bananas in a pile)
        Therefore all rates 1 ... x-1 will be too slow but rates x ... max(bananas in a pile) will be satisfactory
            out of which x will be the optimal
        Given a linear searching space, this boundary gives us a good basis to run binary search on Koko's speed
        Note:   A slow rate must be discarded since its an invalid rate, but a fast one will be kept under consideration,
                (fast+1 ... will be removed however) because that might be the optimal fast rate
                
        Time:  O(nlogm), n -> len(piles), m -> max speed OR range of speed (1 ... max(piles))
        Space: O(1)
    '''
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        # sanity checks
        # if no piles, no eating
        if not piles:
            return 0
        # If we get 1 hour per pile, we have to use max speed
        if h == len(piles):
            return max(piles)
        # If we get 1 hour per banana, we can use that speed
        if h >= sum(piles):
            return 1
        
        # utility fn to calc all piles consumption time for given speed
        def calcHoursTaken(speed):
            nonlocal piles
            hours_taken = 0            
            for bananas in piles:
                hours_taken += math.ceil(bananas / speed)
            return hours_taken
        
        # binary search
        lo, hi = 1, max(piles)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            hours_taken = calcHoursTaken(mid)
            if hours_taken > h:
                # this speed is too slow
                lo = mid + 1
            else:
                # this speed is good (possible but might not be optimal)
                hi = mid
            # The reason we don't return on hours_taken == h is because this is a minimization problem
            # We need mid to try and go lower even if we have a mid which satisfies h
            # else:
            #     return mid
        
        # return optimal speed
        return lo
    
    '''
        Skipped (To-Do):
            A O(nlogn) solution using a priority queue and assigning hours in proportion with pile size
            Might be more time efficient than binary search but with a greater space complexity O(n)
            https://leetcode.com/problems/koko-eating-bananas/solution/1226924
    '''