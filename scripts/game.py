import pygame

from game_ai import Game_AI


class Game():

    SHAPE_X = 'X'
    SHAPE_O = 'O'
    PLAYER1 = 'PLAYER 1'
    PLAYER2 = 'PLAYER 2'

    def __init__(self, board_width, board_height, should_use_ai, ai_genes, background=(0, 0, 0), line_color=(0, 255, 0), line_thickness=3, shape_thickness=2):
        """
        Initialize game state
        """
        self._BOARD_WIDTH = int(board_width)
        self._BOARD_HEIGHT = int(board_height)
        self._BACKGROUND = tuple([int(color) for color in background])
        self._LINE_COLOR = tuple([int(color) for color in line_color])
        self._LINE_THICKNESS = int(line_thickness)
        self._SHAPE_THICKNESS = int(shape_thickness)

        self._PLAYER_SHAPES = {}
        self._PLAYER_SHAPES[Game.PLAYER1] = Game.SHAPE_X
        self._PLAYER_SHAPES[Game.PLAYER2] = Game.SHAPE_O

        self._should_reset = True
        self._reset()

        if bool(should_use_ai):
            aggressive_gene = float(ai_genes[0])
            defensive_gene = float(ai_genes[1])
            random_gene = float(ai_genes[2])
            self._game_ai = Game_AI(aggressive_gene, defensive_gene, random_gene)
        else:
            self._game_ai = None

    def _set_clicked_position(self, coordinate):
        """
        Set clicked grid position based upon given mouse click coordinate
        """
        pos_x = 0
        pos_y = 0
        if coordinate[0] > ((1 / 3.0) * self._BOARD_WIDTH):
            if coordinate[0] > ((2 / 3.0) * self._BOARD_WIDTH):
                pos_x = 2
            else:
                pos_x = 1
        if coordinate[1] > ((1 / 3.0) * self._BOARD_HEIGHT):
            if coordinate[1] > ((2 / 3.0) * self._BOARD_HEIGHT):
                pos_y = 2
            else:
                pos_y = 1
        return (pos_y, pos_x)

    def notify_click(self, coordinate):
        """
        Notify about a click event
        """
        if self._is_over and self._has_shown_message:
            self._should_reset = True
        elif self._player_1_can_click:
            position = self._set_clicked_position(coordinate)
            if self._player_1_filled[position[0]][position[1]] == 1 or self._player_2_filled[position[0]][position[1]] == 1:
                return
            self._player_1_filled[position[0]][position[1]] = 1
            self._clicked_position = position
            self._player_1_can_click = False
            self._player_2_can_click = True
        elif self._game_ai is None and self._player_2_can_click:
            position = self._set_clicked_position(coordinate)
            if self._player_1_filled[position[0]][position[1]] == 1 or self._player_2_filled[position[0]][position[1]] == 1:
                return
            self._player_2_filled[position[0]][position[1]] = 1
            self._clicked_position = position
            self._player_2_can_click = False
            self._player_1_can_click = True

    def _init_board(self, screen):
        """
        Draws the board grid
        """
        screen.fill(self._BACKGROUND)
        pygame.draw.lines(screen, self._LINE_COLOR, False, ((self._BOARD_WIDTH / 3.0, 0), (self._BOARD_WIDTH / 3.0, self._BOARD_HEIGHT)), self._LINE_THICKNESS)
        pygame.draw.lines(screen, self._LINE_COLOR, False, ((2 * self._BOARD_WIDTH / 3.0, 0), (2 * self._BOARD_WIDTH / 3.0, self._BOARD_HEIGHT)), self._LINE_THICKNESS)
        pygame.draw.lines(screen, self._LINE_COLOR, False, ((0, self._BOARD_HEIGHT / 3.0), (self._BOARD_WIDTH, self._BOARD_HEIGHT / 3.0,)), self._LINE_THICKNESS)
        pygame.draw.lines(screen, self._LINE_COLOR, False, ((0, 2 * self._BOARD_HEIGHT / 3.0), (self._BOARD_WIDTH, 2 * self._BOARD_HEIGHT / 3.0,)), self._LINE_THICKNESS)

    def _draw_shape(self, screen):
        """
        Draw the specified shape in the given board position
        """
        if self._PLAYER_SHAPES[self._current_player] == Game.SHAPE_X:
            x_1 = self._clicked_position[1] * self._BOARD_WIDTH / 3.0 + ((1 / 4.0) * (self._BOARD_WIDTH / 3.0))
            y_1 = self._clicked_position[0] * self._BOARD_HEIGHT / 3.0 + ((1 / 4.0) * (self._BOARD_HEIGHT / 3.0))
            x_2 = self._clicked_position[1] * self._BOARD_WIDTH / 3.0 + ((3 / 4.0) * (self._BOARD_WIDTH / 3.0))
            y_2 = self._clicked_position[0] * self._BOARD_HEIGHT / 3.0 + ((3 / 4.0) * (self._BOARD_HEIGHT / 3.0))
            pygame.draw.lines(screen, self._LINE_COLOR, False, ((x_1, y_1), (x_2, y_2)), self._SHAPE_THICKNESS)
            pygame.draw.lines(screen, self._LINE_COLOR, False, ((x_2, y_1), (x_1, y_2)), self._SHAPE_THICKNESS)
        elif self._PLAYER_SHAPES[self._current_player] == Game.SHAPE_O:
            x = self._clicked_position[1] * self._BOARD_WIDTH / 3.0 + ((1 / 2.0) * (self._BOARD_WIDTH / 3.0))
            y = self._clicked_position[0] * self._BOARD_HEIGHT / 3.0 + ((1 / 2.0) * (self._BOARD_HEIGHT / 3.0))
            pygame.draw.circle(screen, self._LINE_COLOR, (int(x), int(y)), int((3 / 8.0) * (self._BOARD_HEIGHT / 3.0)), self._SHAPE_THICKNESS)

    def _show_winner(self, screen, font='Arial', font_size=32, font_color=(0, 0, 255)):
        """
        Displays the winner of the game
        """
        message = self._winning_player + ' WINS!' if self._winning_player is not None else 'TIE!'
        message_x = self._BOARD_WIDTH / 2.0 - ((len(message) / 90.0) * self._BOARD_WIDTH)
        message_y = self._BOARD_HEIGHT / 2.0 - ((1 / 20.0) * self._BOARD_HEIGHT)
        screen.blit(pygame.font.SysFont(font, font_size).render(message, False, font_color, self._BACKGROUND), (message_x, message_y))

    def draw(self, screen):
        """
        Draw the current game state
        """
        if self._should_reset:
            self._init_board(screen)
        if self._clicked_position is not None:
            self._draw_shape(screen)
            self._current_player = Game.PLAYER1 if self._current_player == Game.PLAYER2 else Game.PLAYER2
            self._clicked_position = None
        if self._is_over and not self._has_shown_message:
            self._show_winner(screen)
            self._has_shown_message = True

    def _reset(self, starting_player=PLAYER2):
        """
        Reset the game state
        """
        self._is_over = False
        self._has_shown_message = False
        self._current_player = starting_player
        self._winning_player = None
        self._player_1_can_click = self._current_player == Game.PLAYER1
        self._player_2_can_click = self._current_player == Game.PLAYER2
        self._clicked_position = None

        self._player_1_filled = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self._player_2_filled = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def _check_if_game_over(self):
        """
        Check if the game is over based on the player filled tuple
        """
        if self._is_over:
            return True
        self._is_over = False
        for i in range(3):
            if (sum([self._player_1_filled[i][j] for j in range(3)]) > 2) or (sum([self._player_1_filled[j][i] for j in range(3)]) > 2):
                self._is_over = True
                self._winning_player = Game.PLAYER1
                return True
            elif (sum([self._player_2_filled[i][j] for j in range(3)]) > 2) or (sum([self._player_2_filled[j][i] for j in range(3)]) > 2):
                self._is_over = True
                self._winning_player = Game.PLAYER2
                return True
        if (self._player_1_filled[0][0] + self._player_1_filled[1][1] + self._player_1_filled[2][2] > 2) or (self._player_1_filled[0][2] + self._player_1_filled[1][1] + self._player_1_filled[2][0] > 2):
            self._is_over = True
            self._winning_player = Game.PLAYER1
            return True
        if (self._player_2_filled[0][0] + self._player_2_filled[1][1] + self._player_2_filled[2][2] > 2) or (self._player_2_filled[0][2] + self._player_2_filled[1][1] + self._player_2_filled[2][0] > 2):
            self._is_over = True
            self._winning_player = Game.PLAYER2
            return True
        if sum([sum([self._player_1_filled[i][j] for i in range(3)]) for j in range(3)]) + sum([sum([self._player_2_filled[i][j] for i in range(3)]) for j in range(3)]) > 8:
            self._is_over = True
            return True
        return False

    def update(self, screen):
        """
        Update the game state
        """
        if self._should_reset:
            self._reset()
            self._should_reset = False
        elif self._is_over:
            return
        elif self._check_if_game_over():
            self._is_over = True
            self._player_1_can_click = False
            self._player_2_can_click = False
            self._clicked_position = None
        elif self._game_ai is not None and self._player_2_can_click:
            position = self._game_ai.choose_position(self._player_2_filled, self._player_1_filled)
            if position is not None:
                self._player_2_filled[position[0]][position[1]] = 1
                self._clicked_position = position
                self._current_player = Game.PLAYER2
                self._draw_shape(screen)
            self._player_2_can_click = False
            self._player_1_can_click = True
            self._clicked_position = None
            self._current_player = Game.PLAYER1
