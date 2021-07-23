# Leetcode imports
from typing import List

class Solution:
    '''
        Skipped:
            MaxLeft and MinRight arrays
                O(n), O(n)
                Guide
            MaxLeft and MinRight arrays generated through accumulators (check this out)
                O(n), O(n)
                https://leetcode.com/problems/partition-array-into-disjoint-intervals/discuss/1354458/Python-Two-accumulates-explained
    '''
    
    '''
        Initial and Optimal
        Consider taking the first num as the left partition (len=1)
        Now, as we move towards the right, we need to incorporate all nums < first_num (or max) in the left panel
        If we encounter a num larger than left_max, we don't have to put it in the left partition
            However, what if we encounter a num < left_max after the large num?
                We need to move the partition to the new small num, incorporating the large num
            But in doing so, our left_max might change due to including nums between prev boundary and new boundary
        Therefore, we need to keep track of the global_max as well, so if our boundary moves, we can instantly get the value of the new left_max
        Keep iterating over the rest of nums, and return the length where the boundary lies       
        
        Another great explanation for both Guide and one-pass solutions:
        https://leetcode.com/problems/partition-array-into-disjoint-intervals/discuss/1354396/Python-From-O(N)-space-to-O(1)-space-Picture-explained-Clean-and-Concise
        
        Time:  O(n)
        Space: O(1)
    '''
    def partitionDisjoint(self, nums: List[int]) -> int:
        n = len(nums)
        # sanity check
        if n == 0:
            return 0
        
        left_max = nums[0]      # max of left partition
        global_max = nums[0]    # max of all seen
        partition_length = 1    # current length of partition
        
        for i in range(1, n):
            # every num on left has to be <= right, not < right (common mistake)
            if nums[i] < left_max:
                # partition has to be moved to encompass the new small num
                partition_length = i+1
                # left_max will update since all nums seen became part of left partition
                left_max = global_max
            else:
                # keep track of global max as we move along (in case boundary changes)
                global_max = max(global_max, nums[i])
                
        return partition_length
        
