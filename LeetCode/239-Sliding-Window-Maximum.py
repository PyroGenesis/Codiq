from collections import deque
from typing import List

class Solution:
    '''
    Basically we keep a queue of the numbers that have the potential to become the max in their sliding window.
    Now, one thing you have to notice is that if a num, say x is considered to be in current window, 
        no num y where (y <= x) and y comes before x will ever be considered as a max of the window.
    On the other hand, num z where (z <= x) and z comes after x will be considered 
        (in the case where x drops out of window range)

    Therefore our queue achieves a state where the first element is the max of the window
        (also the one which will be ejected from the queue earliest as the window moves)
    The rest of the elements are successors of their previous elements, 
        ready to take their predecessor's place as the max in the window, if their predecessor falls out of the window range
    
    In general, whenever we encounter a new element x, we want to discard all elements that are less than x before adding x. 
    Let's say we currently have [63, 15, 8, 3] and we encounter 12. 
        Any future window with 8 or 3 will also contain 12, so 8 and 3 can no longer be window max and we can discard them. 
        After discarding them and adding 12, we have [63, 15, 12]. 
    As you can see, this ensures that we keep elements in descending order.
    This also ensures that the max of a window is simply the first value in the queue

    Time:  O(n)
        Every num is pushed and popped from the queue at most 1 time
    Space: O(k)
        The queue size will be k at maximum
    '''
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # if window size is 1, every element is its own window max
        if k==1:
            return nums

        n = len(nums)
        
        # The max of every window (the answer)
        maxes = []
        # The queue of consecutive maxes (should the max move out of range)
        queue_of_maxes: deque[int] = deque()

        # go through every number
        for j in range(n):
            # if we encounter a value that exceeds values currently in the queue,
            # all values <= current get ejected as they are no longer valid candidates for windoe max
            while queue_of_maxes and nums[queue_of_maxes[-1]] <= nums[j]:
                queue_of_maxes.pop()
            # add current value as potential window max (should all values to the left of it move out of window range)
            queue_of_maxes.append(j)

            # if we haven't encountered nums == window size, continue to next number
            if j < k-1:
                continue
            # if our largest queue member is out of window range, pop it out
            if queue_of_maxes[0] <= j-k:
                queue_of_maxes.popleft()

            # record the max value for this window
            # by this window, I mean the window ending at index j (j-k+1 to j)
            maxes.append(nums[queue_of_maxes[0]])
        
        # return the recorded maxes
        return maxes
