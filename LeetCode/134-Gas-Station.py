# LeetCode imports
from typing import List

class Solution:
    '''
        Firstly, we verify that soln is possible by comparing sum(gas) and sum(cost)
        Next we pick a start and iterate until it becomes apparant our start is incorrect
        As soon as that happens, we pick the next stop as our new start location
        Why pick the next stop as new start rather than any stop between current start and current stop? See below:
            If proceed from A, and found A cannot reach B, then for any points C between A and B; C cannot reach B too. (because if A reached C, then the fuel left when reached C will always >= 0, which is always equal or better than start from C)
        Therefore, it becomes apparent that the only start that will work here will have a >= 0 surplus at the end of loop
        
        Now its clear why any points from A to just before B won't work, but whats the proof that a start with a >=0 surplus will work?
        Proof is by contradiction: Assume point k cannot be reached from start
        Firstly,                 sum(0 to N) >= 0                                        (1)
        Splitting it up:         sum(0 to k) + sum(k+1 to start-1) + sum(start to N) >=0 (2)
                                 sum(start to N) >= 0 as our soln proves                 (3)
                                 sum(k+1 to start-1) < 0 otherwise start would be = k+1  (4)
        using (2) and (4):       sum(0 to k) + sum(start to N) >=0                       (5)
        but if k cant be reached sum(start to k) < 0
        OR                       sum(start to N) + sum(0 to k) < 0                       (6)
        (5) and (6) contradict each other, hence proved
        
        Note: This can be done in 1-pass as well by doing the sum inside the for-loop and checking in the end
        
        Time: O(n)
        Space: O(1)
    '''
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        # check if soln exists
        if sum(gas) < sum(cost):
            return -1
        # Also valid is: if sum(gas[i]-cost[i] for i in range(len(gas))) < 0
        # The above translates to if gas is in a deficit passing through all stations in a line
        # Basically, if we cannot pay off any gas debt we accrued while passing through all stations from start to finish
        
        # initially our fuel is 0
        surplus = 0
        # initially our first station is index 0
        start = 0
        
        for i in range(len(gas)):
            # add the gas at the station to our surplus
            surplus += gas[i]
            
            # if we cannot move ahead, we reassign our start to the next station
            if surplus - cost[i] < 0:
                surplus = 0
                start = i+1
            else:
                surplus -= cost[i]
                
        return start