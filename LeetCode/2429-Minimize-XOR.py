class Solution:
    """
    Time:  O(log(n)) = O(32) = O(1)
    Space: O(1)
    """

    def minimizeXor(self, num1: int, num2: int) -> int:
        return self.minimizeXorSinglePass(num1, num2)

    def minimizeXorSinglePass(self, num1: int, num2: int) -> int:
        """One pass but less readable than the two pass method"""
        # get the number of bits in num2
        # I destroy num2 here but idc
        bits_to_set = 0
        while num2:
            bits_to_set += 1
            num2 &= num2 - 1

        # the final XORed num
        x = 0

        # in first pass we try to invert as many set bits as possible in num1 starting from msb
        # at the same time, we can decide to invert a non-set bit if we find that we won't have
        #   enough bits to fulfill the bit requirement later
        for pos in range(31, -1, -1):
            # quit early if we've satisfied the bit requirement
            if bits_to_set == 0:
                break
            mask = 1 << pos
            bits_left = pos + 1
            # if we have enough positions ahead to fulfill bit requirement AND
            #   the current bit is 0, skip it
            if bits_left > bits_to_set and mask & num1 == 0:
                continue
            x |= mask
            bits_to_set -= 1

        return x

    def minimizeXorTwoPass(self, num1: int, num2: int) -> int:
        # get the number of bits in num2
        # I destroy num2 here but idc
        bits_to_set = 0
        while num2:
            bits_to_set += 1
            num2 &= num2 - 1

        # the final XORed num
        x = 0

        # in first pass we try to invert as many set bits as possible in num1 starting from msb
        for pos in range(31, -1, -1):
            # quit early if we've satisfied the bit requirement
            if bits_to_set == 0:
                break
            mask = 1 << pos
            # if the current bit is 0, skip it
            if mask & num1 == 0:
                continue
            x |= mask
            bits_to_set -= 1

        # in second pass we fulfill the rest of the bit requirement from the lsb
        for pos in range(31 + 1):
            # quit early if we've satisfied the bit requirement
            if bits_to_set == 0:
                break
            mask = 1 << pos
            # if the current bit is 1, skip it
            if mask & num1 != 0:
                continue
            x |= mask
            bits_to_set -= 1

        return x
