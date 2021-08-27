class Solution:
    def findLUSlength(self, a: str, b: str) -> int:
        '''
        God, this solution was so simple but I over-thought it.
        Consider the following:
        1. The strings are the same
            There can be no uncommon subsequence, return -1
        2. The strings are the same
            a. The strings have the same length
                Both strings are the 'longest' uncommon subseq
            b. The strings have unequal length
                The longer string cannot be a subseq of shorter string and so it is the longest unequal subseq
            In both cases, longest subseq len == longest string len
        
        Time:  O(min(a, b))     == takes min(a, b) time
        Space: O(1)             No extra space used
        '''
        
        if a == b:
            return -1        
        return max(len(a), len(b))
    
        # one-liner: return -1 if a==b else max(len(a), len(b))
