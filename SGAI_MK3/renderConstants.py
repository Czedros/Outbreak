import pygame
import constants
#Don't want to make edit in main filec
constants.ROWS = 13
constants.LINE_WIDTH = 1
###
CYCLELEN = 10
NOONLENGTH = 2

SIZE = 700
GRIDDIST = 0.112
GRIDRECT = pygame.Rect(GRIDDIST * SIZE, GRIDDIST * SIZE, SIZE * (1 - 2 * GRIDDIST) + 2, SIZE * (1 - 2 * GRIDDIST) + 2)
CELLSIZE = int((GRIDRECT.height - constants.LINE_WIDTH * (constants.ROWS + 1)) / constants.ROWS)
CELLOFF = (GRIDRECT.height % CELLSIZE) / 4