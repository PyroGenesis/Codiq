# Leetcode imports
from typing import List

class Solution:
    def maximumWealth(self, accounts: List[List[int]]) -> int:
        return self.maximumWealthOneLiner(accounts)
        
    '''
        Simple one-liner
        Time:  O(M*N)
        Space: O(1)   if both comprehensions use O(1) space [unlikely]
               O(M+N) if both comprehensions take some amount of space
    '''
    def maximumWealthOneLiner(self, accounts: List[List[int]]) -> int:
        return max(sum(row) for row in accounts)
    
    '''
        Using loop
        A bit overkill but useful for interview and guaranteed best space complexity
        Time:  O(M*N)
        Space: O(1)     we use a single variable
    '''
    def maximumWealthExpanded(self, accounts: List[List[int]]) -> int:
        maxWealth = 0
        for i in range(len(accounts)):
            wealth = sum(accounts[i])
            maxWealth = max(maxWealth, wealth)
        return maxWealth
    
