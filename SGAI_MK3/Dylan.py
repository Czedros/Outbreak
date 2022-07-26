import pygame
import ctypes
import time
import constants
import renderConstants
from Cell import Cells
from PIL import Image
from Animation import Animations
from Animation import Animation
def imageToGrid(path):
    im = Image.open(path, 'r').convert('RGB')
    pix = list(im.getdata())
    if(im.size[0] != constants.ROWS or im.size[1] != constants.ROWS):
        raise Exception("Image isn't correct size, must be a " + str(constants.ROWS) + " by " + str(constants.ROWS) + " pixel image")
    grid = []
    for i in range(constants.ROWS):
        grid.append([None] * constants.ROWS)
    for x in range(constants.ROWS):
        for y in range(constants.ROWS):
            print(str(x) + ", " + str(y))
            pixel = pix[x + y * constants.ROWS]
            match pixel:
                case (0, 255, 0):
                    grid[y][x] = Cells.grass
                    continue
                case (255, 255, 0):
                    grid[y][x] = Cells.sand
                    continue
                case (0, 0, 255):
                    grid[y][x] = Cells.water
                    continue
                case _:
                    grid[y][x] = Cells.nan
                    continue
    return grid
def cellPosition(x, y):
    cellX = int(renderConstants.GRIDRECT.left + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * x + renderConstants.CELLOFF)
    cellY = int(renderConstants.GRIDRECT.top + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * y + renderConstants.CELLOFF)
    return (cellX, cellY)
displayGrid = imageToGrid(r'Assets\\TestGrids\\TestGrid2.png')
start = renderConstants.frame_time
#######
pygame.init()
display_surface = pygame.display.set_mode((renderConstants.SIZE, renderConstants.SIZE))
ctypes.windll.user32.SetProcessDPIAware()#If you're not using Windows, here's an L -> L :).
pygame.display.set_caption("Sussy Baka") #Nice name - Hannah
resources = 0
ap = 0
turn = 0
human = [4, 2, Animation(Animations.human.value)]
zombies = [[3, 4, Animation(Animations.zombie.value)]]
mainLoop = True
while mainLoop:
    renderConstants.frame_time = time.process_time()
    turn = int((renderConstants.frame_time - start))
    ap = int((renderConstants.frame_time - start) % (constants.MAX_HUMAN_AP + 1))
    resources = min((renderConstants.frame_time - start) * 5, constants.MAX_RESOURCES)
    display_surface.fill((0, 0, 0))
    #######
    for x in range(constants.ROWS):
        cellX = int(renderConstants.GRIDRECT.left + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * x + renderConstants.CELLOFF)
        for y in range(constants.ROWS):
            cellY = int(renderConstants.GRIDRECT.top + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * y + renderConstants.CELLOFF)
            display_surface.blit(displayGrid[y][x].value.image, (cellX, cellY))
    #######
    human[2] = human[2].getNextAnimation()
    display_surface.blit(human[2].getImage(), cellPosition(human[0], human[1]))
    for i in zombies:
        i[2] = i[2].getNextAnimation()
        display_surface.blit(i[2].getImage(), cellPosition(i[0], i[1]))
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
    display_surface.blit(resourceBar, resourceBarPos)
    display_surface.blit(resourceIcon, (iconDist, iconDist - iconYOff))
    resourceBarRect.width = resourceRectBound * resources / constants.MAX_RESOURCES
    pygame.draw.rect(display_surface, (202, 0, 69), resourceBarRect)
    resourceText = resourceFont.render('Resources: ' + str(int(resources)) + "/" + str(constants.MAX_RESOURCES), True, (255, 255, 255))
    display_surface.blit(resourceText, resourceTextRect)
    #######
    display_surface.blit(apImage, apImagePos)
    apBarRect.width = apRectBound * ap / constants.MAX_HUMAN_AP
    pygame.draw.rect(display_surface, (239, 73, 52), apBarRect)
    apText = apFont.render('Action Points: ' + str(ap) + "/" + str(constants.MAX_HUMAN_AP), True, (255, 255, 255))
    display_surface.blit(apText, apTextRect)
    #######
    display_surface.blit(healImage, healImagePos)
    #######
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False
        elif event.type == pygame.MOUSEBUTTONUP:
            clickPos = pygame.mouse.get_pos()
            healClickPos = (clickPos[0] - healImagePos[0], clickPos[1] - healImagePos[1])
            if(healClickPos[0] >= 0 and healClickPos[0] <= healImage.get_width() and healClickPos[1] >= 0 and healClickPos[1] <= healImage.get_height()):
                print("Heal")
                continue
            if(clickPos[0] < renderConstants.GRIDRECT.left or clickPos[1] < renderConstants.GRIDRECT.top or clickPos[0] > renderConstants.GRIDRECT.right or clickPos[1] > renderConstants.GRIDRECT.bottom):
                continue
            clickOff = renderConstants.GRIDRECT.left + constants.LINE_WIDTH + renderConstants.CELLOFF
            clickPos = [clickPos[0], clickPos[1]]
            clickPos[0] -= clickOff
            clickPos[1] -= clickOff
            gridPos = (int(clickPos[0] / (constants.LINE_WIDTH + renderConstants.CELLSIZE)), int(clickPos[1] / (constants.LINE_WIDTH + renderConstants.CELLSIZE)))
            print("Clicked: " + str(gridPos))
    pygame.display.update()