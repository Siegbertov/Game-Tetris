import pygame
import numpy as np
import random
from copy import deepcopy

pygame.init()
pygame.display.set_caption('TETRIS')
clock = pygame.time.Clock()
MOVEEVENT, t = pygame.USEREVENT+1, 500
pygame.time.set_timer(MOVEEVENT, t)

def quit_game():
    pygame.quit()
    quit()


class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    ORANGE = (255, 168, 0)
    YELLOW = (255, 255, 0)
    PINK = (255, 0, 255)
    LIGHT_BLUE = (0, 255, 255)
    COLORS = [WHITE, RED, GREEN, BLUE, ORANGE, YELLOW, PINK, LIGHT_BLUE]


class Metadata(Colors):
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 700

    PLAY_ZONE_WIDTH = 400
    PLAY_ZONE_HEIGHT = 600
    PLAY_ZONE_X = (SCREEN_WIDTH - PLAY_ZONE_WIDTH) // 2
    PLAY_ZONE_Y = SCREEN_HEIGHT - PLAY_ZONE_HEIGHT
    CEIL_SIZE = 50
    UPPER_PADDING = 4
    ROW_NUM = PLAY_ZONE_HEIGHT // CEIL_SIZE + UPPER_PADDING
    COLUMN_NUM = PLAY_ZONE_WIDTH // CEIL_SIZE

    up_T = [[0, 1, 0],
            [1, 1, 1]]
    right_T = [[1, 0],
               [1, 1],
               [1, 0]]
    down_T = [[1, 1, 1],
              [0, 1, 0]]
    left_T = [[0, 1],
              [1, 1],
              [0, 1]]

    up_L = [[2, 0],
            [2, 0],
            [2, 2]]
    right_L = [[2, 2, 2],
               [2, 0, 0]]
    down_L = [[2, 2],
              [0, 2],
              [0, 2]]
    left_L = [[0, 0, 2],
              [2, 2, 2]]

    up_J = [[0, 3],
            [0, 3],
            [3, 3]]
    right_J = [[3, 0, 0],
               [3, 3, 3]]
    down_J = [[3, 3],
              [3, 0],
              [3, 0]]
    left_J = [[3, 3, 3],
              [0, 0, 3]]

    ver_line = [[4],
                [4],
                [4],
                [4]]
    hor_line = [[4, 4, 4, 4]]

    hor_Z = [[5, 5, 0],
             [0, 5, 5]]
    ver_Z = [[0, 5],
             [5, 5],
             [5, 0]]

    hor_S = [[0, 6, 6],
             [6, 6, 0]]
    ver_S = [[6, 0],
             [6, 6],
             [0, 6]]

    cube = [[7, 7],
            [7, 7]]

    all_pieces = [up_T, right_T, down_T, left_T,
                  up_L, right_L, down_L, left_L,
                  up_J, right_J, down_J, left_J,
                  ver_line, hor_line,
                  hor_Z, ver_Z,
                  hor_S, ver_S,
                  cube]


class Pieces(Metadata):
    def __init__(self):
        self.empty_upper_board = self.create_empty_board()
        self.empty_col_num = len(self.empty_upper_board[0])

    def create_empty_board(self):
        return np.zeros((self.ROW_NUM, self.COLUMN_NUM))

    def get_random_piece(self):
        return random.choice(self.all_pieces)

    def insert_piece_in_board(self):
        random_piece = self.get_random_piece()
        row = self.UPPER_PADDING - len(random_piece)
        col = random.randrange(self.empty_col_num - len(random_piece[0]))
        copy_board = deepcopy(self.empty_upper_board)
        for r in range(len(random_piece)):
            for c in range(len(random_piece[0])):
                copy_board[row + r][col + c] = random_piece[r][c]
        return copy_board


class Game(Pieces):
    def __init__(self):
        super().__init__()
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.run = True

        self.main_board = np.zeros((self.ROW_NUM, self.COLUMN_NUM))
        self.upper_board = self.insert_piece_in_board()

    #                                                                                                       MOVING RIGHT
    def piece_touch_right_side(self):
        for r in range(len(self.upper_board)):
            if self.upper_board[r][-1] != 0:
                return True
        return False

    def blockage_on_right_side(self):
        for r in range(len(self.upper_board)):
            for c in range(len(self.upper_board[0]) - 1):
                if self.upper_board[r][c] == self.main_board[r][c + 1] and self.upper_board[r][c] != 0:
                    return True
        return False

    def possible_to_move_right(self):
        if self.blockage_on_right_side() or  self.piece_touch_right_side():
            return False
        return True

    def move_right(self):
        if self.possible_to_move_right():
            new_order = []
            num_of_col = len(self.upper_board[0])
            for c in range(num_of_col):
                if c == 0:
                    new_order.append(num_of_col - 1)
                else:
                    new_order.append(c - 1)
            self.upper_board = self.upper_board[:, new_order]

    #                                                                                                        MOVING LEFT
    def piece_touch_left_side(self):
        for r in range(len(self.upper_board)):
            if self.upper_board[r][0] != 0:
                return True
        return False

    def blockage_on_left_side(self):
        for r in range(len(self.upper_board)):
            for c in range(1, len(self.upper_board[0])):
                if self.upper_board[r][c] == self.main_board[r][c - 1] and self.upper_board[r][c] != 0:
                    return True
        return False

    def possible_to_move_left(self):
        if self.blockage_on_left_side() or self.piece_touch_left_side():
            return False
        return True

    def move_left(self):
        if self.possible_to_move_left():
            new_order = []
            num_of_col = len(self.upper_board[0])
            for c in range(num_of_col):
                if c == num_of_col - 1:
                    new_order.append(0)
                else:
                    new_order.append(c + 1)
            self.upper_board = self.upper_board[:, new_order]

    #                                                                                                       FALLING DOWN
    def piece_touch_bottom_side(self):
        last_row = self.upper_board[-1]
        for el in last_row:
            if el != 0:
                return True
        return False

    def blockage_on_bottom_side(self):
        for r in range(len(self.upper_board) - 1):
            for c in range(len(self.upper_board[0])):
                if self.upper_board[r][c] != 0 and self.main_board[r+1][c] != 0:
                    return True
        return False

    def possible_to_move_down(self):
        if self.blockage_on_bottom_side() or self.piece_touch_bottom_side():
            return False
        return True

    def tick_tick_tick(self):
        if self.possible_to_move_down():
            new_board = []
            num_of_rows = len(self.upper_board)
            for r in range(num_of_rows):
                if r == 0:
                    new_board.append(self.upper_board[num_of_rows-1])
                else:
                    new_board.append(self.upper_board[r - 1])
            self.upper_board = np.array(new_board)
        else:
            self.main_board = self.main_board + self.upper_board
            self.upper_board = self.insert_piece_in_board()

    #                                                                                                       CHECK LOSING
    def you_lose(self):
        for c in range(len(self.main_board[0])):
            if self.main_board[3][c] != 0:
                return True
        return False

    #                                                                                                  COMBO COMBO COMBO
    def check_each_row(self):
        for r in range(len(self.main_board)):
            if all(self.main_board[r]):
                self.reduce_and_shift(r)

    def reduce_and_shift(self, num_of_row):
        for num in range(num_of_row, 3, -1):
            self.main_board[num] = self.main_board[num-1]

    #                                                                                                          REDRAWING
    def draw_play_zone(self):
        pygame.draw.rect(self.SCREEN, self.BLACK,
                         (self.PLAY_ZONE_X, self.PLAY_ZONE_Y, self.PLAY_ZONE_WIDTH, self.PLAY_ZONE_HEIGHT), 3)
        for hor in range(self.ROW_NUM- self.UPPER_PADDING):
            pygame.draw.line(self.SCREEN, self.BLACK, (self.PLAY_ZONE_X, self.PLAY_ZONE_Y + hor * self.CEIL_SIZE), (self.PLAY_ZONE_X + self.PLAY_ZONE_WIDTH, self.PLAY_ZONE_Y + hor * self.CEIL_SIZE), 3)

        for ver in range(self.COLUMN_NUM):
            pygame.draw.line(self.SCREEN, self.BLACK, (self.PLAY_ZONE_X + ver * self.CEIL_SIZE, self.PLAY_ZONE_Y), (self.PLAY_ZONE_X + ver * self.CEIL_SIZE, self.SCREEN_HEIGHT), 3)

    def draw_pieces(self):
        for r in range(self.UPPER_PADDING, len(self.upper_board)):
            for c in range(len(self.upper_board[0])):
                x = self.PLAY_ZONE_X + c * self.CEIL_SIZE
                y = self.PLAY_ZONE_Y + (r - self.UPPER_PADDING) * self.CEIL_SIZE
                if self.upper_board[r][c] != 0:
                    pygame.draw.rect(self.SCREEN, self.COLORS[int(self.upper_board[r][c])], (x, y, self.CEIL_SIZE, self.CEIL_SIZE))
                if self.main_board[r][c] != 0:
                    pygame.draw.rect(self.SCREEN, self.COLORS[int(self.main_board[r][c])], (x, y, self.CEIL_SIZE, self.CEIL_SIZE))

    def redraw_screen(self):
        self.SCREEN.fill(self.WHITE)
        self.draw_pieces()
        self.draw_play_zone()
        self.check_each_row()
        if self.you_lose():
            self.loser_screen()
        pygame.display.update()

    def loser_screen(self):
        s = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        s.set_alpha(40)
        s.fill(self.RED)
        self.SCREEN.blit(s, (0, 0))


def game_loop():
    new_game = Game()
    while new_game.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == MOVEEVENT:
                if not new_game.you_lose():
                    new_game.tick_tick_tick()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

                if event.key == pygame.K_RIGHT:
                    new_game.move_right()

                if event.key == pygame.K_LEFT:
                    new_game.move_left()

                if event.key == pygame.K_DOWN:
                    new_game.tick_tick_tick()

        new_game.redraw_screen()

game_loop()

