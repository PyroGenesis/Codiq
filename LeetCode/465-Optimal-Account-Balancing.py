from collections import defaultdict
from typing import List

class Solution:
    def minTransfers(self, transactions: List[List[int]]) -> int:
        # according to constraints, there can only be 12 people
        n = 12

        # initializing final balance state for 12 people
        state = [0]*n
        for a, b, p in transactions:
            # compute final tally for every person
            state[a] -= p
            state[b] += p
        
        def backtrack(curr: int):
            nonlocal state, n
            # skip 0 balance people
            while curr < n and state[curr] == 0:
                curr += 1
            # if every person has been balanced, we are at the end of the stack
            #   so no more operations needed so return 0
            if curr == n:
                return 0
            
            # track the least amount of transactions, using the max number of people as a loose upper limit
            best = n
            for nxt in range(curr+1, n):
                # skip if state[nxt] is same sign or 0
                if state[curr] * state[nxt] >= 0:
                    continue
                
                # transfer money / debt from curr to nxt
                amount = state[curr] # min(u, abs(v))
                # we don't need to clear the value in curr because we are not going to access it again in the recursive calls
                # state[curr] -= amount     
                state[nxt] += amount
                # continue settling more debts recursively
                best = min(best, 1 + backtrack(curr + 1))
                # we don't refill the value in curr because we never cleared it
                # state[curr] += amount
                state[nxt] -= amount
            
            return best

        # start backtracking from the 0th transaction
        return backtrack(0)
    
    '''
    This backtracking fn is flawed because it recalculates a ton of already calculated states
    '''
    def minTransfersBacktrackFlawed(self, transactions: List[List[int]]) -> int:
        # upper limit for number of transactions == number of transactions used to get in this mess
        max_transactions = len(transactions)

        # according to constraints, there can only be 12 people
        state = [0]*12
        for a, b, p in transactions:
            # compute final tally for every person
            state[a] -= p
            state[b] += p
        
        def backtrack(curr: int):
            nonlocal state, max_transactions
            # if our chain is exceeding the number of initial transactions, fail early
            if curr >= max_transactions:
                return max_transactions
            
            # check whether debt is settled
            for x in state:
                if x != 0:
                    break
            else:
                return curr

            # track the least amount of transactions, using max_transactions as an upper limit
            best = max_transactions
            for i, u in enumerate(state):
                # find a person with a positive balance
                if u <= 0:
                    continue
                
                for j, v in enumerate(state):
                    # find a person with a negative balance
                    if v >= 0:
                        continue
                    
                    # transfer all excess cash of net positive person to net negative person
                    amount = u # min(u, abs(v))
                    state[i] -= amount
                    state[j] += amount
                    # continue settling more debts recursively
                    best = min(best, backtrack(curr + 1))
                    # reverse the transfer
                    state[i] += amount
                    state[j] -= amount
            
            return best

        # start backtracking from the 0th transaction
        return backtrack(0)
    