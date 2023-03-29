from typing import List


class Solution:
    def mincostTickets(self, days: List[int], costs: List[int]) -> int:
        return self.mincostTicketsBottomUpDp(days, costs)
    
    
    def mincostTicketsBottomUpDp(self, days: List[int], costs: List[int]) -> int:
        last_day = days[-1]
        dayset = set(days)
        dp = [0] * (last_day + 1)

        for day in range(1, last_day+1):
            if day not in dayset:
                dp[day] = dp[day - 1]
            else:
                prev_day = max(day - 1, 0)
                prev_week = max(day - 7, 0)
                prev_month = max(day - 30, 0)

                dp[day] =  min(costs[0] + dp[prev_day],
                                costs[1] + dp[prev_week],
                                costs[2] + dp[prev_month])
        
        return dp[last_day]
    

    def mincostTicketsTopDownDp(self, days: List[int], costs: List[int]) -> int:
        last_day = days[-1]
        dayset = set(days)
        memo = [0] * (last_day + 1)

        def recurse(day):
            nonlocal costs, memo, last_day, dayset
            if day > last_day:
                return 0
            elif day not in dayset:
                return recurse(day + 1)
            elif memo[day] > 0:
                return memo[day]
                        
            min_cost =  min(costs[0] + recurse(day + 1),
                            costs[1] + recurse(day + 7),
                            costs[2] + recurse(day + 30))
            memo[day] = min_cost
            return min_cost
        
        return recurse(1)

