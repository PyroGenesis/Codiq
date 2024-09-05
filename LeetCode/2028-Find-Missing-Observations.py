from typing import List


class Solution:
    def missingRolls(self, rolls: List[int], mean: int, n: int) -> List[int]:
        return self.missingRollsMath(rolls, mean, n)
    
    '''
    Math
        For n rolls, we can roll the range [n, 6n] so make sure that is enough to reach mean
        We can find the total sum by multiplying the mean by m + n. 
        Next, we subtract the sum of the m known throws from this total sum to get the sum of the missing n throws.
        If we know the sum of the missing n throws, we can distribute it like so:
            [need // n, need // n ... (n times)] + [1, 1, 1, (need % n times)]
            Here the + is not concatenation, its element-wise addition
    
        Time:  O(m+n) ~ O(max(m,n))
            curr_sum:   O(m)
            new_rolls:  O(n)
    '''
    def missingRollsMath(self, rolls: List[int], mean: int, n: int) -> List[int]:        
        curr_rolls = len(rolls)
        curr_sum = sum(rolls)
        
        # computing sum of n rolls needed to satisfy mean
        final_rolls = curr_rolls + n
        final_sum = final_rolls * mean
        need = final_sum - curr_sum

        # check upper and lower bounds
        if need < n or need > 6*n:
            return []
        
        # its possible just need to distribute
        base, remainder = divmod(need, n)
        new_rolls = [base]*n
        for i in range(remainder):
            new_rolls[i] += 1
        return new_rolls

    '''
    Simulation
        For n rolls, we can roll the range [n, 6n] so make sure that is enough to reach mean
        Go through all n rolls one by one
            Calculate the roll that gets curr_mean closest to target mean and add it to rolls
    
        Time:  O(m+n) ~ O(max(m,n))
            curr_sum:   O(m)
            new_rolls:  O(n)
    '''
    def missingRollsSimulate(self, rolls: List[int], mean: int, n: int) -> List[int]:
        curr_rolls = len(rolls)
        curr_sum = sum(rolls)
        
        # computing sum of n rolls needed to satisfy mean
        final_rolls = curr_rolls + n
        final_sum = final_rolls * mean
        need = final_sum - curr_sum
        
        # check upper and lower bounds
        if need < n or need > 6*n:
            return []
        # check shortcut
        if need % n == 0:
            return [need // n] * n
        
        # its possible, just need to figure out the rolls
        new_rolls = []
        for _ in range(n):
            curr_rolls += 1
            need = curr_rolls*mean - curr_sum
            roll = max(1, min(6, need))
            curr_sum += roll
            new_rolls.append(roll)
        return new_rolls
