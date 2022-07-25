from asyncio import constants
import pygame
from Int2 import Int2
import time
import constants
start = time. process_time()
pygame.init()
size = Int2(700, 700)
display_surface = pygame.display.set_mode((size.x, size.y))
pygame.display.set_caption("Sus")

day = pygame.transform.scale(pygame.image.load(r'Assets\\UI\\Backgrounds\\SunBackground.png'), (size.x, size.y))
noon = pygame.transform.scale(pygame.image.load(r'Assets\\UI\\Backgrounds\\SunDownBackground.png'), (size.x, size.y))
night = pygame.transform.scale(pygame.image.load(r'Assets\\UI\\Backgrounds\\MoonBackground.png'), (size.x, size.y))
turn = 0
cycleLen = 10
noonLength = 2
mainLoop = True
while mainLoop:
    turn = int((time. process_time() - start))
    display_surface.fill(constants.WHITE)
    if(turn % cycleLen < cycleLen/2):
        if(turn % cycleLen > cycleLen/2 - 1 - noonLength):
            display_surface.blit(noon, (0, 0))
        else:
            display_surface.blit(day, (0, 0))
    else:
        display_surface.blit(night, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False
    pygame.display.update()