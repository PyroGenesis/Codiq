# Leetcode imports
from typing import List

class Solution:
    ''' Optimal
    Bit Manipulation / XOR
        The Guide description is flawless:
        * XOR of a bit with 0 is the same bit
          i.e., x ^ 0 = x
        * XOR of a bit with itself is 0
          i.e., x ^ x = 0
        * Therefore, a ^ b ^ a
                  => (a ^ a) ^ b
                  => 0 ^ b
                  =  b
                  
        This way, all the duplicates will get rid of themselves and the unique num will remain
        (Yes, this rule still works if duplicates are out of order or nested)
        
        One-liner: return reduce(lambda acc, x: acc ^ x, nums)
        
        Time:  O(n)
        Space: O(1)
    '''
    def singleNumber(self, nums: List[int]) -> int:
        xor = 0
        for num in nums:
            xor = xor ^ num
        return xor
    
    '''
    Skipped (Also failures):
        List solution: Dumb
        
        Hashset: 
            Keep Hashset of seen nums. If seen again, remove them. The num left in the hashset will be the ans
            You can also do this with a hashmap/dict instead but get no advantage
            Time: O(n), Space: O(n)
        
        Math:
            Shorter program than Hashset with same time and space complexity, but with a bigger coeff
            If we do 2 * (uniques_sum) - original_sum, we get left with the single occurence num
            return 2 * sum(set(nums)) - sum(nums)
            Time: O(n+n) = O(n), Space: O(n+n) = O(n)
    '''