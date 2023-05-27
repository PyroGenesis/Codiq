import math
from typing import List


class Solution:
    '''
    Binary search
    There are basically 3 factors that help you distinguish this as a binary search problem
        1. There is a clear boundary between valid and invalid capacities
            Example: weights = [1,2,3,4,5,6,7,8,9,10], days = 5
                     capacity = 12 13 14 15  16  17  18
                                >5 >5 >5  5 <=5 <=5 <=5
        2. The answer can be reached by minimization OR maximization
            In the example above, capacity 15, 16, 17 ... all satisfy the 5 days constraint
            But 15 is the minimum capacity to do that and is our answer
        3. There are defined upper and lower bounds for the value
            In this problem, if the capacity == max(weights), each day we will be taking a single package
                Here, a lower capacity is not possible because then the task would become impossible
            Otherwise, if the capacity == sum(weights), we can take all packages in a single day
                Here, a higher capacity is pointless since we can already take all the packages in a single day
    
    The algorithm is simple, we perform binary search on the capacity until we narrow it down to a single value
    The low and high bounds start from max(weights) to sum(weights) as mentioned above
        We can tighten the upper bound as min(total_weight, total_weight/days + max_weight), but eh.
    At every mid value we calc the days with that capacity
        if calc_days > days, we failed the constraint.
            get rid of left half, including mid
        if calc_days <= days, we passed the constraint.
            keep mid value as potential answer but mid+1 and above is rejected
    At the end, we will be left with the single right answer at lo == hi

    Time complexity: O(nlogn)
        Getting max, sum: O(n)
        Getting the days for a particular capacity: O(n)
        Binary search range: max to sum
            since weight is bounded to 500, the range can be at max (500 to n*500)
            which is basically (n-1)*500
        Total complexity:
            Binary search iterations * criteria operation
            [Binary search on range (n-1)*500] * Getting the days for a particular capacity
            log[(n-1)*500] * n
            O(nlogn)

    Space complexity: O(1)
    '''
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        # utility fn that gets the number of days needed to ship all packages when given a capacity
        def getDaysForCapacity(capacity: int) -> int:
            nonlocal weights
            # size of current shipment, current days needed
            shipment, days = 0, 1
            for weight in weights:
                if shipment + weight > capacity:
                    # current package cannot fit into shipment
                    # add it to next day's
                    days += 1
                    shipment = weight
                else:
                    # add package to current shipment
                    shipment += weight
            return days
        
        # utility fn to calc max and sum in a single loop
        def maxsum(arr):
            m, s = -math.inf, 0
            for v in arr:
                m = max(m, v)
                s += v
            return m, s
                
        
        lo, hi = maxsum(weights)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if getDaysForCapacity(mid) <= days:
                # we keep mid since it is a potential answer
                # mid+1 and above, however, are not
                hi = mid
            else:
                # this mid failed the constraint
                # it and anything below it must be rejected
                lo = mid + 1

        # lo == hi == ans
        return lo
