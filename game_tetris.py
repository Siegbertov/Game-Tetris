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
    COLORS = [RED, GREEN, BLUE, ORANGE, YELLOW, PINK, LIGHT_BLUE]


class Metadata(Colors):
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 700

    PLAY_ZONE_WIDTH = 400
    PLAY_ZONE_HEIGHT = 600
    PLAY_ZONE_X = (SCREEN_WIDTH - PLAY_ZONE_WIDTH) // 2
    PLAY_ZONE_Y = SCREEN_HEIGHT - PLAY_ZONE_HEIGHT
    CEIL_SIZE = 40
    UPPER_PADDING = 4
    ROW_NUM = PLAY_ZONE_HEIGHT // CEIL_SIZE + UPPER_PADDING
    COLUMN_NUM = PLAY_ZONE_WIDTH // CEIL_SIZE

    ver_line = [[1],
                [1],
                [1],
                [1]]
    hor_line = [[1, 1, 1, 1]]

    cube = [[1, 1],
            [1, 1]]

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

    hor_Z = [[1, 1, 0],
             [0, 1, 1]]
    ver_Z = [[0, 1],
             [1, 1],
             [1, 0]]

    hor_S = [[0, 1, 1],
             [1, 1, 0]]
    ver_S = [[1, 0],
             [1, 1],
             [0, 1]]

    up_L = [[1, 0],
            [1, 0],
            [1, 1]]
    right_L = [[1, 1, 1],
               [1, 0, 0]]
    down_L = [[1, 1],
              [0, 1],
              [0, 1]]
    left_L = [[0, 0, 1],
              [1, 1, 1]]

    up_J = [[0, 1],
            [0, 1],
            [1, 1]]
    right_J = [[1, 0, 0],
               [1, 1, 1]]
    down_J = [[1, 1],
              [1, 0],
              [1, 0]]
    left_J = [[1, 1, 1],
              [0, 0, 1]]

    all_pieces = [ver_line, hor_line,
                  cube,
                  up_T, right_T, down_T, left_T,
                  hor_Z, ver_Z,
                  hor_S, ver_S,
                  up_L, right_L, down_L, left_L,
                  up_J, right_J, down_J, left_J]