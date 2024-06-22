from typing import List


class Solution:
    '''
    Binary Search
        Given a day, we can easily check if we can create k bouquets of m flowers
        So we can use binary search to solve this problem
    
    Intuition for why this is a binary search problem:
        1. Clear boundary between invalid and valid answer
            Eg: bloomDay = [1,10,3,10,2], m = 3, k = 1
                day         0   1   2   3   4   10
                bouquets    0   1   2   3   3   5
                            <3  <3  <3  3   >=3 >=3
                              invalid   Ans Suboptimal
        2. Proper upper and lower bounds
            Lower Bound: Since we need at least one flower, our ans cannot be less than the first day a flower blooms
            Upper Bound: At most we need all flowers, so our ans cannot be larger than the last day a flower blooms
        3. Any answer can help us eliminate the left or right half of search space
            If day d blooms enough flowers to make k bouquets, 
                days d+1, d+2 ... upper-bound will all be suboptimal and can be eliminated
            If day d does not bloom enough flowers to make k bouquets, 
                lower-bound ... d-1, d will also not be enough and can be eliminated
    
    Let n -> number of flowers
        d -> range of first bloom day to last bloom day
    
        Time:  O(n log d)
            1. binary search on bloom day range: O(log d)
            2. check a day to see if we can create k bouquets: O(n)
            (2) for every (1): O(n log d)
            
        Space: O(1)
            only some variables used
    '''
    def minDays(self, bloomDay: List[int], m: int, k: int) -> int:
        # if we need more flowers than possible, quit early
        max_flowers = len(bloomDay)
        if m*k > max_flowers:
            return -1
        
        # checks whether we can make enough bouquets on a particular day
        def checkDay(day: int) -> bool:
            nonlocal m, k
            curr_count = 0
            bouquets_needed = m

            for flower_bloom_day in bloomDay:
                # if flower has bloomed, add it to our count of adjacent bloomed flowers
                # otherwise, reset it
                if day >= flower_bloom_day:
                    curr_count += 1
                else:
                    curr_count = 0
                
                # if we can make a bouquet now with the adjacent bloomed flowers found, do it
                if curr_count == k:
                    curr_count = 0
                    bouquets_needed -= 1
                    # early exit so that we don't need to check the rest of the flowers
                    if bouquets_needed == 0: break
            
            return bouquets_needed == 0

        # binary search between first bloom day and last bloom day
        lo, hi = min(bloomDay), max(bloomDay)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if checkDay(mid):
                # if mid day has enough flowers bloomed, it could be our result
                # or we could do better
                hi = mid
            else:
                # if mid day doesn't have enough flowers bloomed,
                # our ideal day is definitely after it
                lo = mid + 1
        
        return lo
