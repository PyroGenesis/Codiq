from typing import List

# My import
from collections import defaultdict

class Solution:
    '''
    This is just 2-sum with a counter
    '''
    def maxOperations(self, nums: List[int], k: int) -> int:
        return self.maxOperationsHashmap(nums, k)
    
    '''
    Hashmap, One pass, Time optimal    
        For every element current, we must first try to find if its complement exists in the hashmap. 
        If it does, there is no need to add the current element to the map and we could simply remove the 
            complement element from the hashmap and increment the counter. 
        Otherwise, add the current element to the map, so that it can be possibly paired with some future element.
        
        Time:  O(n) [We iterate over every element only once]
        Space: O(n) [hashmap]
    '''
    def maxOperationsHashmap(self, nums: List[int], k: int) -> int:
        # keeps the count of the previously seen UNMACTCHED numbers
        count = defaultdict(int)
        
        # number of 2-sum pairs found
        matches = 0
        for num in nums:
            if count[k - num] > 0:
                # if there is an unmatched num previously seen that forms a 2-sum pair with this number,
                #   skip adding the current num into the hashmap, remove the complement from the hashmap,
                #   inc the 2-sum pair count
                matches += 1
                count[k - num] -= 1
            else:
                # if there is no unmatched num previously seen that is the complement of this number,
                #   add this num to the hashmap for future numbers to check with
                count[num] += 1
        
        # return the number of 2-sum pairs found
        return matches
    
    '''
    Two-pointer, Space optimal
        In a sorted array, we know that for every ith element, 
            the value of (i+1)th element would always be greater than or equal it's own value, AND
            the value of (i-1)th element would be less than or equal to its value

        We can use 2 pointers, 
            the first pointer i, is positioned at 0th index of the array, and 
            the second pointer j, is positioned at (n-1)th index of the array

        The value of the sum of the ith and jth elements can be used to determine where a possible pair could lie,
         - If sum < k, we know that we want a larger value, 
           hence we can increment the i by 1 to get a little larger value.
         - Else, if sum > k, we know that we want a smaller value,
           hence we can decrement the j by 1 to get a little smaller value.
         - Otherwise, sum == k and we have found one pair of elements pointed by i and j. 
           We can increment i and decrement j to find the next pair.
        Iterate until we meet in the middle, i == j

        Time:  O(nlogn) [sort]
        Space: O(1)
    '''
    def maxOperationsPointers(self, nums: List[int], k: int) -> int:
        nums.sort()             # sort the numbers
        i, j = 0, len(nums)-1   # pointers starting from the first and last numbers
        
        # number of 2-sum pairs found
        matches = 0
        while i < j:
            # total of the current 2 numbers
            total = nums[i] + nums[j]
            if total < k:
                # there is no num large enough to pair with the num at i
                # (or it is already paired up)
                i += 1
            elif total > k:
                # there is no num small enough to pair with the num at j
                # (or it is already paired up)
                j -= 1
            else:
                # found a matching pair! Skip both nums at i and j now so that they won't be paired again
                matches += 1
                i += 1
                j -= 1
        
        # return the number of 2-sum pairs found
        return matches
