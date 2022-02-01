# Leetcode imports
from typing import List


class Solution:
    
    def maxProfit(self, prices: List[int]) -> int:
        return self.maxProfitSimple(prices)
    
    '''
        One-pass simple algorithm
        There are 2 simple rules
        1. If we encounter a price < current buy price (i.e., profit < 0), we reset buy price to this new value
        2. Otherwise we calc profit bsaed on current price - buy price and save it to max profit if applicable
        
        Concerns
        1.  What if our ideal profit was ahead in the list but we switched out our buy price
        Ans Note that we only switch buy price when curr < og buy price (or profit < 0)
            This means that we will never lose out on a profit by switching because switching will always result in
                a greater profit considering the same sell price
        
        2.  What if our best buy-sell pair has already happened but we found another lower buy?
        Ans Since our buy-sell already happened, that profit must be recorded and stored in max_profit
            Now if we encounter a lower buy, we will switch our buy, however, our max_profit will remain the same
                unless we encounter a sell which would increase our overall profit
                
        Time:  O(n)
        Space: O(1)
    '''
    def maxProfitSimple(self, prices: List[int]) -> int:
        # If we can't buy and sell
        if len(prices) < 2:
            return 0
        
        min_price = float('inf')
        max_profit = 0
                
        for price in prices:            
            if price < min_price:
                # reset buy price
                min_price = price
            else:
                # sell and calculate profit
                profit = price - min_price
                max_profit = max(max_profit, profit)
                
        return max_profit
    
    '''
        Applying Kadane's algorithm for max subarray sum
            (Not more optimal, but interesting and useful for variations with change in profit)
        Look at the problem carefully. This problem can be converted to a max subarray problem.
        Buy on low and sell on high is the same as selling and buying on every price change
            and adding up all of the profits and losses in that range to get the overall profit
        Now the caveat is that if overall profit drops below 0, it means that the price went below current buy price
            so we reset the overall profit to 0, essentially buying at this new lowered price
        While all of this goes on, we keep track of the max value reached by overall profit and that's our answer
        
        So  current profit: curr price - prev price
            overall profit: max(0, overall profit + curr profit)
            ans:            max(ans, overall profit)
            
        Some examples will help:
        [7,1,5,3,6,4]
            We buy at 7 and sell at 1, curr profit = -6, overall = -6 as well so we reset
            We buy at 1 and sell at 5, curr profit = 4, overall = 4, ans = 4
            We buy at 5 and sell at 3, curr profit = -2, overall = 2, ans = 4
            We buy at 3 and sell at 6, curr profit = 3, overall = 5, ans = 5
            We buy at 6 and sell at 4, curr profit = -2, overall = 3, ans = 4
        
        [3,6,1,5,2]
            We buy at 3 and sell at 6, curr profit = 3, overall = 3, ans = 3
            We buy at 6 and sell at 1, curr profit = -5, overall = -2 (reset to 0), ans = 3
            We buy at 1 and sell at 5, curr profit = 4, overall = 4, ans = 4
            We buy at 5 and sell at 2, curr profit = -3, overall = 1, ans = 5
            
        [7,6,4,3,1]
            At every step, curr = -ve, so overall = -ve so keep resetting
            ans = 0
        
        As you can see, not only are the answers correct, but overall also represents buying on lowest prev value and
            selling on curr value
                
        Time:  O(n)
        Space: O(1)
    '''
    def maxProfitKadane(self, prices: List[int]) -> int:
        # If we can't buy and sell
        if len(prices) < 2:
            return 0
        
        max_profit = 0      # ans
        overall_profit = 0
        
        for i in range(1, len(prices)):
            # profit if bought at price before and sold now
            curr_profit = prices[i] - prices[i-1]
            # profit if bought at least price before and sold now
            overall_profit = max(0, overall_profit + curr_profit)
            # record max sell profit
            max_profit = max(max_profit, overall_profit)
        
        return max_profit
            