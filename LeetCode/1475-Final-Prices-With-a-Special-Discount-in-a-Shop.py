from typing import List


class Solution:
    def finalPrices(self, prices: List[int]) -> List[int]:
        return self.finalPricesStack(prices)

    def finalPricesStack(self, prices: List[int]) -> List[int]:
        """
        Monotonic Stack
            We can start by storing a price in a stack
            When we get a new price, we can check top of stack repeatedly
                and remove the prices which can now be discounted

            But why does this work? What if a price cannot discount top of stack
                but can discount a price further in stack?
            Let's say our stack is [x, y] with new price z
            If z cannot discount y, z > y
            If z can discount x,    z <= x
            So, x >= z > y, therefore x > y
            But if x > y then y would have already discounted x
            Therefore our stack is always in increasing order,
                and a new price that cannot discount the top of stack
                cannot discount the rest of the stack either

        Time:  O(n)
            We loop through every price once
            Also, even though we have a nested while loop,
                each price only gets added and removed from stack once at maximum
        Space: O(n) OR O(1)
            Result space
        """
        n = len(prices)

        # stack which stores indices of prices not discounted
        stack = []
        for i in range(n):
            # if there are prices left that current price can discount, do it
            while stack and prices[stack[-1]] >= prices[i]:
                prev_i = stack.pop()
                prices[prev_i] -= prices[i]
            # add this price as new discounted price
            stack.append(i)
        return prices

    def finalPricesSimpleBruteForce(self, prices: List[int]) -> List[int]:
        """
        Simple brute-force
            The constraints are so low that simple brute-force solution is feasible and quick.
            Simply try to find a valid price reduction for every item

        Time:  O(n^2)
            Because we may need to iterate to the end for every price (except last)
        Space: O(n) OR O(1)
            Result space
        """
        n = len(prices)

        # try to reduce price for each item
        # no need to check discount for last item
        for i in range(n - 1):
            # check every price after current one until we find a valid one
            for j in range(i + 1, n):
                if prices[j] <= prices[i]:
                    # reduce the price when we find a valid later item
                    # no need to check any further
                    prices[i] -= prices[j]
                    break
        return prices
