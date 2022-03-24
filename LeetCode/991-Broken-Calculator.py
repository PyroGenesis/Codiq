class Solution:
    '''
    Greedy Division (Backwards) - Optimal
        The base idea is such, multiplication by 2 will quickly get us very close to a high number, but it can also 
            overshoot by a lot which will have to be made up by lots of subtractions
        Therefore doing subtractions first to get to an ideal number and then using multiplication to boost up close to target
            will give us a minimum number of operations.
            Why? Because subtractions carry forward much more value, earlier than later
                Proof: (start - subs) * muls = start*muls - subs*muls
                Here you can see, both LHS and RHS will equal the same number, but 
                    LHS is (subs + muls) operaions
                    RHS is (subs*muls + muls) operations
            
        Now we need to turn this concept over backwards since we know where we want to be after multiplications,
        (right on target if odd and target+1 if even), but we don't yet know the ideal number to reach via subtractions first.
            Therefore, we change the problem from start -> target (via mul, sub) to target -> start (via div, add)
        
        So now that we've changed the problem, it becomes much easier to map out an optimal path:
            If y (originally equal to target) is odd, it is not possible to divide so our only option is to add
                (in original problem terms, y cannot be reached by mul so there has to be 
                 at least 1 sub to get here from an odd number)
            If y is even (lets say x == y // 2), we can either
                divide and reach x, then 1 more operation makes us reach x+1
                add, but then we are forced to add again. Dividing after that, we reach x+1 in 3 steps (optimal: 2)
                    (in original problem terms, sub first then mul will take us 2 operations for x+1 -> y, 
                     but mul first then sub will take us 3 operations [mul, sub, sub])
                     
        So why can't we go forwards with X instead of backwards with Y? 
            As mentioned before, the multiplication operation is, quite obviously, multiplicative, 
                and will have an enhancing effect on any subtraction operations performed before it. 
            Therefore, we cannot possibly know how much impact any given subtraction operation will have 
                on the difference between X and Y until we find out how many multiplication operations we will need after it.
        
        Therefore, we get these set of greedy rules:
        To reach from y -> x,
            if y == x, 0 operations remain                                              (1)
            if y < x, next (x - y) operations are add because we are forced to do so    (2)
            if y is odd, next operation is add, then repeat check for next rule         (3)
            if y is even, next operation is div, then repeat check for next rule        (4)
        
        Time:  O(log target)
        Space: O(1)
    '''
    def brokenCalc(self, startValue: int, target: int) -> int:
        operations = 0
        
        # doing the looped rules
        while target > startValue:
            if target % 2 == 1:
                # rule (3)
                target += 1
            else:
                # rule (4)
                target //= 2
            
            # both (3) and (4) are single operations
            operations += 1
        
        # combining rule (1) and (2), because (1) is just a special case of (2) [y-x = 0]
        operations += startValue - target
        
        # returning the optimal num of operations calculated
        return operations
