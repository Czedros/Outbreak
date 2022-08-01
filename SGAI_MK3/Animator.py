from enum import Enum
import pygame
import renderConstants
from Int2 import Int2
import time
class AnimationType:
    def __init__(self, folder, images, length, nextAnimation = 0):
        if(nextAnimation == 0):
            self.nextAnimation = self
        else:
            self.nextAnimation = nextAnimation
        self.images = [None] * len(images)
        self.length = length
        for i in range(len(images)):
            self.images[i] = pygame.transform.scale(pygame.image.load(folder + "/" + images[i]), (renderConstants.CELLSIZE, renderConstants.CELLSIZE))
class Animation:
    def __init__(self, animType):
        self.animType = animType
        self.startTime = renderConstants.frame_time
        self.endTime = animType.length * len(animType.images) + self.startTime
    def getImage(self):
        t = (renderConstants.frame_time - self.startTime) / self.animType.length
        return self.animType.images[int(t)]
    def getNextAnimation(self):
        if(self.animType.nextAnimation != None and renderConstants.frame_time < self.endTime):
            return self
        else:
            return Animation(self.animType.nextAnimation)
humanFolder = r'Assets/Human Assets (Hannah Added)'
zombieFolder = r'Assets/Zombie Assets (Hannah Added)'
humanAnim = AnimationType(humanFolder, ["HumanNormal1.png", "HumanNormal2.png"], 1)
zombieAnim = AnimationType(zombieFolder, ["ZombieRoam1.png", "ZombieRoam2.png"], 1)
class Animations(Enum):
    human = humanAnim
    zombie = zombieAnim
    cure = AnimationType(humanFolder, ["HumanCure1.png", "HumanCure2.png"], 1, humanAnim)
    vaccinate = AnimationType(humanFolder, ["HumanVaccinate1.png", "HumanVaccinate2.png"], 1, humanAnim)
    seek = AnimationType(zombieFolder, ["ZombieSeek1.png", "ZombieSeek2.png"], 1)   
    bite = AnimationType(zombieFolder, ["ZombieBite1.png", "ZombieBite2.png"], 1)   
humanAnimation = Animation(Animations.human.value)