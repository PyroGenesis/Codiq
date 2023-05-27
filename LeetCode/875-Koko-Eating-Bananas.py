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
    Binary Search
    Simply conduct binary search with calculating hours taken at every mid to arrive at the optimal answer

    Intuition for why this is a binary search problem:
        1. Clear boundary between invalid and valid answer
            Eg: piles: [3,6,7,11], h: 8
                speed       2       3    4      5          6
                hours      15      10    8      8          6
                        Invalid invalid Ans Suboptimal Suboptimal
        2. Proper upper and lower bounds
            Lower Bound
                At the slowest pace, Koko will eat at exactly total_bananas / h speed
                Therefore, min speed = sum(piles) // h (OR ceil(sum(piles) / h))
            Upper Bound
                At the fastest pace, Koko will eat every pile in exactly 1 hour
                Therefore, max speed = max(piles)
        3. Any answer can help us eliminate the left or right half of search space
            If speed s is enough to consume all piles within h hours, 
                speeds s+1 ... upper-bound will all be suboptimal and can be eliminated
            If speed s is not enough to consume all piles within h hours, 
                lower-bound ... s will also not be enough and can be eliminated

    Time Complexity: O(n * log(m))
        Let n -> len(piles)
        Let m => range of speeds (hi - lo)
        Get initial lo: O(n)
        Get initial hi: O(n)
        Calculating hours taken for particular speed: O(n)
        Therefore, total time complexity:
            O(n + n + nlogm)
            O(n * log(m))

    Space complexity: O(1)
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
                # used 2 statements instead of math.ceil(bananas / speed) 
                #   to prevent float-precision error from getting round up
                hours_taken += bananas // speed
                if bananas % speed > 0:
                    hours_taken += 1
            return hours_taken
        
        # Technically, this speed needs to be ceil(total_bananas / h) but 
        #   the difference between that and total_bananas // h is 1 so it doesn't matter
        lo = sum(piles) // h
        hi = max(piles)

        # binary search
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if calcHoursTaken(mid) <= h:
                # this speed is good (possible but might not be optimal)
                hi = mid
            else:
                # this speed is too slow
                lo = mid + 1
            # The reason we don't return on hours_taken == h is because this is a minimization problem
            # We need mid to try and go lower even if we have a mid which satisfies h
        
        # return optimal speed
        return lo
