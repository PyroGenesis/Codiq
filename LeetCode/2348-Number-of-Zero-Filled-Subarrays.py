from typing import List


class Solution:
    def zeroFilledSubarray(self, nums: List[int]) -> int:
        def getSubarraysFromZeroCount(zero_count: int) -> int:
            return (zero_count * (zero_count+1)) // 2
        
        subarrays = 0
        curr_subarray_len = 0
        for i, num in enumerate(nums):
            if num == 0:
                curr_subarray_len += 1
            elif curr_subarray_len > 0:
                subarrays += getSubarraysFromZeroCount(curr_subarray_len)
                curr_subarray_len = 0
        subarrays += getSubarraysFromZeroCount(curr_subarray_len)
        
        return subarrays
