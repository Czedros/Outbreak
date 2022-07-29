import pygame
import renderConstants
from enum import Enum
class Obstacle:
    def __init__(self, imagePath, passable):
        self.image = pygame.transform.scale(pygame.image.load(imagePath), (renderConstants.CELLSIZE, renderConstants.CELLSIZE))
        self.passable = passable

class Obstacles(Enum):
    resource = Obstacle(r"Assets/Tiles/ResourceTile.png", True)
    rock = Obstacle(r"Assets/Tiles/Boulder.png", False)
    tree = Obstacle(r"Assets/Tiles/Cactus.png", False)
    nan = Obstacle(r"Assets/Tiles/nanObstacle.png", False)