from asyncio import constants
import pygame
from Int2 import Int2
import time
import constants
import renderConstants
from Cell import Cells
start = time.process_time()
pygame.init()
display_surface = pygame.display.set_mode((renderConstants.SIZE, renderConstants.SIZE))
pygame.display.set_caption("Sus")
#######
day = pygame.transform.scale(pygame.image.load(r'Assets\\UI\\Backgrounds\\SunBackground.png'), (renderConstants.SIZE, renderConstants.SIZE))
noon = pygame.transform.scale(pygame.image.load(r'Assets\\UI\\Backgrounds\\SunDownBackground.png'), (renderConstants.SIZE, renderConstants.SIZE))
night = pygame.transform.scale(pygame.image.load(r'Assets\\UI\\Backgrounds\\MoonBackground.png'), (renderConstants.SIZE, renderConstants.SIZE))
dayProgressBarHeight = renderConstants.SIZE * 0.06
dayProgress = pygame.image.load(r'Assets\\UI\\DayProgressBar.png')
dayProgress = pygame.transform.scale(dayProgress, (dayProgress.get_width() / dayProgress.get_height() * dayProgressBarHeight, dayProgressBarHeight))
dayProgressPos = (renderConstants.SIZE * (1 - 0.13) - dayProgress.get_width(), renderConstants.SIZE * (1 - 0.005) - dayProgress.get_height())
dayProgressBorderSize = 0.13
dayProgressBorderSize = (dayProgressBorderSize * dayProgress.get_height() / dayProgress.get_width(), dayProgressBorderSize)
dayProgressRectWidth = 3
dayProgressRectBounds = dayProgressBorderSize[0] * dayProgress.get_width()
dayProgressRectBounds = (dayProgressPos[0] + dayProgressRectBounds + 1, dayProgressPos[0] + dayProgress.get_width() - dayProgressRectBounds - dayProgressRectWidth + 1)
dayProgressRect = pygame.Rect(dayProgressRectBounds[1], dayProgressPos[1] + dayProgress.get_height() * dayProgressBorderSize[1] + 0.5, dayProgressRectWidth, dayProgress.get_height() * (1 - dayProgressBorderSize[1] * 2) + 0.5)
#######
#######
turn = 0
mainLoop = True
while mainLoop:
    turn = int((time. process_time() - start))
    display_surface.fill((0, 0, 0))
    #######
    for x in range(constants.ROWS):
        cellX = int(renderConstants.GRIDRECT.left + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * x + renderConstants.CELLOFF)
        for y in range(constants.ROWS):
            cellY = int(renderConstants.GRIDRECT.top + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * y + renderConstants.CELLOFF)
            display_surface.blit(Cells.grass.value.image, (cellX, cellY))
    #######
    if(turn % renderConstants.CYCLELEN < renderConstants.CYCLELEN/2):
        if(turn % renderConstants.CYCLELEN > renderConstants.CYCLELEN/2 - 1 - renderConstants.NOONLENGTH):
            display_surface.blit(noon, (0, 0))
        else:
            display_surface.blit(day, (0, 0))
    else:
        display_surface.blit(night, (0, 0))
    #######
    display_surface.blit(dayProgress, dayProgressPos)
    ratio = (turn % (renderConstants.CYCLELEN)) / (renderConstants.CYCLELEN - 1)
    dayProgressRect.left = dayProgressRectBounds[0] * (1 - ratio) + dayProgressRectBounds[1] * ratio
    pygame.draw.rect(display_surface, (255, 255, 255), dayProgressRect)
    #######
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False
    pygame.display.update()