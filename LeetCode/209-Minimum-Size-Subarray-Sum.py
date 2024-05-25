import math
from typing import List


class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        i, j = 0, 0
        total = nums[0]

        min_len = math.inf
        while j < n:
            if total >= target:
                min_len = min(min_len, j - i + 1)
                if min_len == 1: return min_len
                total -= nums[i]
                i += 1
            else:
                j += 1
                if j < n: total += nums[j]
        
        return min_len if min_len != math.inf else 0
