# LeetCode imports
from typing import List

class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        return self.threeSumClosest2Pointers(nums, target)
    
    def threeSumClosest2Pointers(self, nums: List[int], target: int) -> int:
        n = len(nums)
        closest = float('inf')
        best_diff = float('inf')
        
        nums.sort()
        
        for num1 in range(n-2):
            num2 = num1 + 1
            num3 = n - 1
                        
            while num2 < num3:                
                s = nums[num1] + nums[num2] + nums[num3]
                diff = abs(target - s)
                if diff < best_diff:
                    best_diff = diff
                    closest = s
                
                if s < target:
                    num2 += 1
                elif s > target:
                    num3 -= 1
                else:
                    return s
        
        return closest
                
    
    '''
        Initial, Brute-force
        Basically keep track of unique single nums and unique sums of 2 nums prior
            We also keep track of the closest value to target and its diff
        Iterate from 3rd num to end
        Consider it as 3rd num
            Add with every prior unique sum to see if it gets any closer to target
        Consider it as 2nd num
            Iterate over the unique single nums and save its addition in unique sums
        Consider it as 1st num
            Add to unique single nums
        Return the closest num to target found
        
        Time:  O(n^3) ... I think
               Consider as num1: O(1)
               Consider as num2: O(1+2+3+ ... +n) = O(n^2)
               Consider as num3: O(1C2 + 2C2 + ... + nC2) = O(n^3)
        Space: O(n^2)
               for all 2-combinations
    '''
    def threeSumClosestOptimizedBruteForce(self, nums: List[int], target: int) -> int:
        singles = set(nums[:2])
        doubles = set([sum(nums[:2])])
        closest = float('inf')
        best_diff = float('inf')
        
        for i in range(2, len(nums)):
            num3 = nums[i]
            for num12 in doubles:
                s = num12 + num3
                diff = abs(target - s)
                
                if diff < best_diff:
                    closest = s
                    best_diff = diff
                    
                    if best_diff == 0:
                        return closest
            
            doubles.update([num1+num3 for num1 in singles])
            singles.add(num3)
        
        return closest
                