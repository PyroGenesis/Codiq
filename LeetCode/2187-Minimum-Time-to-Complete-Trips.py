from typing import List

'''
Binary Search
Simply conduct binary search with calculating total trips at every mid to arrive at the optimal answer

Intuition for why this is a binary search problem:
    1. Clear boundary between invalid and valid answer
        Eg: Time: [1,2,3], totalTrips: 5
            minTime     1       2    3      4          5
            trips       1       3    5      7          8
                    Invalid invalid Ans Suboptimal Suboptimal
    2. Proper upper and lower bounds
        the minimum amount of time = the amount of time taken by fastest bus to complete 1 trip
        the maximum amount of time = the amount of time taken by fastest bus to complete all trips
    3. Any answer can help us eliminate the left or right half of search space
        If time t is enough to do totalTrips, t+1 ... upper-bound will all be suboptimal and can be eliminated
        If time t is not enough to do totalTrips, lower-bound ... t will also not be enough and can be eliminated

Time Complexity: O(n * log(mt * tt))
    Let number of buses be n
    Say fastest bus takes time mt to complete a trip
    Represent totalTrips with the variable tt
    Finding min(time): O(n)
    Binary search range: 
        min(time) to min(time)*totalTrips
        mt to mt*tt
        => mt*tt - mt
        => mt * (tt - 1)
    Calculating total trips for a particular time: O(n)
    Therefore, total time complexity:
        O(n + (n * log(mt * [tt - 1])))
        O(n * log(mt * tt))

Space complexity: O(1)
'''
class Solution:
    def minimumTime(self, time: List[int], totalTrips: int) -> int:
        # utility fn to get the total number of trips possible with a given time
        def getTotalTrips(t: int) -> int:
            nonlocal time
            trips = 0
            for bus_time in time:
                trips += t // bus_time
            return trips
        
        # lo is set to min(time) because if it is any lower totalTrips will be 0
        #   at least 1 trip made by fastest bus
        lo = min(time)
        # hi is set to min(time)*totalTrips because that is enough 
        #   for the fastest bus to complete all the trips by itself.
        hi = lo * totalTrips

        while lo < hi:
            mid = lo + (hi - lo) // 2
            if getTotalTrips(mid) >= totalTrips:
                # this is a valid time to complete totalTrips trips
                #   keep this value in search space but eliminate anything
                #   greater because that will be suboptimal
                hi = mid
            else:
                # this time is insufficient to complete totalTrips trips
                #   eliminate this time and anything lower from the search space
                lo = mid + 1
        
        # lo == high == ans
        return lo
