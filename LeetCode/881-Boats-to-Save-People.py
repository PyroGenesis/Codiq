from collections import deque
from typing import List

class Solution:
    '''
    The Greedy Concept:
        At every pairing, we try to match up the heaviest and lightest person that are unassigned
        If they are able to fit in a boat, we assign them one and take both out of the unassigned pool
        If they cannot fit in a boat, only the heavy is assigned a boat by themselves and removed the pool
        
        Intuition behind working:
        How about trying to pair the heavy with any other unassigned light?
            If lightest assigned cannot fit into a boat with the heavy, no other person can either
              because they will all be heavier than the lightest unassigned
        What if current heavy cannot form a pair with unassigned lightest but can form one with an assigned lightweight?
            Let's say a, z are an assigned pair
            For the new pair, y is not able to pair up with b but can pair up with a
            So what about pairing y with a?
            
            Some observations:
            a <= b and y <= z           ...(1) [because of the sort]
            a + z <= limit              ...(2) [scenario assumption]
            b + y > limit               ...(3) [scenario assumption]
            Therefore, b > a            ...(4) [because b is not < a (1) and if b == a then b+y == a+y <= limit (1)y<=z]
            Therefore, b + z > limit    ...(5) [because if (3) is true then it has to be because of (1)y<=z]
            
            So basically, if a pair cannot be formed with current lightest, no paired up heavy will work with current lightest
              therefore if you break up a previous pair, the previous heavy would have to sit alone in a boat
              
        Another proof:
        If hi and lo are not in same boat, say in boat-hi and boat-lo respectively.
        Let's say lo's boat mate is m, which will be <= hi [because hi is taken with greedy principles]
        Let's say hi's boat mate is n
        Now we can swap hi and m
            One boat will have (hi, lo) which we know is valid
            The other will have (m, n) which will also be valid because
                m + n <= hi + n [since m <= hi] <= limit [because (n, hi) were an original pair]
                Therefore m + n <= limit and (m, n) is a valid pair
        Since the swap results no extra boat(s), a new optimal solution T is obtained. 
        That indicates our first step (put hi and lo into same boat) is an optimal step and and greedy choice property also holds.
    '''
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        return self.numRescueBoatsTwoPointer(people, limit)
    
    '''
    Skipped:
        This problem can also be solved by Counting Sort (not too efficient though)
        https://leetcode.com/problems/boats-to-save-people/discuss/197063/easy-thought-process-to-improve-from-O(nlogn)-to-O(n)
        Time complexity: O(n + limit)
    '''
    
    '''
    Greedy - Two Pointers
        We follow the Greedy concept above, this time using two index pointers
        Inc i when a lightweight is paired with a heavyweight
        Inc j at every loop, putting heavyweight in a boat with/without lightweight
        
        We follow the rules putting 1 OR 2 people in a boat at a time, while bringing the pointers closer
        If one person is left in the pool (i==j), we give them their own boat
        
        Time:  O(nlogn) [because of sort]
        Space: O(sort)  [O(1) in case of in-place sort else O(n)]
    '''
    def numRescueBoatsTwoPointer(self, people: List[int], limit: int) -> int:
        # sort the people by weight
        people.sort()
        
        # i -> index of lightest person (not assigned a boat)
        # j -> index of heaviest person (not assigned a boat)
        i, j = 0, len(people)-1
        boats = 0
        
        # the loop will run while there are at least 2 people to assign a boat to
        while i < j:
            # try to pair up the heaviest and lightest unassigned people
            # if they cannot pair up, there can be no person to pair with the heavy
            #   so put them alone in a single boat
            if people[i] + people[j] <= limit:
                i += 1
            # regardless of whether lightweight can fit, heavyweight is always put in a boat on every loop
            j -= 1
            
            # In any case, there will be a boat used
            boats += 1
        
        # if any person is left alone after pairing loop, they get their own boat
        boats += 1 if i == j else 0        
        
        return boats
    
    '''
    Greedy - Deque
        We follow the Greedy concept above, obeying the rules with a sorted deque
        Pop from left to get the lightest
        Pop from right to get the heaviest
        
        We follow the rules putting 1 OR 2 people in a boat at a time, while emptying the deque pool
        If one person is left in the deque pool, we give them their own boat
        
        Time:  O(nlogn) [because of sort]
        Space: O(n)     [because of deque]
    '''
    def numRescueBoatsQueue(self, people: List[int], limit: int) -> int:
        # a deque of people sorted by weights
        weights = deque(sorted(people))        
        boats = 0
        
        # only loop while there are at least 2 people left (for assigning boats)
        while len(weights) > 1:
            # try to pair up the heaviest and lightest unassigned people
            # if they cannot pair up, there can be no person to pair with the heavy
            #   so put them alone in a single boat
            if weights[0] + weights[-1] <= limit:
                weights.popleft()
            # regardless of whether lightweight can fit, heavyweight is always put in a boat on every loop
            weights.pop()
            
            # In any case, there will be a boat used
            boats += 1
        
        # if any person is left alone after pairing loop, they get their own boat
        boats += len(weights)
        
        return boats
