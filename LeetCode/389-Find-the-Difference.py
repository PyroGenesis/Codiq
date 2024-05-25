from collections import Counter

class Solution:
    def findTheDifference(self, s: str, t: str) -> str:
        return self.findTheDifferenceBitManip(s, t)
    
    '''
    Bit Manipulation
        Idea is simple, XORing the same thing twice zeroes it out. So we just XOR all the letters
        Only 1 letter will be XORed an odd number of times and that will be the extra letter in t
        
    Time:  O(n)
    Space: O(1)
    '''
    def findTheDifferenceBitManip(self, s: str, t: str) -> str:
        XOR_res = 0
        
        for char in s:
            XOR_res ^= ord(char)
        
        for char in t:
            XOR_res ^= ord(char)
        
        return chr(XOR_res)
    
    '''
    Hashmap
        Match every character in t to a character in s, until we find a char that does not match
        We do this by keeping a count of every char in s, then decrementing when we encounter that char in t
            If a letter in t is not present in the Counter, or the count is already 0, that is the extra letter
    
    Time:  O(n)
    Space: O(n)
    '''
    def findTheDifferenceHashmap(self, s: str, t: str) -> str:
        s_char_count = Counter(s)
        for c in t:
            if c not in s_char_count or s_char_count[c] == 0:
                return c
            s_char_count[c] -= 1
        
        # will never reach here
        return None
