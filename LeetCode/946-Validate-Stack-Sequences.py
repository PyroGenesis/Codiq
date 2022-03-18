# Leetcode imports
from typing import List

class Solution:
    '''
    Skipped:
        You can technically do the below greedy soln in O(1) space by using the input space of pushed instad of making your own stack
        However, you will be destroying the input, and the O(1) nature is debatable
        
        def validateStackSequences(self, pushed, popped):
            i = j = 0
            for x in pushed:
                pushed[i] = x
                while i >= 0 and pushed[i] == popped[j]:
                    i, j = i - 1, j + 1
                i += 1
            return i == 0
    '''
    
    '''
    Greedy solution
        The way to solve this problem is to simulate the stack
            and so simulate all the pushes and pops
        But how do we know whether to push or pop at any given stage?
        Since the values in the list are distinct, we can make use of a Greedy strategy
            1. Pop every chance you get
            2. If cannot pop, push once and goto step 1
            3. If cannot push or pop, we are done with the simulation
            
        Proof that Greedy is correct:
        Assume that we are in a simulation where you can both push and pop
        Since the elements are distinct, if you don't pop now (and push), you will never be able to pop again
            (becuase that num will get stuck in the pop queue)
        This will lead to incomplete simulation and be suboptimal
    
    Algorithm:
        Iterate infinitely while keeping a stack
            Pop out element if possible (Greedy)
            Push in element if pop not possible
            Quit loop if neither are possible
        Since len(pushed) == len(popped), we can simply check if the simulated stack is empty at the end
            to verify the completion of the simulation
    
        Time:  O(n)
        Space: O(n)
    '''
    def validateStackSequences(self, pushed: List[int], popped: List[int]) -> bool:
        stack = []          # the stack for simulation
        n = len(pushed)     # n == len(pushed) == len(popped)
        i, j = 0, 0         # i -> index to next pushed value, j -> index to next popped value
        
        # started infinite loop, but at max this can only loop 2n times
        while True:
            
            if stack and j < n and stack[-1] == popped[j]:
                # take every valid chance of popping an element. Greedily.
                stack.pop()
                j += 1
            elif i < n:
                # if we can't pop, push instead
                stack.append(pushed[i])
                i += 1
            else:
                # we cannot pop and push, so we are stuck here and therefore, quit the loop
                break
        
        # the stack should be empty in the end
        # this is making use of the assumption that len(pushed) == len(popped)
        return not stack
