class Solution:
    '''
        Note for this problem in Java:
        In Java Integer type is signed and there is no unsigned int. So the input 2147483648 is represented in Java as -2147483648 (in java int type has a cyclic representation, that means Integer.MAX_VALUE+1==Integer.MIN_VALUE).
        
        This forces us to use: n != 0
        in the while condition and we cannot use n > 0
        because the input 2147483648 would correspond to -2147483648 in java and the code would not enter the while if the condition is n>0 for n=2147483648.
    '''
    def hammingWeight(self, n: int) -> int:
        # the most basic one: bin(n).count('1') but not good for interview        
        return self.hammingWeightEfficient(n)
    
    '''
    Using the bits to count the bits -> Most efficient solution
        First of all, a fact: Each number n, is perfectly capable of keeping its bit count in itseld
        For example, number of 1s in 1 bit num can be held in 1 bit
                     number of 1s in 2-3 bit num can be held in 2 bits
                     number of 1s in 32 bit num can be held in 6 bits
        Therefore, with some creative bit-shifts and addition, we can use the same num to count the bits in itself
        More explanation: 
            https://en.wikipedia.org/wiki/Hamming_weight#Efficient_implementation
            https://leetcode.com/problems/number-of-1-bits/discuss/1044775/Python-n-and-(n-1)-trick-%2B-even-faster-explained
            
        Time:  O(log(no. of bits)) = O(log 32) = O(5) = O(1)
        Space: O(1)
    '''
    def hammingWeightEfficient(self, n: int) -> int:
        # Before we do anything, each bit in num will contain the number of 1s in that 1-bit group
        #   For example, bit 3 in 10110 is 1, indicating that the group of bits (bit 3 to bit 3) has a single 1
        #   I know this is like saying the water is water, but it's important for you to understand future steps
        
        # Now, we pair up 2 adjacent bits and add up their counts
        #   n & 01      will give us the bit at 0th pos in group
        #   (n>>1) & 01 will give us the bit at the 1st pos in group
        # We use 0x55555555 -> 0b01010101010101010101010101010101
        n = (n & 0x55555555) + ((n >> 1) & 0x55555555)
        # Now each 2-bit group has the number of 1 bits in that group
        #   Example | 0 1 | 1 1 | 1 0 | -> 01 10 01 (1st/3rd group -> 1, 2nd group -> 2)
        
        # Now, we can pair up adjacent 2-bit groups and add up their counts to get the number of bits in 4-bit groups        
        #   n & 0011        will give us the count of the lower 2-bit group
        #   (n>>2) & 0011   will give us the count of the upper 2-bit group
        # We use 0x33333333 -> 0b00110011001100110011001100110011
        n = (n & 0x33333333) + ((n >> 2) & 0x33333333)
        # Now each 4-bit group has the number of 1 bits in that group
        #   Example | 01 10 | 01 01 | -> 0011 0010 (1st group -> 3, 2nd group -> 2)
        
        # We do the above steps again, combining adjacemt 4-bit groups into an 8-bit group
        # We use 0x0f0f0f0f -> 0b00001111000011110000111100001111
        n = (n & 0x0f0f0f0f) + ((n >> 4) & 0x0f0f0f0f)
        
        # We do the above steps again, combining adjacemt 8-bit groups into a 16-bit group
        # We use 0x00ff00ff -> 0b00000000111111110000000011111111
        n = (n & 0x00ff00ff) + ((n >> 8) & 0x00ff00ff)
        
        # Finally, We do the above steps once last time, combining adjacemt 16-bit groups into a 32-bit group
        # We use 0x0000ffff -> 0b00000000000000001111111111111111
        n = (n & 0x0000ffff) + ((n >> 16) & 0x0000ffff)
        
        # If we had, say a 64-bit integer, we would do more steps here
        
        # return our processed count
        return n
    
    
    '''
    Invert last bit
        The idea here is to only iterate the number of times 1 actually occurs in bits
        But how do we do that without iterating through all bits?
        If we have number n, then n & (n-1) will remove the rightmost in binary representation of n.
        For example if n = 10110100, then n & (n-1) = 10110100 & 10110011 = 10110000, where & means bitwize operation AND
        Complexity: O(no. of 1 bits) = O(1), O(1)
    '''
    def hammingWeightSmart(self, n: int) -> int:
        hamming_weight = 0
        while n > 0:
            hamming_weight += 1
            n &= (n-1)
        return hamming_weight
        
    '''
    Count every bit
        The solution here checks every bit for the occurences of 1s
        This can be done either by shifting directly or by masking
        Complexity: O(32) = O(1), O(1)        
    '''
    def hammingWeightCheckEveryBit(self, n: int) -> int:
        # direct shifting
        hamming_weight = 0
        while n > 0:
            hamming_weight += n & 1
            n = n >> 1
        return hamming_weight
        
        # masking
        hamming_weight = 0
        mask = 1
        for _ in range(32):
            if (n & mask) > 0:
                hamming_weight += 1
            mask <<= 1
        return hamming_weight
