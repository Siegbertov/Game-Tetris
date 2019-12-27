import pygame
import numpy as np
import random
from copy import deepcopy

pygame.init()
pygame.display.set_caption('TETRIS')
clock = pygame.time.Clock()
MOVEEVENT, t = pygame.USEREVENT+1, 500
pygame.time.set_timer(MOVEEVENT, t)