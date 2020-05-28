import numpy as np
import random


class Game_AI():

    def __init__(self, aggressive_gene, defensive_gene, random_gene, board_size=3):
        """
        Initialize AI
        """
        self._AGGRESSIVE_GENE = int(aggressive_gene)
        self._DEFENSIVE_GENE = int(defensive_gene)
        self._RANDOM_GENE = int(random_gene)

        self._BOARD_SIZE = int(board_size)

    def _make_aggressive_choice(self, self_filled, opponent_filled, possible_positions, log_choice):
        """
        Make aggressive position choice
        """
        rows = {}
        cols = {}
        max_diags_1 = {}
        max_diags_2 = {}
        for i in range(self._BOARD_SIZE):
            rows[i] = []
            cols[i] = []
            max_diags_1[i] = False
            max_diags_2[i] = False
        for i in range(self._BOARD_SIZE):
            count = sum([self_filled[i][j] for j in range(self._BOARD_SIZE)])
            rows[count].append(i)
            count = sum([self_filled[j][i] for j in range(self._BOARD_SIZE)])
            cols[count].append(i)
        count = sum([self_filled[j][j] for j in range(self._BOARD_SIZE)])
        max_diags_1[count] = True
        count = sum([self_filled[self._BOARD_SIZE - 1 - j][j] for j in range(self._BOARD_SIZE)])
        max_diags_2[count] = True

        for count in range(self._BOARD_SIZE - 1, -1, -1):
            position_choices = []
            if len(rows[count]) > 0:
                for row in rows[count]:
                    if sum([opponent_filled[row][j] for j in range(self._BOARD_SIZE)]) == 0:
                        position_choices.extend([[row, j] for j in range(self._BOARD_SIZE) if possible_positions[row][j] == 1])
            if len(cols[count]) > 0:
                for col in cols[count]:
                    if sum([opponent_filled[j][col] for j in range(self._BOARD_SIZE)]) == 0:
                        position_choices.extend([[j, col] for j in range(self._BOARD_SIZE) if possible_positions[j][col] == 1])
            if max_diags_1[count]:
                if sum([opponent_filled[j][j] for j in range(self._BOARD_SIZE)]) == 0:
                    position_choices.extend([[j, j] for j in range(self._BOARD_SIZE) if possible_positions[j][j] == 1])
            if max_diags_2[count]:
                if sum([opponent_filled[self._BOARD_SIZE - 1 - j][j] for j in range(self._BOARD_SIZE)]) == 0:
                    position_choices.extend([[self._BOARD_SIZE - 1 - j, j] for j in range(self._BOARD_SIZE) if possible_positions[self._BOARD_SIZE - 1 - j][j] == 1])
            if len(position_choices) > 0:
                if log_choice:
                    print('Aggressive Choice')
                    print(position_choices)
                return position_choices[random.randint(0, len(position_choices) - 1)]

        return self._make_random_choice(self_filled, opponent_filled, possible_positions, log_choice)

    def _make_defensive_choice(self, self_filled, opponent_filled, possible_positions, log_choice):
        """
        Make defensive position choice
        """
        rows = {}
        cols = {}
        max_diags_1 = {}
        max_diags_2 = {}
        for i in range(self._BOARD_SIZE):
            rows[i] = []
            cols[i] = []
            max_diags_1[i] = False
            max_diags_2[i] = False
        for i in range(self._BOARD_SIZE):
            count = sum([opponent_filled[i][j] for j in range(self._BOARD_SIZE)])
            rows[count].append(i)
            count = sum([opponent_filled[j][i] for j in range(self._BOARD_SIZE)])
            cols[count].append(i)
        count = sum([opponent_filled[j][j] for j in range(self._BOARD_SIZE)])
        max_diags_1[count] = True
        count = sum([opponent_filled[self._BOARD_SIZE - 1 - j][j] for j in range(self._BOARD_SIZE)])
        max_diags_2[count] = True

        for count in range(self._BOARD_SIZE - 1, -1, -1):
            position_choices = []
            if len(rows[count]) > 0:
                for row in rows[count]:
                    if sum([self_filled[row][j] for j in range(self._BOARD_SIZE)]) == 0:
                        position_choices.extend([[row, j] for j in range(self._BOARD_SIZE) if possible_positions[row][j] == 1])
            if len(cols[count]) > 0:
                for col in cols[count]:
                    if sum([self_filled[j][col] for j in range(self._BOARD_SIZE)]) == 0:
                        position_choices.extend([[j, col] for j in range(self._BOARD_SIZE) if possible_positions[j][col] == 1])
            if max_diags_1[count]:
                if sum([self_filled[j][j] for j in range(self._BOARD_SIZE)]) == 0:
                    position_choices.extend([[j, j] for j in range(self._BOARD_SIZE) if possible_positions[j][j] == 1])
            if max_diags_2[count]:
                if sum([self_filled[self._BOARD_SIZE - 1 - j][j] for j in range(self._BOARD_SIZE)]) == 0:
                    position_choices.extend([[self._BOARD_SIZE - 1 - j, j] for j in range(self._BOARD_SIZE) if possible_positions[self._BOARD_SIZE - 1 - j][j] == 1])
            if len(position_choices) > 0:
                if log_choice:
                    print('Defensive Choice')
                    print(position_choices)
                return position_choices[random.randint(0, len(position_choices) - 1)]

        return self._make_random_choice(self_filled, opponent_filled, possible_positions, log_choice)

    def _make_random_choice(self, self_filled, opponent_filled, possible_positions, log_choice):
        """
        Make random position choice
        """
        if log_choice:
            print('Random Choice')
        positions = []
        for i in range(self._BOARD_SIZE):
            for j in range(self._BOARD_SIZE):
                if possible_positions[i][j] == 1:
                    positions.append([i, j])
        return positions[random.randint(0, len(positions) - 1)]

    def choose_position(self, self_filled, opponent_filled, log_choice=False):
        """
        Choose the next fill position
        """
        is_board_empty = True
        is_board_full = True
        possible_positions = [[0 for j in range(self._BOARD_SIZE)] for i in range(self._BOARD_SIZE)]
        for i in range(self._BOARD_SIZE):
            for j in range(self._BOARD_SIZE):
                if self_filled[i][j] == 0 and opponent_filled[i][j] == 0:
                    possible_positions[i][j] = 1
                    is_board_full = False
                else:
                    is_board_empty = False

        # Empty Board
        if is_board_empty:
            return self._make_random_choice(self_filled, opponent_filled, possible_positions, log_choice)
        # Filled Board
        elif is_board_full:
            return
        # Normal Board
        else:
            choice_function = list(np.random.choice([self._make_aggressive_choice, self._make_defensive_choice, self._make_random_choice], 1,
                                                    p=[self._AGGRESSIVE_GENE / 100.0, self._DEFENSIVE_GENE / 100.0, self._RANDOM_GENE / 100.0]))[0]
            return choice_function(self_filled, opponent_filled, possible_positions, log_choice)
