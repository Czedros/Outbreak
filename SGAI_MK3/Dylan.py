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
dayProgressBarHeight = size.y * 0.06
dayProgress = pygame.image.load(r'Assets\\UI\\DayProgressBar.png')
dayProgress = pygame.transform.scale(dayProgress, (dayProgress.get_width() / dayProgress.get_height() * dayProgressBarHeight, dayProgressBarHeight))
dayProgressPos = (size.x * (1 - 0.13) - dayProgress.get_width(), size.y * (1 - 0.005) - dayProgress.get_height())
dayProgressBorderSize = 0.13
dayProgressBorderSize = (dayProgressBorderSize * dayProgress.get_height() / dayProgress.get_width(), dayProgressBorderSize)
dayProgressRectWidth = 3
dayProgressRectBounds = dayProgressBorderSize[0] * dayProgress.get_width()
dayProgressRectBounds = (dayProgressPos[0] + dayProgressRectBounds + 1, dayProgressPos[0] + dayProgress.get_width() - dayProgressRectBounds - dayProgressRectWidth + 1)
dayProgressRect = pygame.Rect(dayProgressRectBounds[1], dayProgressPos[1] + dayProgress.get_height() * dayProgressBorderSize[1] + 0.5, dayProgressRectWidth, dayProgress.get_height() * (1 - dayProgressBorderSize[1] * 2) + 0.5)
turn = 0
cycleLen = 10
noonLength = 2
mainLoop = True
while mainLoop:
    turn = int((time. process_time() - start))
    display_surface.fill(constants.WHITE)
    #######
    if(turn % cycleLen < cycleLen/2):
        if(turn % cycleLen > cycleLen/2 - 1 - noonLength):
            display_surface.blit(noon, (0, 0))
        else:
            display_surface.blit(day, (0, 0))
    else:
        display_surface.blit(night, (0, 0))
    #######
    display_surface.blit(dayProgress, dayProgressPos)
    ratio = (turn % (cycleLen)) / (cycleLen - 1)
    dayProgressRect.left = dayProgressRectBounds[0] * (1 - ratio) + dayProgressRectBounds[1] * ratio
    pygame.draw.rect(display_surface, (255, 255, 255), dayProgressRect)
    #######
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False
    pygame.display.update()