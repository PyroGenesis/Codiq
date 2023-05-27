from collections import defaultdict
from typing import List

class Solution:
    '''
    Sliding window:
        First thought was to split logic into 3 distinct parts
        while j < n
            if fruit type already in basket, 
                add to basket and simply check for best max and inc j
            Else if basket doesn't have two types already,
                add to basket and simply check for best max and inc j
            Else basket already has 2 types,
                empty basket until 1 type remains then
                add to basket and simply check for best max and inc j
        You can see here that the logic is quite duplicated

        We can simplify if we realize that we can add the jth fruit first and
          then worry about the constraints
        while j < n
            add jth fruit to basket
            if basket has more than 2 types, 
                remove until we have only 2 or less types
            simply check for best max and inc j
        
        An additional simplification can be done when we realize that j is 
          always incremented, so while loop -> for loop

        Time:  O(n) [we go through every tree at most twice (i & j)]
        Space: O(1) [the basket can only have 3 entries at max]
    '''
    def totalFruit(self, fruits: List[int]) -> int:
        n = len(fruits)             # number of trees
        max_fruits = 0              # max fruits we could pick
        basket = defaultdict(int)   # currently picked fruits in basket (type -> count)
        
        i = 0                       # start idx of collection of fruits (inclusive)
        for j in range(n):          # end idx of collection of fruits (exclusive)
            # Add jth fruit to basket
            basket[fruits[j]] += 1

            # remove fruits from basket until we only have 2 types
            while len(basket) > 2:
                ti = fruits[i]
                if basket[ti] == 1:
                    del basket[ti]
                else:
                    basket[ti] -= 1
                i += 1
            
            # update the max picked fruit count
            max_fruits = max(max_fruits, j - i + 1)     
        # ans   
        return max_fruits
