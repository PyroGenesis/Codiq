from typing import List

class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        return self.RecursiveBacktracking(k, n)
    
    '''
    Recursive Backtracking Solution: Optimal
    This is a prime example of an recursive algorithm performing better (and cleaner) than its iterative counterpart
        
        At the beginning, we perform some clever checks to see if a sequence is even possible
        We start with an empty sequence, and the first digit to consider as 9
        
        At any step, if we have the sum of sequence == n and the sequence length == k
            We have succeeded, add a copy of the sequence into the result
        At any step, if we have run out of positions for numbers or already reached target sum without using all positions,
            this sequence has failed, and so return immediately
        At any particular step, we pick a number in the range (digit to consider to 1) 
          [provided the digit does not exceed remaining sum]
          (for the first iteration, this is 9 -> 1)
            We add the digit to our sequence and restart the next step with initial digit to consider = current digit picked + 1
              (this is because we do not wish to pick any duplicate digits)
            After we return back from future steps, we take the digit out of current sequence
              [all sequences with current digit have been considered]
            Pick the next digit and repeat this loop
        
        Time complexity:
        Since we are actually going through valid combinations only, our upper bound should be equal to
            the combination length * number of valid combinations which will be
            O(k * C(9,k)) OR O(K * 9!/[(9-K)!*K!])
        Infact, since our k is fixed between 0 to 9, we can actually compute the max value for this time complexity, 
            which is possible when k = (n+1)/2 OR (n-1)/2 which comes out to k = 4 OR 5 and k * C(9,k) = 630, 
            which should technically reduce our time complexity to O(1)
        But it might be better to only simplify until O(k * C(9,k)) OR O(K * 9!/[(9-K)!*K!])
        
        Space complexity:
        If we don't take the result complexity into account, space used is
        O(
            k   [for maintaing current sequence]
            +
            k   [function call stack]
        )
        => O(k)
    '''
    def RecursiveBacktracking(self, k: int, n: int) -> List[List[int]]:
        # sanity checks
        # if any of these are true, there are no combinations possible
        if k==0 or n==0 or k>9:
            return []
        
        # low and high checks
        # low check:  1 + 2 + ... + k
        #   This is the smallest sum, so if this is > n, there is no combination possible
        #   Calculated using formula: [n*(n+1)] // 2
        # high check: 9 + 8 + ... + 9-k
        #   This is the largest sum, so if this is < n, there is no combination possible
        #   Calculated using the AP sum formula: [n/2] * [2a + (n-1)d]
        if (k*(k+1))//2 > n or (k/2)*(2*9 + (k-1)*-1) < n:
            return []
        
        res = []    # all combinations, result
        curr = []   # current combinations, copied to result if successful
        
        def backtrack(sum_remain, last_digit):
            nonlocal k, curr
            
            if len(curr) == k and sum_remain == 0:
                # We've used exactly k elements, whose resultant sum is n
                # This is a successful combination, so copy it to the result
                # The reason we copy and don't add directly is because curr is dynamic and will change for next combination
                res.append(curr.copy())
                return
            elif len(curr) == k or sum_remain == 0:
                # If only one of condition is satisfied, current combination is doomed to failure, so return early
                # len(curr) == k,  curr cannot take more elements so current comb not possible
                # sum_remain == 0, more elements will make sum go above n, so current comb not possible
                return
            
            # since digits cannot repeat, start the digit from the last digit-1 to 1
            # (We are going in reverse order just because it feels faster)
            for d in range(last_digit-1, 0, -1):
                # digit is too large and exceeds sum, move on to next digit
                if d > sum_remain:
                    continue
                
                # add digit to current sequence
                curr.append(d)
                # backtrack on current sequence, considering the rest of digits for rest of positions
                backtrack(sum_remain - d, d)
                # all sequences with this digit has been considered, remove it from current sequence
                curr.pop()
        
        # start the backtracking with sum required = n and first digit to consider = 10-1 = 9
        backtrack(n, 10)
        # after backtracking, res should've been filled correctly. return it.
        return res
    
    
    '''
        Iterative Backtracking soln - Suboptimal space and algorithm complexity
        We pick a value between start=1 and end=9
            If value > remaining, we failed
            If value == remaining, we passed if this is the last number else we failed
            If value < remaining, we subtract value from remaining, reduce count and pick another number with start = last_pick+1 
                (so as to avoid duplicates)
        
        Time: 
        Since we are actually going through valid combinations only, our upper bound should be equal to
            the combination length * number of valid combinations which will be
            O(k * C(9,k)) OR O(K * 9!/[(9-K)!*K!])
        Infact, since our k is fixed between 0 to 9, we can actually compute the max value for this time complexity, 
            which is possible when k = (n+1)/2 OR (n-1)/2 which comes out to k = 4 OR 5 and k * C(9,k) = 630, 
            which should technically reduce our time complexity to O(1)
        But it might be better to only simplify until O(k * C(9,k)) OR O(K * 9!/[(9-K)!*K!])
              
        Space: 
        IDK man, the write-up says O(k) for a recursive backtrack but the stack version seems a little worse
        Lets say n is large, so we'll go through all combinations as well as k == 9, the largest combination possible
        The first candidate check, our stack will inc by 9
        The second candidate check, our stack will inc by 8
        The third candidate check, our stack will inc by 7
        So our max size could be (9 + 8 + 7 + ... + (9-k)) which would be at max sum(1 to 9) = 45
        This is kinda the same as our AP sum: (k/2)*(2*9 + (k-1)*-1) so O(k^2)?
    '''
    def IterativeBacktracking(self, k: int, n: int) -> List[List[int]]:
        # sanity checks
        # if any of these are true, there are no combinations possible
        if k==0 or n==0 or k>9:
            return []
        
        # low and high checks
        # low check:  1 + 2 + ... + k
        #   This is the smallest sum, so if this is > n, there is no combination possible
        #   Calculated using formula: [n*(n+1)] // 2
        # high check: 9 + 8 + ... + 9-k
        #   This is the largest sum, so if this is < n, there is no combination possible
        #   Calculated using the AP sum formula: [n/2] * [2a + (n-1)d]
        if (k*(k+1))//2 > n or (k/2)*(2*9 + (k-1)*-1) < n:
            return []
        
        # stack = [seq, start, k, target]
        stack = [[[], 1, k, n]]
        ans = []
        
        while stack:
            seq, start, count_remaining, value_remaining = stack.pop()
            
            # if only 1 digit is remaining to be added, we dont actually have a choice
            # Just check whether that remaining digit would be in a valid range
            # If so, add it to our soln
            # If not, discard it
            # Whatever we do, we just continue on without checking any other candidates
            if count_remaining == 1:
                if start <= value_remaining <= 9:
                    ans.append(seq+[value_remaining])
                continue
            
            # Our candidate will obv not be valid if > remaining
            # But if candidate is == remaining, its still not valid because count > 1 (we completed before our time)
            # If less, than welcome aboard!
            for candidate in range(start, 9):
                if candidate >= value_remaining:
                    break
                else:
                    stack.append([seq+[candidate], candidate+1, count_remaining-1, value_remaining-candidate])
        
        return ans
