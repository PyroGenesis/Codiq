
class TicTacToeOptimal:
    def __init__(self, n: int):
        # save size for later
        self.n = n

        # The score for a particular row / column / diagonal is represented as follows:
        #   negative for player 1
        #   positive for player 2 

        # self.row_score[i] indicates the score for row i 
        self.row_score = [0]*n
        # self.col_score[j] indicates the score for column j
        self.col_score = [0]*n
        # scores for both diagonals
        self.primary_diag_score = 0
        self.secondary_diag_score = 0
    
    def move(self, row: int, col: int, player: int) -> int:
        # Scores:
        #   player 1 -> -1, player 2 -> 1
        player_score = 2*player - 3

        # update row, col and (if necessary) diags
        self.row_score[row] += player_score
        self.col_score[col] += player_score
        if row == col: self.primary_diag_score += player_score
        if row + col == self.n - 1: self.secondary_diag_score += player_score

        # check if player won
        if (abs(self.row_score[row]) == self.n or
            abs(self.col_score[col]) == self.n or
            abs(self.primary_diag_score) == self.n or
            abs(self.secondary_diag_score) == self.n):
            return player
        
        # if no-one won
        return 0


class TicTacToeSimple:
    def __init__(self, n: int):
        # save size for later
        self.n = n
        # 2D board portraying game state
        self.field = [[0 for _ in range(n)] for _ in range(n)]
    
    def _checkRow(self, row: int, player: int) -> bool:
        # check if player has completed specified row
        for j in range(self.n):
            if self.field[row][j] != player:
                return False
        return True

    def _checkCol(self, col: int, player: int) -> bool:
        # check if player has completed specified column
        for i in range(self.n):
            if self.field[i][col] != player:
                return False
        return True

    def _checkPrimaryDiag(self, player: int) -> bool:
        # check if player has completed the primary diagonal 
        #   (0, 0), (1, 1) ... (n-1, n-1)
        for i in range(self.n):
            if self.field[i][i] != player:
                return False
        return True
    
    def _checkSecondaryDiag(self, player: int) -> bool:
        # check if player has completed the secondary diagonal 
        #   (0, n-1), (1, n-2) ... (n-1, 0)
        for i in range(self.n):
            if self.field[i][self.n-1-i] != player:
                return False
        return True

    def _checkDiag(self, row: int, col: int, player: int) -> bool:
        # check if player has completed primary or secondary diagonals
        won = False
        if row == col: 
            won = self._checkPrimaryDiag(player)
        if not won and row + col == self.n - 1: 
            won = self._checkSecondaryDiag(player)
        return won            

    def move(self, row: int, col: int, player: int) -> int:
        # put move on the board
        self.field[row][col] = player

        # check if player has won by row
        won = self._checkRow(row, player)
        # check if player has won by column
        if not won: won = self._checkCol(col, player)
        # check if player has won by diagonal
        if not won: won = self._checkDiag(row, col, player)
        
        # return player if they have won, else 0
        return player if won else 0


class TicTacToe(TicTacToeOptimal):
    pass


# Your TicTacToe object will be instantiated and called as such:
# obj = TicTacToe(n)
# param_1 = obj.move(row,col,player)