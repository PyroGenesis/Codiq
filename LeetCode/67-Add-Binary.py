class Solution:
    def addBinary(self, a: str, b: str) -> str:
        return self.addBinaryWithoutAddition(a, b)
    

    def addBinaryWithoutAddition(self, a: str, b: str) -> str:
        a_rev = reversed(list(a))   # a, going from LSB -> MSB. Note that reversed() will give you an iterator
        b_rev = reversed(list(b))   # b, going from LSB -> MSB. Note that reversed() will give you an iterator
        n1, n2 = len(a), len(b)     # lengths of a and b

        res = []
        carry = 0
        for i in range(max(n1, n2)):
            # the bit-value of a and b at position i
            d_a, d_b = 0, 0

            # since reversed is an iterator, we use next() to get the actual values
            if i < n1 and next(a_rev) == '1':
                d_a = 1
            if i < n2 and next(b_rev) == '1':
                d_b = 1

            # the bit-value of res at position i
            # it is 1 if we have an odd number of 1s in d_a, d_b, carry
            d = d_a ^ d_b ^ carry
            # carry is 1 if at least 2 of d_a, d_b, carry is 1
            carry = (d_a & d_b) | (d_a & carry) | (d_b & carry)
            
            # add the appropriate char to res
            if d == 0:
                res.append('0')
            else:
                res.append('1')
        
        # if there was a carry left at the end, add it as the MSB
        if carry:
            res.append('1')
        
        # reverse the string created to get the final ans
        return ''.join(reversed(res))
    
    '''
    Simple solution
        Start by reversing 
    '''
    def addBinary(self, a: str, b: str) -> str:
        a_rev = reversed(list(a))   # a, going from LSB -> MSB. Note that reversed() will give you an iterator
        b_rev = reversed(list(b))   # b, going from LSB -> MSB. Note that reversed() will give you an iterator
        n1, n2 = len(a), len(b)     # lengths of a and b

        res = []
        carry = False
        for i in range(max(n1, n2)):
            # The 'value' at this position
            d = 0

            # since reversed is an iterator, we use next() to get the actual values from a_rev and b_rev
            if i < n1 and next(a_rev) == '1':
                d += 1
            if i < n2 and next(b_rev) == '1':
                d += 1
            
            # add existing carry and reset it
            if carry:
                d += 1
                carry = False
            
            # set new carry
            carry = d > 1
            # set the bit value here
            if d == 0 or d == 2:
                res.append('0')
            else:
                res.append('1')
        
        # if there was a carry left at the end, add it as the MSB
        if carry:
            res.append('1')
        
        # reverse the string created to get the final ans
        return ''.join(reversed(res))
