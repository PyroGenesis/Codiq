# LeetCode import
from typing import List

class NumArray:

    def __init__(self, nums: List[int]):
        self.prefix_sums = []
        curr_sum = 0
        for num in nums:
            curr_sum += num
            self.prefix_sums.append(curr_sum)

    def sumRange(self, left: int, right: int) -> int:
        left_subtract = self.prefix_sums[left-1] if left > 0 else 0
        return self.prefix_sums[right] - left_subtract


# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# param_1 = obj.sumRange(left,right)