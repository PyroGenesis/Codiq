# Leetcode imports
from typing import List

class Solution:
    '''
    Observations:
        single digit
            at start of num:    1, 8
            in middle of num:   1, 8, 0
            if n==1:            1, 8, 0
        two digits
            at start of mum:    11, 88, 69, 96
            in middle of num:   11, 88, 69, 96, 00    
    '''
    
    '''
    Backtracking (Optimal)
        Consider the following approach:
        Let's say we start from the start of the num, and pick a digit at the start
        Since this is a strobogrammatic num, the end digit will also be chosen automatically
        Now we can move ahead and pick the next digit and so on...
        After we have picked the possibilities for the middle digit(s) and added them all to our ans list,
            we can go back to the prev choice and pick another pair
        This way we can get all combinations by backtracking when have finished all the future ones
        We just have to make sure to go through all the valid choices for a position in the num based on the observations above
        
        Implemenation Note:
            Its better to pick a arr to represent the num here since it will be mutable
            Otherwise we will end up storing all partial immutable strings in memory
        
        Time complexity:
            Consider the problem as a tree where at every step we pick an appropriate pair
            So the branching factor of tree = max(choices)      = 5
                   depth of tree            = floor(n/2) + 1    = (n//2) + 1
            At each leaf of this tree, we will also take O(n) time to make our arr into a string
            Therefore, Time complexity = O(n * 5^[(n//2) + 1]))
        
        Space complexity:
            Since we store all strings of size n for all leaves of the tree described above
            Space complexity = O(n * 5^[(n//2) + 1]))
    '''
    def findStrobogrammatic(self, n: int) -> List[str]:
        # handle special case for n==1 separately (to reduce complexity further on)
        if n == 1:
            return ["0","1","8"]
        
        strobos = []    # all strobogrammatic nums of size n
        
        candidates_start  = [('1','1'), ('8','8'), ('6','9'), ('9','6')]            # pairs if the digit will be at the start of num
        candidates_middle = [('1','1'), ('8','8'), ('0','0'), ('6','9'), ('9','6')] # pairs if the digit will be in the middle of num
        candidates_single = [('1','1'), ('8','8'), ('0','0')]                       # singles for single digit in the middle of num
        
        # backtracking function
        def backtrack(arr_num, i, j):
            # get the global ans and candidate lists
            nonlocal strobos
            nonlocal candidates_start, candidates_middle, candidates_single
            
            if i > j:
                # the number has been completed, add it to strobos
                strobos.append(''.join(arr_num))
                return
            
            candidates = []     # the list of possible candidates
            if i == j:
                # only 1 digit left
                candidates = candidates_single
            elif i == 0:
                # this pair will make the starting digit
                candidates = candidates_start
            else:
                # all other pairs in the middle
                candidates = candidates_middle
            
            # try a candidate and then move forward
            # return back when done and try the next candidate
            for candidate in candidates:
                arr_num[i], arr_num[j] = candidate
                backtrack(arr_num, i+1, j-1)
                
            # all candidates have been evaluated
            return
        
        # call recursive fn with an arr with size of n (for the str digits)
        backtrack(['0']*n, 0, n-1)        
        return strobos
    
    '''
    Skipped:
        Recursion:
            def findStrobogrammatic(self, n: int) -> List[str]:
                reversible_pairs = [
                    ['0', '0'], ['1', '1'], 
                    ['6', '9'], ['8', '8'], ['9', '6']
                ]

                def generate_strobo_numbers(n, final_length):
                    if n == 0:
                        # 0-digit strobogrammatic number is an empty string.
                        return [""]

                    if n == 1:
                        # 1-digit strobogrammatic numbers.
                        return ["0", "1", "8"]

                    prev_strobo_nums = generate_strobo_numbers(n - 2, final_length)
                    curr_strobo_nums = []

                    for prev_strobo_num in prev_strobo_nums:
                        for pair in reversible_pairs:
                            if pair[0] != '0' or n != final_length:
                                curr_strobo_nums.append(pair[0] + prev_strobo_num + pair[1])

                    return curr_strobo_nums

                return generate_strobo_numbers(n, n)
        
        BFS:
            def findStrobogrammatic(self, n: int) -> List[str]:
                reversible_pairs = [
                    ['0', '0'], ['1', '1'], 
                    ['6', '9'], ['8', '8'], ['9', '6']
                ]

                # When n is even (n % 2 == 0), we start with strings of length 0 and
                # when n is odd (n % 2 == 1), we start with strings of length 1.
                curr_strings_length = n % 2

                q = ["0", "1", "8"] if curr_strings_length == 1 else [""]

                while curr_strings_length < n:
                    curr_strings_length += 2
                    next_level = []

                    for number in q:
                        for pair in reversible_pairs:
                            if curr_strings_length != n or pair[0] != '0':
                                next_level.append(pair[0] + number + pair[1])
                    q = next_level

                return q
    
    Both skipped solutions have the same time and space complexity
    '''
