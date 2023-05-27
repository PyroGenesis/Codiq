'''
Brainteaser
    There is only one answer to this problem, and unfortunately it relies on realizing a trick
    The trick is to realize there are only two possible answers, 1 and 2
    
    How?
    The main reason this is the case, is because we have only 2 letters and subsequences are allowed
    Consider the two cases
    1. The input is a palindrome
        If the input is a palindrome, it can be completely eliminated in a single step
        This gives us an answer of 1
    2. The input is NOT a palindrome
        If the input is not a palindrome, the ans will be > 1
        So the min ans = 2, but how is that the actual answer?
            In the first operation, remove all letters 'a'. This is guaranteed to be palindromic since there are no other letters
            In the second operation, you can remove the rest of string which will all be 'bbb...' and also guaranteed to be
                palindromic
        This proves that if ans is not 1, it is always 2
    
    Time:  O(n) - for checking palindrome
    Space: O(1) - we used 2 pointers and no storage
'''
class Solution:
    # checks whether a string is a palindrome
    def isPalindrome(self, s):
        # the two pointers
        i, j = 0, len(s)-1
                
        while i < j:
            # if the letters at the two ends are not the same, the string is not a palindrome
            if s[i] != s[j]:
                return False
            # move both pointers towards each other
            i += 1
            j -= 1
        # all checks passed, the string is a palindrome
        return True
    
    def removePalindromeSub(self, s: str) -> int:
        # operations = 1 if palindrome, = 2 if not
        return 1 if self.isPalindrome(s) else 2
