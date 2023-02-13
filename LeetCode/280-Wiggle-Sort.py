from typing import List

class Solution:
    def wiggleSort(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        self.wiggleSortGreedy(nums)
    
    def wiggleSortGreedy(self, nums: List[int]) -> None:
        n = len(nums)

        direction = +1
        for i in range(n-1):
            diff = nums[i+1] - nums[i]
            if (direction > 0 and diff < 0) or (direction < 0 and diff > 0):
                # swap
                nums[i], nums[i+1] = nums[i+1], nums[i]
            # change direction
            direction *= -1
    
    '''
    Swap all pairs of odd-even indices starting from 1
    '''
    def wiggleSortSimple(self, nums: List[int]) -> None:
        n = len(nums)
        nums.sort()

        for i in range(2, n, 2):
            nums[i], nums[i-1] = nums[i-1], nums[i]
    
    '''
    Swap with bit-manipulation
    '''
    def wiggleSortBitManip(self, nums: List[int]) -> None:
        n = len(nums)
        nums.sort()
        BITS = 14
        i, j = 0, n-1

        for k in range(n):
            if k%2 == 0:
                nums[k] |= (nums[i] & 0x3fff) << BITS
                i += 1
            else:
                nums[k] |= (nums[j] & 0x3fff) << BITS
                j -= 1
        
        for k in range(n):
            nums[k] >>= BITS
    
