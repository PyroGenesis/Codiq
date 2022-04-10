from typing import List

class Solution:
    '''
    Stack
        This solution requires no explanation
        Time:  O(n)
        Space: O(n) [storing all scores]
    '''
    def calPoints(self, ops: List[str]) -> int:
        scores = []     # stack to maintain scores
        
        for op in ops:
            if op == '+':
                # adding last two scores as a new score
                scores.append(scores[-1] + scores[-2])
            elif op == 'D':
                # doubling last score and adding it as a new score
                scores.append(scores[-1] * 2)
            elif op == 'C':
                # deleting last score
                scores.pop()
            else:
                # adding a new score
                scores.append(int(op))
        
        # returning the sum of all scores
        return sum(scores)
