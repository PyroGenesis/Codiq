import math

class Solution:
    def minEnd(self, n: int, x: int) -> int:
        bits_to_change = n-1
        mask = 1

        while bits_to_change:
            if x & mask:
                # we cannot change this bit, we need to keep it 1
                pass
            else:
                # we can change this bit, but we only need to if bits_to_change last bit is 1
                if bits_to_change & 1:
                    # bit does need to be changed
                    x |= mask
                # we consumed a bit to change
                bits_to_change >>= 1
            # shift mask to check next bit
            mask <<= 1
        
        return x
