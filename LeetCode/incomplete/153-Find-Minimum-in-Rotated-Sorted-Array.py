# LeetCode imports
from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]
        
        low, high = 0, n-1
        while low < high:
            if nums[low] < nums[high]:
                # the remaining array is sorted now, so return directly
                return nums[low]
            
            mid = low + (high - low) // 2
            
            # in the end, low == mid so this should be >= and not >
            if nums[mid] >= nums[low]:
                low = mid + 1
            else:
                high = mid
        
        return nums[high]