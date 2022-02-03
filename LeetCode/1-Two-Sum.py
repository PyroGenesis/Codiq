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
            
        Pointers in sorted list
            Here, we first sort the original array (while keeping the idx record), then initialize 2 pointers at start and end
            1. If num[start]+num[end] > target, start++
            2. If num[start]+num[end] < target, end--
            3. If num[start]+num[end] == target, nums found
            This is actually the solution for Two Sum II 
                (it might not be optimal right away but it can be very useful for followup questions)
            The reason this works is:
                If case 1 happens, that start cannot be part of the solution because even with the highest possible value for end
                    (provided that num[start]+num[end] do not exceed target), num[start] is too low
                If case 2 happens, that end cannot be part of the solution because even with the smallest possible value for start
                    (provided that num[start]+num[end] is not less than target), num[end] is too high
            O(nlogn), O(n)
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
                
                