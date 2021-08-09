# My import
from itertools import zip_longest

class Solution:
    '''
        Skipped:
            Solution without zip_longest: Guide
            This is a good way to do the loop without zip_longest
                p1 = len(num1) - 1
                p2 = len(num2) - 1
                while p1 >= 0 or p2 >= 0:
                    x1 = cint(num1[p1]) if p1 >= 0 else 0
                    x2 = cint(num2[p2]) if p2 >= 0 else 0
    '''
    
    
    '''
        Initial, Optimal, Only Solution
        Basically do digit by digit addition (zip_longest makes this really easy)
        To convert single char digit to int digit use ord diff
        
        Time:  O(max(num1, num2))   [for the loop]
        Space: O(max(num1, num2))   [for the ans]
    '''
    def addStrings(self, num1: str, num2: str) -> str:
        # sum, carry
        s, c = 0, 0
        # fn to convert single char digit to int digit
        cint = lambda d: ord(d) - ord('0')
        # the ans
        sum_arr = []
        
        # go through both strings in reverse, filling in '0's for the mismatched lengths
        # reversed and zip just create iterators, not copies, making this efficient
        for d1, d2 in zip_longest(reversed(num1), reversed(num2), fillvalue='0'):
            # do the single digit add and add it to the ans
            digit_sum = cint(d1) + cint(d2) + c
            s = digit_sum % 10
            c = digit_sum // 10
            sum_arr.append(s)
        
        # if carry present for MSB, add it to the front
        if c != 0:
            sum_arr.append(c)
        
        # reveree the num, convert all digits to chars and join them before returning
        return ''.join(str(d) for d in reversed(sum_arr))
            