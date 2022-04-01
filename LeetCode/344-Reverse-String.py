from typing import List

class Solution:
    '''
    Pointer solution
        There is only one real solution to this problem
            No, its not s.reverse()
        It's to swap the characters: (0,n-1), (1,n-2) ...
            until we cross the pointers
    
        Time:  O(n)
        Space: O(1)
    '''
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        # the two pointers
        i, j = 0, len(s)-1
        
        # swap the characters
        while i < j:
            s[i], s[j] = s[j], s[i]
            i += 1
            j -= 1
            
        '''
        Other ways of looping:
        
        for i in range(size//2):
            s[i], s[-i-1] = s[-i-1], s[i]
        
        for i in range(size//2):
            s[i], s[~i] = s[~i], s[i]
        '''
        
        return s
