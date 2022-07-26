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
displayGrid = imageToGrid(r'Assets\\TestGrids\\TestGrid1.png')
start = renderConstants.frame_time
#######
pygame.init()
display_surface = pygame.display.set_mode((renderConstants.SIZE, renderConstants.SIZE))
ctypes.windll.user32.SetProcessDPIAware()#If you're not using Windows, here's an L -> L :).
pygame.display.set_caption("Sussy Baka") #Nice name - Hannah
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
resourceIcon = pygame.transform.scale(pygame.image.load(r'Assets\\UI\\ResourceIcon2.png'), (renderConstants.SIZE * 0.1, renderConstants.SIZE * 0.1))
resourceBarHeight = resourceIcon.get_height() * 0.5
resourceBar = pygame.image.load(r'Assets\\UI\\ResourceBar.png')
resourceBar = pygame.transform.scale(resourceBar, (resourceBarHeight * resourceBar.get_width() / resourceBar.get_height(), resourceBarHeight))
iconDist = renderConstants.SIZE * renderConstants.GRIDDIST - resourceIcon.get_height() * 0.75
iconYOff = renderConstants.SIZE * 0.01
resourceBarPos = (iconDist + resourceIcon.get_width() - renderConstants.SIZE * 0.015, iconDist + resourceIcon.get_height() * 0.75 - resourceBar.get_height() - iconYOff)
resourceBorderSize = 0.23
resourceRectBound = resourceBar.get_width() - resourceBar.get_height() * resourceBorderSize * 2 + 2
resourceBarRect = pygame.Rect(resourceBarPos[0] + resourceBar.get_height() * resourceBorderSize, resourceBarPos[1] + resourceBar.get_height() * resourceBorderSize, resourceRectBound, resourceBar.get_height() * (1 - resourceBorderSize * 2) + 2)
##
resourceFont = pygame.font.Font('freesansbold.ttf', int(renderConstants.SIZE / 40))
resourceText = resourceFont.render('Resources: sus', True, (255, 255, 255))
resourceTextRect = resourceText.get_rect()
resourceTextRect.left = resourceBarPos[0] + renderConstants.SIZE * 0.02
resourceTextRect.top = resourceBarPos[1] - resourceTextRect.height
#######
apImageSize = 0.12
apImage = pygame.image.load(r'Assets\\UI\\testap.png')
apImage = pygame.transform.scale(apImage, (renderConstants.SIZE * apImageSize * apImage.get_width() / apImage.get_height(), renderConstants.SIZE * apImageSize));
apImagePos = (renderConstants.SIZE * 0.05, renderConstants.SIZE - apImage.get_height())
apBorderSize = (0.35, 0.345)
apBarPos = (apImagePos[0] + apImage.get_width() * apBorderSize[0] - 1, apImagePos[1] + apImage.get_height() * apBorderSize[1] + 1)
apRectBound = apImage.get_width() * (1 - apBorderSize[0] - 0.033)
apBarRect = pygame.Rect(apBarPos[0], apBarPos[1], apRectBound, apImage.get_height() * (1 - apBorderSize[1] * 2) + 2)
apFont = pygame.font.Font('freesansbold.ttf', int(apImage.get_width() / 15))
apText = apFont.render('Action Points: sus', True, (255, 255, 255))
apTextRect = apText.get_rect()
apTextRect.left = apBarRect.left + apImage.get_width() * 0.01
apTextRect.top  = apBarRect.top + (apBarRect.height - apTextRect.height) / 2
#######
healImageSize = 0.1 * renderConstants.SIZE
healImage = pygame.image.load(r'Assets\\cure2.png')
healImage = pygame.transform.scale(healImage, (healImageSize, healImageSize * healImage.get_height() / healImage.get_width()))
healImagePos = (renderConstants.SIZE * (1 - renderConstants.GRIDDIST) + (renderConstants.GRIDDIST * renderConstants.SIZE - healImage.get_width()) / 2, renderConstants.SIZE * 0.1)
#######
humanImage = pygame.transform.scale(pygame.image.load(r'Assets\\Human Assets (Hannah Added)\\HumanNormal1.png'), (renderConstants.CELLSIZE, renderConstants.CELLSIZE))
zombieImage = pygame.transform.scale(pygame.image.load(r'Assets\\Zombie Assets (Hannah Added)\\ZombieRoam1.png'), (renderConstants.CELLSIZE, renderConstants.CELLSIZE))
#######
resources = 0
ap = 0
turn = 0
human = [4, 2, Animation(Animations.human.value)]
zombies = [[12, 3, Animation(Animations.zombie.value)], [7, 11, Animation(Animations.zombie.value)], [3, 6, Animation(Animations.zombie.value   )]]
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