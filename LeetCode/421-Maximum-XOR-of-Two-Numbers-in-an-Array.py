# Leetcode imports
from typing import List


class Solution:
    '''
        Assumptions:
            It will always be (largest)^(smallest) -> Disproved by [7,8,3]
            It will always be (largest)^(second-largest) -> Disproved by [3, 10, 5, 25, 2, 8]
            Largest number will always be involved -> Disproved by [10,8,7]
            Smallest number in largest bracket ^ Largest number in smaller bracket -> Disproved by [10,9,4]
            
        I couldn't figure out this one. :(    
    '''
    def findMaximumXOR(self, nums: List[int]) -> int:
        return self.findMaximumXORTrie(nums)
    
    
    '''
        Trie Soln - Kinda simpler than soln 1
        The idea is simple, the max an xor of a number can be is with its bitwise opp number.
        That means wherever the number has a 1, it has a 0 and vice-versa
        This will at best result in a number with bits 1*L (max: 2^31 - 1 = 1*30)
        The best way to follow this particular path is by converting it to a tree, specifically a bitwise trie.
        
        We could do this by first creating the trie with all nums then iterating through nums for its best partner and keeping track of the max XOR
        But why do it in 2 pass? We can keep checking for the best partner WHILE we are inserting it into the trie in 1 pass
        The symmetric nature of this problem will ensure that the 2nd partner will always be able to catch its best 1st partner, even tho the 1st partner will not be able to do the same (bcoz 2nd partner doesnt exist in trie yet)
        
        Time:   Outer loop runs for each num and inner loop runs for each bit of that num (max: 31)
                Therefore, O(n*31) = O(n)
        Space:  Same dumb logic in write-up as in soln 1. I say its O(n)
    '''
    def findMaximumXORTrie(self, nums: List[int]) -> int:
        # sanity check
        if len(nums) < 2:
            return 0
        if len(nums) == 2:
            return nums[0]^nums[1]
        
        # we are finding the min number of bits that can represent all nums
        # We do that by converting the max num into binary, then do -2 for the '0b' prefix
        nBits = len(bin(max(nums))) - 2
        max_xor = 0
        trie = {}
        
        # we do both trie creation and max_xor check in 1 pass
        for num in nums:
            insertionNode = trie    # the node where the new entry will be added to
            xorNode = trie          # the node where the best partner of current lies
            max_xor_with_num = 0    # value of curr XOR best partner
            bits = [(num>>i) & 1 for i in range(nBits-1, -1, -1)]
            
            for bit in bits:
                # inserting into the trie
                if bit not in insertionNode:
                    insertionNode[bit] = {}
                insertionNode = insertionNode[bit]
                
                # computing max possible xor with this number by trying to move the opposite way of it's bit value
                # oppBit: 0 -> 1 and 1 -> 0
                oppBit = 1 - bit
                
                # ready the current XOR for a new bit
                max_xor_with_num <<= 1
                # try to move opp way but if cant, move the only way possible
                if oppBit in xorNode:
                    xorNode = xorNode[oppBit]
                    max_xor_with_num |= 1
                else:
                    # no choice
                    xorNode = xorNode[bit]
                
            # keep track of max_xor
            max_xor = max(max_xor, max_xor_with_num)
        
        return max_xor
                
                
        
    '''
        This is kind-of a greedy solution
        Starting from the MSB bit, we iterate through the prefixes of size 1 ... max (worst case: 31)
        So, for a 4 bit num, we would try the prefixes
            (1***), (11**), (111*), (1111)
        Each time we try to get the LSB of the prefix to be 1, and check in prefixes if there are 2 prefixes that satisfy that cond
        If yes, then we set that bit to 1
        If no, we leave the bit to be 0
        So in actuality the prefixes might go something like:
            (1***), [failed] (10**), (101*), [failed] (1010)
        The beauty of the problem is that each time we are sure that all the bits to the left of the LSB in the bestPrefix to be possible since we verified them each when they were LSBs
        
        Concern 1: How is the prefix method guaranteed to get the max?
            Due to the nature of bits, a bit set to 1 is greater than all of its lower order bits set to 1 simultaneously
            Eg: 1000 > 0111
            Therefore, by prioritizing the MSBs at all costs, we guarantee that the resultant XOR will be the max
        Concern 2: Let's say prefix is (11**), how do we know (110*) is possible if (111*) is not
            There are atleast 2 nums in prefix. Now lets take 2 bits a and b
            That gives us 4 combinations 00, 01, 10, 11
            If the combinations are 01 or 10, bestPrefix will be satisfied and max_xor will be updated
            The remaining two combinations (00 and 11) are guaranteed to give us a 0 there
            Basically, since there is no third possibility, if 1 is not possible, 0 is guaranteed to be possible
        Concern 3: What if 2 diff nums made earlier prefix and 2 later nums made the later one?
            This is kinda correct. One set of nums might make the initial prefix and another set the later ones
            However, since we check the entire prefix and not just the new prefix bit, if another set does make the later ones
                they are guaranteed to make the first set of prefixes as well.
            Therefore at any time, a prefix might be possible by multiple sets of nums, but no new set can make later
                prefixes if they do not already made the earlier prefixes
        
        Time:   Outer loop runs for each bit and inner loop runs for all numbers
                Therefore, O(31*n) = O(n)
        Space:  The only considerable space taken is in prefixes.
                Now the write-up says that this is O(1), which is dumb.
                If nums contain all possible numbers (0 ... 2^31), for prefixes of size 31, we will get 
                    all the numbers in the prefixes set
                Saying O(1) means saying that num cant be +inf so space is constant.
                NO, space is O(n)
    '''
    def findMaximumXORSet(self, nums: List[int]) -> int:
        # sanity check
        if len(nums) < 2:
            return 0
        if len(nums) == 2:
            return nums[0]^nums[1]
        
        # we are finding the min number of bits that can represent all nums
        # We do that by converting the max num into binary, then do -2 for the '0b' prefix
        nBits = len(bin(max(nums))) - 2
        
        max_xor = 0
        
        # for prefixes from len -> 1 to full-size
        for prefixLen in range(1, nBits+1):
            # the number of right shifts needed to get to that prefix
            rightShifts = nBits - prefixLen
            
            # shifting max_xor to process new bit
            # note that this number is assumed to be possible but I'm still not sure why that is
            # maybe we try for the best -> 1, but if we dont get that the 2nd and only other option must be possible
            # though I cant make a case where 0 is NOT possible
            # UPDATE: 0 case is explained above in docstring
            max_xor <<= 1
            
            # best possible prefix
            bestPrefix = max_xor | 1
            
            # computing all possible prefixes
            prefixes = {num >> rightShifts for num in nums}
            
            # Now see if best prefix is possible
            # If bestPrefix is possible:
            #               p1 ^ p2 = bestPrefix
            # Therefore,    p1 ^ bestPrefix = p2
            # OR            p1 ^ bestPrefix in prefixes
            for p1 in prefixes:
                if p1^bestPrefix in prefixes:
                    # bestPrefix is possible so we update max_xor
                    max_xor |= 1
                    break
            # bestPrefix is not possible so we leave the max_xor with a 0
        
        return max_xor