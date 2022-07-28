from enum import Enum
import pygame
import renderConstants
class CellType:
    def __init__(self, passable, imgPath):
        self.passable : bool = passable
        self.image = pygame.transform.scale(pygame.image.load(imgPath), (renderConstants.CELLSIZE, renderConstants.CELLSIZE))

class Cells(Enum):
    grass = CellType(True, r'Assets/Tiles/Grass.png')
    sand = CellType(True, r'Assets/Tiles/Sand.png')
    woodWall = CellType(False, r'Assets/Tiles/Wall.png')
    woodFloor = CellType(True, r'Assets/Tiles/Floor.png')
    water = CellType(False, r'Assets/Tiles/Water.png')
    nan = CellType(True, r'Assets/Tiles/nan.png')

    