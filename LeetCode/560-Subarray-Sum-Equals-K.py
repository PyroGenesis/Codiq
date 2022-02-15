# LeetCode imports
from typing import List

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        return self.subarraySumPrefixSum(nums, k)
    
    '''
    Prefix Sum
    This solution uses the fact that we can recreate any subarray sum just by
        recording sums of all subarrays starting from first element
    For example:
        Consider an array of size n, and we want a subarray [i:j] (inclusive) where 0 <= i <= j < n
        Now, [0:j] = [0:i-1] + [i:j]
        Therefore, [i:j] = [0:j] - [0:i-1]
        This way, any subarray can be represented by two subarrays starting from the beginning of the array
    
    Now that we know that any subarray sum can be recreated like this, we iterate through the nums while keeping
        the count of cumulative sum of every prev sum
    The hashmap will store with the key being any particular sum, and the value being the number of times it has happened
        till the current iteration of the loop as we traverse the array from left to right.
    Why do we keep count but not index?
        index is not needed as if [i:x] and [j:x] both sum to k, we don't really care which one was picked
        but we keep the count, so if there ARE 2 ranges [i:x] and [j:x] which sum to k, we need to count both
    So for a range [0:x] which sums to y, if there exists a prev range [0:i] which sums to y-k, then we found a range
        [i:x] which sums to k
    Note that there might be multiple ranges [0:i] which satisfy y-k which is why we use the count and not just do +1
    
    After inc the count for every time above case happens (inc by freq, not by +1), we will arrive at the final ans
    
    Time:  O(n)
    Space: O(n)
    '''
    def subarraySumPrefixSum(self, nums: List[int], k: int) -> int:
        # we initialize prefix sums with 0: 1 because a subarray of sum=0 is always possible,
        # the sum of []
        prefix_sums = {0: 1}
        total = 0   # cumulative total
        count = 0   # total num of subarray with sum=k found
        
        for num in nums:
            total += num
            diff = total - k
            if diff in prefix_sums:
                count += prefix_sums[diff]
            prefix_sums[total] = prefix_sums.get(total, 0) + 1
        return count
                
    '''
    Brute Force: TLE
    Basically go through all subarrays organized by start idx
        Example: [0], [0,1], [0,1,2] ... [0,1, ... ,n] then [1], [1,2], [1,2,3] ... [1,2, ... ,n] ... finally [n]
    We keep a cumulative sum while iterating forwards from chosen start point
    Whenever the sum equals the required k value, we can update the count value
    
    Time:  O(n^2)
    Space: O(1)
    '''
    def subarraySumBruteForce(self, nums: List[int], k: int) -> int:
        n = len(nums)
        count = 0
        
        # for every subarray start
        for start in range(n):
            total = 0   # reset to 0
            
            # for every subarray end with given start
            for end in range(start, n):
                # keep total updated
                total += nums[end]
                
                # match to criteria
                if total == k:
                    count += 1
        
        return count
        
    '''
    Flawed 2-pointer approach

    Why is this flawed?
        This would only work if all numbers were > 0, which would guarantee 2 things:
        * Expanding the window will increase the sum
        * Contracting the window will decrease the sum

        However, since in this problem there might also be -ve numbers / 0, the above two statements are not guaranteed
        * If a -ve num / 0 is outside on the edge of a window, expanding it might decrease the total
        * If a -ve num / 0 is inside a window, contracting it might increase the total

        Example:
        [-1, 2, -1], k = 2
        Obviously the ans is 1, i.e., [2]
        But the algorithm will not be able to figure this out
            [-1] -> -1 < 2 so expand
            [-1,2] -> 1 < 2 so expand
            [-1,2,-1] -> 0 < 2 so expand (but cannot since max reached)
            ans = 0 OR not possible (incorrect)
    '''
#     def subarraySum(self, nums: List[int], k: int) -> int:
#         n = len(nums)
#         if n==0:
#             return 0
        
#         i=0
#         j=1
#         total = nums[0]
#         ans = 0
#         while j<n:
#             if total == k:
#                 ans += 1
#             elif total < k:
#                 total += nums[j]
#                 j += 1
#             else:
#                 if i<j:
#                     total -= nums[i]
#                     i += 1
#                 else:
#                     total += nums[j]
#                     j += 1
        
#         while i < j:
#             if total == k:
#                 ans += 1
#             else:
#                 total -= nums[i]
#                 i += 1
#         return ans
                