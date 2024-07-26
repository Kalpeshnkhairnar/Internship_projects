import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

class TicTacToe:
    def __init__(self):
        self.board = self.initial_state()

    def initial_state(self):
        """
        Returns the starting state of the board.
        """
        return [[EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY]]

    def get_diagonals(self):
        """
        Returns the diagonals of the board.
        """
        return [[self.board[0][0], self.board[1][1], self.board[2][2]],
                [self.board[0][2], self.board[1][1], self.board[2][0]]]

    def get_columns(self):
        """
        Returns the columns of the board.
        """
        return [[self.board[row][col] for row in range(3)] for col in range(3)]

    def three_in_a_row(self, line):
        """
        Returns True if all elements in the line are the same and not EMPTY.
        """
        return line[0] is not None and line.count(line[0]) == 3

    def player(self):
        """
        Returns the player who has the next turn on the board.
        """
        count_x = sum(row.count(X) for row in self.board)
        count_o = sum(row.count(O) for row in self.board)
        return O if count_x > count_o else X

    def actions(self):
        """
        Returns set of all possible actions (i, j) available on the board.
        """
        return {(i, j) for i in range(3) for j in range(3) if self.board[i][j] == EMPTY}

    def result(self, action):
        """
        Returns the board that results from making move (i, j) on the board.
        """
        if self.board[action[0]][action[1]] is not EMPTY:
            raise ValueError("Invalid move")
        
        next_player = self.player()
        new_board = deepcopy(self.board)
        new_board[action[0]][action[1]] = next_player
        return new_board

    def winner(self):
        """
        Returns the winner of the game, if there is one.
        """
        lines = self.board + self.get_columns() + self.get_diagonals()
        for line in lines:
            if self.three_in_a_row(line):
                return line[0]
        return None

    def terminal(self):
        """
        Returns True if the game is over, False otherwise.
        """
        return self.winner() is not None or all(cell is not EMPTY for row in self.board for cell in row)

    def utility(self):
        """
        Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
        """
        win = self.winner()
        if win == X:
            return 1
        elif win == O:
            return -1
        return 0

    def max_value(self, alpha, beta):
        if self.terminal():
            return self.utility(), None
        
        v = float('-inf')
        best_action = None
        
        for action in self.actions():
            self.board = self.result(action)
            min_result = self.min_value(alpha, beta)[0]
            if min_result > v:
                v = min_result
                best_action = action
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        
        return v, best_action

    def min_value(self, alpha, beta):
        if self.terminal():
            return self.utility(), None
        
        v = float('inf')
        best_action = None
        
        for action in self.actions():
            self.board = self.result(action)
            max_result = self.max_value(alpha, beta)[0]
            if max_result < v:
                v = max_result
                best_action = action
            beta = min(beta, v)
            if alpha >= beta:
                break
        
        return v, best_action

    def minimax(self):
        """
        Returns the optimal action for the current player on the board.
        """
        if self.terminal():
            return None
        
        current_player = self.player()
        if current_player == X:
            return self.max_value(float('-inf'), float('inf'))[1]
        else:
            return self.min_value(float('-inf'), float('inf'))[1]

    def print_board(self):
        """
        Print the board to the console.
        """
        for row in self.board:
            print(' | '.join([cell if cell else ' ' for cell in row]))
            print('-' * 5)

    def play_game(self):
        """
        Play a game of Tic-Tac-Toe with the user.
        """
        while not self.terminal():
            self.print_board()
            if self.player() == X:
                print("Player X's turn")
                row = int(input("Enter row (0, 1, 2): "))
                col = int(input("Enter column (0, 1, 2): "))
                if (row, col) not in self.actions():
                    print("Invalid move. Try again.")
                    continue
                self.board = self.result((row, col))
            else:
                print("Player O's turn (AI)")
                action = self.minimax()
                if action:
                    self.board = self.result(action)

        self.print_board()
        winner = self.winner()
        if winner:
            print(f"Player {winner} wins!")
        else:
            print("It's a tie!")

if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()
