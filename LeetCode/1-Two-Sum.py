# LeetCode imports
from typing import List


class Solution:
    '''
    Skipped:
        Brute Force
            Guide: for every num, add it to every other num and see if the result is target
            O(n^2), O(1)
            
        Two-Pass hash table
            Guide:
                Make hashmap of num -> idx of entire list
                Now check if complement (target-num) shows up for every num in hashmap
                Since n1 and n2 (where n1 + n2 = target) can't be the same,
                    no need to account for dups
            O(n), O(n)
    '''
    
    '''
        Initial, Optimal
        One pass hash table solution
        Keep hashmap of num -> idx while iterating
        If complement (target-num) shows up, we're done.
        
        Time:  O(n)
        Space: O(n)
    '''
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        numsMap = {}
        for i,num in enumerate(nums):
            if target-num in numsMap:
                # if the complement already seen earlier
                return [numsMap[target-num], i]
            else:
                numsMap[num] = i
                
                