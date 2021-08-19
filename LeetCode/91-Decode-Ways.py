class Solution:
    
    '''
        Skipped:
            Recursion with memoization: Guide
            Another resource: https://leetcode.com/problems/decode-ways/discuss/608268/Python-Thinking-process-diagram-(DP-%2B-DFS)
                memo[i] indicates combs for num[i:]
                O(n), O(n)
            
            Iterative: Guide
                using [i-1] and [i-2] in dp array
                O(n), O(n)
            
            Iterative with Constant Space: Guide
                using oneBeck and twoBack (very similar to curr soln, might be simpler)
                O(n), O(1)            
    '''
    
    
    '''
        Original and optimal
        We use 2 counters to count out all decodings possible upto a given num
            combined indicates that the num was combined with prev
                only possible if prev was 1 OR              (for 10-19)
                                 prev was 2 and num is <= 6 (for 20-26)
            separate indicates thet the num was kept on its own
                only possible if num is non-zero            (for 0-9)
                there cannot be a leading 0
        also make sure we don't come across a leading 0, because that makes the res 0
        
        Time:  O(n)
        Space: O(1)
    '''
    def numDecodings(self, s: str) -> int:
        n = len(s)
        
        # base cases, no leading 0 and single digit
        if s[0] == '0':
            return 0
        if n == 1:
            return 1
        
        combined = 0        # num combined with prev
        separate = 1        # num was kept on its own
        last = int(s[0])    # prev digit
        
        # starting with 2nd digit
        for i in range(1, n):
            # get the digit
            ci = int(s[i])
            
            # if we kept new digit as separate letter, it would basically be equal to all prior permutations found
            # except 0, we cannot keep it separate
            new_separate = 0
            if ci != 0:
                new_separate = combined + separate
            
            # if we attempt to combined it, prev and curr should satisfy all constraints
            # also combined will only work for permutations where the prev digit was left alone, so we only use the separate count
            new_combined = 0
            if last == 1 or (last == 2 and ci <= 6):
                new_combined = separate
            
            # update values
            combined, separate, last = new_combined, new_separate, ci
            # leading 0 found, quit early
            if (combined + separate) == 0:
                return 0
        
        # return all possible permutations
        return combined + separate
