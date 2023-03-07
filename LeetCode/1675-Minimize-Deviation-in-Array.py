import heapq
import math
from typing import List

class Solution:
    '''
    The first thing you need to realize is even though both operations look symmetric,
      they are not really
    This is because when growing a number, you can only do it once (after that it is no longer odd)
    But reducing a number can be done log n times (it can still be even after division)
    For example:
        Initial: 4, 9, 8, 5
        Grow to max:    4, 9 -> 18, 8, 5 -> 10
                        4, 18, 8, 10
        Reduce to min:  4 -> 2 -> 1, 9, 8 -> 4 -> 2 -> 1, 5
                        1, 9, 1, 5
    Therefore, when going for greedy its easier to start by increasing all nums to their max
    Then, we can use a max-heap to reduce and recalc the deviation at each step
    We can be sure this will lead to an optimal ans because we started with the max values possible and eliminated the *2 operation
    And so we were only left with the /2 operation which we applied to the highest always to reduce the deviation
    When we encounter an odd max value, we have reached the limit to which the max deviation can be decreased
    '''
    def minimumDeviation(self, nums: List[int]) -> int:
        # this max-heap will be responsible for reducing the upper-bound of the deviation
        max_heap = []
        # variables to keep track of the current maximum and minimum values
        minimum, maximum = math.inf, -math.inf
        for num in nums:
            # if num is odd, we multiply by 2
            # this ensures that the lower-bound of deviation is as high as possible
            #   therefore we can eliminate increasing lower-bound when trying to greedily reduce to min deviation
            if num % 2 == 1:
                num *= 2
            minimum = min(minimum, num)
            maximum = max(maximum, num)
            # since python heaps are always min heaps, we use -ve value for heap operation
            max_heap.append((-num, num))
        
        heapq.heapify(max_heap)
        min_deviation = maximum - minimum

        # reduce upper bound as much as possible, making sure to recalc the deviation on every step
        # because its not guaranteed that the lower the upper-bound the lower the deviation:
        #   Example: 7, 8 -> deviation = 1
        #            7, 4 -> deviation = 3
        while max_heap[0][1] % 2 == 0 and min_deviation > 0:
            # run loop which largest value is even and deviation is not already 0
            # reduce the max value (divide by 2)
            num = max_heap[0][1]
            num //= 2
            # reassign minimum value, if needed
            minimum = min(minimum, num)
            # put the reduced value back in the heap, overwriting the original
            heapq.heapreplace(max_heap, (-num, num))
            # reassign maximum value
            maximum = max_heap[0][1]
            # recalc deviation
            min_deviation = min(min_deviation, maximum - minimum)
                
        return min_deviation
