import math
from typing import List

# Read the solutions from the bottom to the top
class Solution:
    def minCostII(self, costs: List[List[int]]) -> int:
        return self.minCostIIOptimized(costs)
    
    '''
    Optimized
        And this is to go, even further beyond!
        In the previous solution, for every new house-color calc,
          we iterated over all previous house colors to find the minimum.
        But do we need to iterate every time? As it turns out, no!

        For most new house-color costs, we will use the minimum of all previous house-color costs
        The only exception to this is if the new house color considered is the same as the previous minimum cost house-color
            In that case, we can simply just use the second-lowest house-color cost for the calc of that new house-color cost
        
        Therefore, we can simply keep track of the lowest and second-lowest aggregated coloring costs for the previous house colors
          as well as the colors (index) for the mentioned costs
        Then we can use that to find the min and second-min aggregated costs (and indices respectively) after including the next house
        Finally the last min-cost we end up with is the answer

        Time:  O(n*k)
            The nested loop goes through every house-color combo once
        Space: O(1)
            We only use a fixed number of variables
    '''
    def minCostIIOptimized(self, costs: List[List[int]]) -> int:
        n = len(costs)      # number of houses
        k = len(costs[0])   # number of colors

        # sanity check
        # needed for if the input doesn't have 2+ colors or houses
        if n == 1:
            return min(costs[0])

        # utility function to take in an input and update the min and second-min values (if necessary)
        # the color vars are additional info that needs to follow the cost assignment operations
        def updateMinAndSecondMin(color: int, cost: int, best_cost, second_best_cost, best_color: int, second_best_color: int):
            if cost <= best_cost:
                # if the cost is equal to or better than the best cost, 
                #   assign it to the best cost and the old best cost to the second best cost
                second_best_cost, best_cost = best_cost, cost
                second_best_color, best_color = best_color, color
            elif cost < second_best_cost:
                # Otherwise, if it is only strictly better than the second best cost, 
                #   replace it with the incoming one
                second_best_cost = cost
                second_best_color = color
            
            # return all possibly changed arguments
            return best_cost, second_best_cost, best_color, second_best_color

        # the min and second-min aggregated cost of painting the previous house,
        #   and all the houses before it. 
        # We also keep track of the actual colors these two min costs refer to
        best_prev_color_cost, second_best_prev_color_cost = math.inf, math.inf
        best_prev_color, second_best_prev_color = -1, -1

        # process the first house, going through every color
        #   to fill out the above 4 variables
        for color, cost in enumerate(costs[0]):
            (best_prev_color_cost,
             second_best_prev_color_cost,
             best_prev_color,
             second_best_prev_color) = updateMinAndSecondMin(color, cost,
                                                             best_prev_color_cost,
                                                             second_best_prev_color_cost,
                                                             best_prev_color,
                                                             second_best_prev_color)

        # go through every house (starting from idx 1 as idx 0 is already processed)
        for house in range(1, n):
            # the min and second-min aggregated cost of painting the current house,
            #   and all the houses before it. 
            # We also keep track of the actual colors these two min costs refer to
            best_curr_color_cost, second_best_curr_color_cost = math.inf, math.inf
            best_curr_color, second_best_curr_color = -1, -1

            # try to paint the house every color
            for color in range(k):
                # the aggregated cost will include painting current house this color
                cost = costs[house][color]

                # pick the best possible aggregate cost of painting all houses before 
                #   this one and add it to the cost
                if color == best_prev_color:
                    cost += second_best_prev_color_cost
                else:
                    cost += best_prev_color_cost
                
                # update the min, second-min costs (and color idxs) based on the cost just computed
                (best_curr_color_cost, 
                 second_best_curr_color_cost, 
                 best_curr_color, 
                 second_best_curr_color) = updateMinAndSecondMin(color, cost,
                                                                 best_curr_color_cost,
                                                                 second_best_curr_color_cost,
                                                                 best_curr_color,
                                                                 second_best_curr_color)
            
            # copy all current costs and colors to the prev variables to get ready to process the next house
            best_prev_color_cost = best_curr_color_cost
            second_best_prev_color_cost = second_best_curr_color_cost
            best_prev_color = best_curr_color
            second_best_prev_color = second_best_curr_color
        
        # the ans is the best aggregated cost found for the last house
        return best_prev_color_cost


    '''
    Dynamic Programming
        Now, we need to reverse the recursive logic to come up with an iterative solution
        To do so, consider the final recursive calls near the end of the stack in the recursive solution
            For house n-1, we simply return the cost of the picked color
            For house n-2,  for color A, we pick every color != A for house n-1 and consider the min as best solution
                            for color B, we pick every color != B for house n-1 and consider the min as best solution
                            ...
        So every color of a house, the best it can do is the min cost of coloring its neighbor some other color
        This logic can be realized and implemented iteratively. A visual aid is drawn below.

        costs               colors
                    0   1   2   3   4   5
                0   10  6   16  25  7   28
                   /```````````````````````
        houses    / + min()
                 /
                1   7   16  18  30  16  28
        
        We can optimize on space by only keeping the costs of coloring the prev house (aggregated) 
          only instead of the entire house-color grid because that is all that is required for
          figuring out all color costs of the next house
                
        Time:  O(n*(k^2))
            The for-loop runs for
                every house:        O(n)
                every new color:    O(k)
                every prev color:   O(k)
        
        Space: O(k)
            We only keep the costs of the coloring of the prev house (aggregated)
    '''
    def minCostIIIterativeDp(self, costs: List[List[int]]) -> int:
        n = len(costs)      # number of houses
        k = len(costs[0])   # number of colors

        # the minimized aggregated cost of picking a color for the house,
        #   taking into account the all possible coloring combinations
        #   of the houses before it. 
        # It's a 1D array and only needs to keep track of the costs for 
        #   the house we are processing
        dp = [costs[0][color] for color in range(k)]
        
        # go through every house (starting from idx 1 as idx 0 is already in dp)
        for house in range(1, n):
            # the aggregated costs for picking each color for this house
            curr = []
            # go through every color
            for color in range(k):
                # get the min aggregated cost out of all the colors chosen for 
                #   the previous house except the one chosen for the current house
                best_prev_color_cost = math.inf
                for prev_color in range(k):
                    if prev_color == color: continue
                    best_prev_color_cost = min(best_prev_color_cost, dp[prev_color])
                # add the result (min aggregated cost) of choosing this color for the current house
                curr.append(best_prev_color_cost + costs[house][color])
            # set the current house aggregated costs as dp
            dp = curr
        
        # the ans is the minimum out of all the aggregated costs of each color for the last house
        return min(dp)

        
    
    '''
    Recursion + Memoization
        Since this is a dp problem, start by thinking recursively
        Think about the choices you have at any single point of time
        
        Recursion
        Let's say you go through the houses one by one, starting from the 0th.
        You can start by choosing a color for the current house and calling the recursive function
            The function will then try every possible color (!= current color) for the next house 
              and call the recursive function again
        At the end, the last house will return the cost of coloring itself the chosen color
        As the function backtracks, the costs of coloring the houses gets added up.
        The min() in the loop ensures that only the best future coloring is returned 
          for the color picked for the current house
        
        Memoization
        The pure recursive solution would have a lot of redundant work done.
        For example, say the colors are [red, green, blue] and there are 10 houses.
            For house 1, let's say we picked red
                Then for house 2, we pick green
                    and so on ...
                Then for house 2, we pick blue      -> {1}
                    and so on ...
            For house 1, now we pick green
                Then for house 2, we pick red
                    and so on ...
                Then for house 2, we pick blue      -> (2)
                    and so on ...
            and so on ...
        Here, you can see that the entire recursive tree starting at (1) and (2) are identical
          and therefore will cause a lot of repeated work
        We can improve this by the storing the ideal cost for every house, color combo when it is computed

        Time:  O(n*(k^2))
            The recurse fn runs for every house, color combo once
                (repeated combos are memoized)
            Total combos = n*k
            For every combo, we have a loop of O(k) for the next color
            Total = O(n*k * k) = O(n*(k^2))
        
        Space: O(n*k)
            The memoization grid takes the most space at n*k cells
    '''
    def minCostIIRecursiveMemo(self, costs: List[List[int]]) -> int:
        n = len(costs)      # number of houses
        k = len(costs[0])   # number of colors

        # the minimized aggregated cost of picking a color for a house,
        #   taking into account the all possible coloring combinations
        #   of the houses after it
        memo = [[0 for _ in range(k)] for _ in range(n)]

        # the recursive function takes in a house index and a color index
        #   and returns the minimum aggregated cost of picking that color
        #   for that house and all possible coloring combinations
        #   of the houses after it
        def recurse(house: int, chosen_color: int) -> float:
            nonlocal costs, n, k, memo

            if house == n-1:
                # base case
                #   if this is the final house, the aggregated value is 
                #     simply the cost of painting the house the chosen color
                return costs[house][chosen_color]
            if memo[house][chosen_color] > 0:
                # if the ans is memoized, return it
                return memo[house][chosen_color]
            
            min_cost = math.inf
            # iterate through every color for the next house
            for color in range(k):
                if color == chosen_color:
                    # cannot pick the same color as current house
                    continue
                
                # calc the aggregated cost for each neighbor color
                cost = costs[house][chosen_color] + recurse(house+1, color)
                min_cost = min(min_cost, cost)
            
            # save the min aggregated coloring cost for this house and chosen color
            memo[house][chosen_color] = min_cost
            return min_cost
        
        # start recursion for every color for the first house 
        #   and pick the least aggregared cost returned
        return min(recurse(0, color) for color in range(k))

