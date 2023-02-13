# My imports
from collections import defaultdict

class Solution:
    '''
        Incomplete
    '''
    
    def pushDominoes(self, dominoes: str) -> str:
        next_move = defaultdict(list)
        n = len(dominoes)
        
        if n == 1:
            return dominoes
        dominoes = list(dominoes)
        
        while True:
            for i, move in enumerate(dominoes):
                if move == 'L':
                    next_move[i-1].append('L')
                elif move == 'R':
                    next_move[i+1].append('R')
                    
            for potential in list(next_move.keys()):
                if potential < 0 or potential >= n:
                    del next_move[potential]
                
                elif dominoes[potential] != '.':
                    del next_move[potential]
                
                elif len(next_move[potential]) > 1:
                    del next_move[potential]
            
            if len(next_move) == 0:
                break
            else:
                for idx, move in next_move.items():
                    dominoes[idx] = move[0]
                next_move.clear()
        
        return ''.join(dominoes)
