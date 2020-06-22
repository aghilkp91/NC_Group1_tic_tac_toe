from math import inf as infinity
from random import choice

class Game_Minimax():

    def __init__(self, board_size=3):
        """
        Initialize MiniMax
        """
        self._MINIMAX = 1
        self._OTHER_PLAYER = -1

    def empty_cells(self, self_filled, opponent_filled):
        """
        Each empty cell will be added into cells' list
        :param self_filled: the state of the self_filled in current board
        :param opponent_filled: the state of the opponent_filled in current board
        :return: a list of empty cells
        """
        cells = []

        for x in range(3):
            for y in range(3):
                if self_filled[x][y] == 0 and opponent_filled[x][y] == 0:
                    cells.append([x, y])

        return cells

    def wins(self, state, player):
        """
        This function tests if a specific player wins. Possibilities:
        * Three rows    [X X X] or [O O O]
        * Three cols    [X X X] or [O O O]
        * Two diagonals [X X X] or [O O O]
        :param state: the state of the current board
        :param player: a human or a computer
        :return: True if the player wins
        """
        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]
        if [1, 1, 1] in win_state:
            return True
        else:
            return False

    def evaluate(self, self_filled, opponent_filled):
        """
        Function to heuristic evaluation of state.
        :param state: the state of the current board
        :return: +1 if the computer wins; -1 if the human wins; 0 draw
        """
        if self.wins(self_filled, self._MINIMAX):
            score = +1
        elif self.wins(opponent_filled, self._OTHER_PLAYER):
            score = -1
        else:
            score = 0

        return score

    def game_over(self, self_filled, opponent_filled):
        """
        This function test if the human or computer wins
        :param state: the state of the current board
        :return: True if the human or computer wins
        """
        return self.wins(opponent_filled, self._OTHER_PLAYER) or self.wins(self_filled, self._MINIMAX)

    def minimax(self, self_filled, opponent_filled, depth, player, log_choice=False):
        """
        AI function that choice the best move
        :param state: current state of the board
        :param depth: node index in the tree (0 <= depth <= 9),
        but never nine in this case (see iaturn() function)
        :param player: an human or a computer
        :return: a list with [the best row, best col, best score]
        """
        if player == self._MINIMAX:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        if depth == 0 or self.game_over(self_filled, opponent_filled):
            score = self.evaluate(self_filled ,opponent_filled)
            return [-1, -1, score]

        for cell in self.empty_cells(self_filled, opponent_filled):
            x, y = cell[0], cell[1]
            if player == self._MINIMAX:
                self_filled[x][y] = 1
            else:
                opponent_filled[x][y] = 1
            score = self.minimax(self_filled, opponent_filled, depth - 1, -player)
            if player == self._MINIMAX:
                self_filled[x][y] = 0
            else:
                opponent_filled[x][y] = 0
            score[0], score[1] = x, y

            if player == self._MINIMAX:
                if score[2] > best[2]:
                    best = score  # max value
            else:
                if score[2] < best[2]:
                    best = score  # min value

        return best

    def choose_position(self, self_filled, opponent_filled, log_choice=False):
        """
        Choose the next fill position
        """
        is_board_empty = True
        is_board_full = True
        possible_positions = self.empty_cells(self_filled, opponent_filled)
        depth = len(possible_positions)

        # Empty Board
        if depth == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
            return [x, y]
        # Filled Board
        elif depth == 0 or self.game_over(self_filled, opponent_filled):
            return
        # Normal Board
        else:
            move = self.minimax(self_filled, opponent_filled, depth, self._MINIMAX)
            x, y = move[0], move[1]
            return [x, y]