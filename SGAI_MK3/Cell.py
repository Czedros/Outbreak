from enum import Enum
import pygame
import renderConstants
class CellType:
    def __init__(self, passable, imgPath):
        self.passable = passable
        self.image = pygame.transform.scale(pygame.image.load(imgPath), (renderConstants.CELLSIZE, renderConstants.CELLSIZE))

class Cells(Enum):
    grass = CellType(True, r'Assets\\Tiles\\Grass.png')
    sand = 1
    wood = 2

    