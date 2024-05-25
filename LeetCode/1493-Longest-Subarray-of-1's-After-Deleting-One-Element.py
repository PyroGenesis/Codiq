from typing import List

class Solution:
    '''
    Skipped
        Editorial Sliding Window
            My solution is much more efficient than this one
            Maybe not in terms of time/space complexity, but in terms of the constant
    '''

    '''
    Subarray count tracking
        The idea is to keep track of the number of contiguous 1s before a separator 0 and after
        Then when we encounter another 0,
            We record before count + after count in a max variable
            After that we set before count to after count and after count to 0
        We need to check one last time after the loop if the arr ended with a 1 subarray
        If there were no zeroes, subtract 1 from the max count since we lose a 1
        Return the max count
    
        Time:  O(n)
        Space: O(1)
    '''
    def longestSubarray(self, nums: List[int]) -> int:
        prev_subarr, curr_subarr = 0, 0     # before and after 0 1-subarray counts
        max_subarr = 0                      # max count
        NO_ZEROES = True                    # assume no 0s initially

        for num in nums:
            if num == 1:
                # inc curr subarray count
                curr_subarr += 1
            else:
                # there exists a 0
                NO_ZEROES = False
                # set max subarray count appropriately
                max_subarr = max(max_subarr, prev_subarr + curr_subarr)
                # reset counts for next pair
                prev_subarr, curr_subarr = curr_subarr, 0
        
        # do it one last time for the final 1-subarray at the end of the array
        max_subarr = max(max_subarr, prev_subarr + curr_subarr)
        # lose a 1 if there are no 0s
        if NO_ZEROES: max_subarr -= 1

        return max_subarr
