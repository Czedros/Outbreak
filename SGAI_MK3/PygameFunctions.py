from email.mime import audio
from glob import glob
from re import S
from typing import List, Tuple
import pygame
from constants import *
import constants
import renderConstants
import ctypes
import time
from Cell import Cells
from PIL import Image
from sys import platform
from enum import Enum
if(platform != "darwin"):
    from pyvidplayer import Video
from Animator import Animations
from Animator import Animation
from Obstacle import Obstacles
from pymediainfo import MediaInfo
from ffpyplayer.player import MediaPlayer
from Audio import Audio

    #Rumeysa 
    #might not use all these libraries
import csv  #writting to from datacollection1
import pandas as pd #reading from dataCollection1 and it also simplifies anaylizing data
import matplotlib.pyplot as plt #graphing the data - will use last



def imageToGrid(path, pathObstacles, States, mapOff = (0, 0)):
    im = Image.open(path, 'r').convert('RGB')
    imObstacle = Image.open(pathObstacles, 'r').convert('RGB')
    pix = list(im.getdata())
    pixObstacle = list(imObstacle.getdata())
    if(im.size[0] % constants.ROWS != 0 or im.size[1] % constants.ROWS != 0):
        raise Exception("Image isn't correct size, must be a " + str(constants.ROWS) + " by " + str(constants.ROWS) + " pixel image")
    if(imObstacle.size[0] % constants.ROWS != 0 or imObstacle.size[1] % constants.ROWS != 0):
        raise Exception("Obstacle image isn't correct size, must be a " + str(constants.ROWS) + " by " + str(constants.ROWS) + " pixel image")
    for x in range(constants.ROWS):
        for y in range(constants.ROWS):
            ind = x + mapOff[0] * constants.ROWS + (y + mapOff[1] * constants.ROWS) * im.size[0]
            pixel = pix[ind]
            pixelObstacle = pixObstacle[ind]
            match pixel:
                case (0, 255, 0):
                    States[y][x].cellType = Cells.grass.value
                case (255, 255, 0):
                    States[y][x].cellType = Cells.sand.value
                case (0, 0, 255):
                    States[y][x].cellType = Cells.water.value
                case (123, 60, 0):
                    States[y][x].cellType = Cells.woodWall.value
                case (211, 103, 0):
                    States[y][x].cellType = Cells.woodFloor.value
                case _:
                    States[y][x].cellType = Cells.nan.value
            if(pixelObstacle != pixel):
                match pixelObstacle:
                    case (157, 157, 157):
                        States[y][x].obstacle = Obstacles.rock.value
                    case (0, 135, 28):
                        States[y][x].obstacle = Obstacles.tree.value
                    case (255, 0, 0):
                        States[y][x].obstacle = Obstacles.resource.value
                    case _:
                        States[y][x].obstacle = Obstacles.nan.value

def cellPosition(x, y):
    cellX = int(renderConstants.GRIDRECT.left + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * x + renderConstants.CELLOFF)
    cellY = int(renderConstants.GRIDRECT.top + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * y + renderConstants.CELLOFF)
    return (cellX, cellY)
# Initialize pygame
pygame.init()
display_surface = pygame.display.set_mode((renderConstants.SIZE, renderConstants.SIZE))
if(platform != "darwin"):
    ctypes.windll.user32.SetProcessDPIAware()#If you're not using Windows, here's an L -> L :).
pygame.display.set_caption("Sussy Baka") #Nice name - Hannah

# Initialize variables
start = renderConstants.frame_time
#######
ambience = MediaPlayer(r"Assets/Audio/Ambience.wav", ff_opts = {"loop": 0})
audios = []#Garbage collector deletes audio without this
#######
day = pygame.transform.scale(pygame.image.load(r'Assets/UI/Backgrounds/SunBackground.png'), (renderConstants.SIZE, renderConstants.SIZE))
noon = pygame.transform.scale(pygame.image.load(r'Assets/UI/Backgrounds/SunDownBackground.png'), (renderConstants.SIZE, renderConstants.SIZE))
night = pygame.transform.scale(pygame.image.load(r'Assets/UI/Backgrounds/MoonBackground.png'), (renderConstants.SIZE, renderConstants.SIZE))
dayProgressBarHeight = renderConstants.SIZE * 0.06
dayProgress = pygame.image.load(r'Assets/UI/DayProgressBar.png')
dayProgress = pygame.transform.scale(dayProgress, (dayProgress.get_width() / dayProgress.get_height() * dayProgressBarHeight, dayProgressBarHeight))
dayProgressPos = (renderConstants.SIZE * (1 - 0.13) - dayProgress.get_width(), renderConstants.SIZE * (1 - 0.03) - dayProgress.get_height())
dayProgressBorderSize = 0.13
dayProgressBorderSize = (dayProgressBorderSize * dayProgress.get_height() / dayProgress.get_width(), dayProgressBorderSize)
dayProgressRectWidth = 3
dayProgressRectBounds = dayProgressBorderSize[0] * dayProgress.get_width()
dayProgressRectBounds = (dayProgressPos[0] + dayProgressRectBounds + 1, dayProgressPos[0] + dayProgress.get_width() - dayProgressRectBounds - dayProgressRectWidth + 1)
dayProgressRect = pygame.Rect(dayProgressRectBounds[1], dayProgressPos[1] + dayProgress.get_height() * dayProgressBorderSize[1] + 0.5, dayProgressRectWidth, dayProgress.get_height() * (1 - dayProgressBorderSize[1] * 2) + 0.5)
#######
resourceIcon = pygame.transform.scale(pygame.image.load(r'Assets/UI/ResourceIcon2.png'), (renderConstants.SIZE * 0.1, renderConstants.SIZE * 0.1))
resourceBarHeight = resourceIcon.get_height() * 0.5
resourceBar = pygame.image.load(r'Assets/UI/ResourceBar.png')
resourceBar = pygame.transform.scale(resourceBar, (resourceBarHeight * resourceBar.get_width() / resourceBar.get_height(), resourceBarHeight))
iconDist = renderConstants.SIZE * renderConstants.GRIDDIST - resourceIcon.get_height() * 0.75
iconYOff = renderConstants.SIZE * 0.01
resourceBarOff = renderConstants.SIZE * 0.015
resourceBarPos = (iconDist + resourceIcon.get_width() - resourceBarOff, iconDist + resourceIcon.get_height() * 0.75 - resourceBar.get_height() - iconYOff)
resourceBorderSize = 0.23
resourceRectBound = resourceBar.get_width() - resourceBar.get_height() * resourceBorderSize * 2 + 2
resourceBarRect = pygame.Rect(resourceBarPos[0] + resourceBar.get_height() * resourceBorderSize, resourceBarPos[1] + resourceBar.get_height() * resourceBorderSize, resourceRectBound, resourceBar.get_height() * (1 - resourceBorderSize * 2) + 2)
##
resourceFont = pygame.font.Font('freesansbold.ttf', int(renderConstants.SIZE / 40))
resourceText = resourceFont.render('Resources: sus', True, renderConstants.BARTEXTCOLOR)
resourceTextRect = resourceText.get_rect()
resourceTextRect.left = resourceBarPos[0] + renderConstants.SIZE * 0.02
resourceTextRect.top = resourceBarPos[1] - resourceTextRect.height
#######
savedFont = pygame.font.Font('freesansbold.ttf', int(renderConstants.SIZE / 40))
savedIcon = pygame.transform.scale(pygame.image.load(r'Assets/UI/SavedIcon.png'), (resourceIcon.get_width(), resourceIcon.get_height()))
savedCounterPos = (renderConstants.SIZE - resourceBarPos[0], resourceBarPos[1])
#######
apImageSize = 0.12
apImage = pygame.image.load(r'Assets/UI/APBar.png')
apImage = pygame.transform.scale(apImage, (renderConstants.SIZE * apImageSize * apImage.get_width() / apImage.get_height(), renderConstants.SIZE * apImageSize));
apImagePos = (renderConstants.SIZE * 0.01, renderConstants.SIZE - apImage.get_height())
apBorderSize = (0.35, 0.345)
apBarPos = (apImagePos[0] + apImage.get_width() * apBorderSize[0] - 1, apImagePos[1] + apImage.get_height() * apBorderSize[1] + 1)
apRectBound = apImage.get_width() * (1 - apBorderSize[0] - 0.033)
apBarRect = pygame.Rect(apBarPos[0], apBarPos[1], apRectBound, apImage.get_height() * (1 - apBorderSize[1] * 2) + 2)
apFont = pygame.font.Font('freesansbold.ttf', int(apImage.get_width() / 15))
apText = apFont.render('Action Points: sus', True, renderConstants.BARTEXTCOLOR)
apTextRect = apText.get_rect()
apTextRect.left = apBarRect.left + apImage.get_width() * 0.01
apTextRect.top  = apBarRect.top + (apBarRect.height - apTextRect.height) / 2
#######
healImageSize = 0.1 * renderConstants.SIZE
healImage = pygame.image.load(r'Assets/cure2.png')
healImage = pygame.transform.scale(healImage, (healImageSize, healImageSize * healImage.get_height() / healImage.get_width()))
healImageOpen = pygame.transform.scale(pygame.image.load(r'Assets/cure2Open.png'), (healImageSize, healImageSize * healImage.get_height() / healImage.get_width()))
healImagePos = (renderConstants.SIZE * (1 - renderConstants.GRIDDIST) + (renderConstants.GRIDDIST * renderConstants.SIZE - healImage.get_width()) / 2, renderConstants.SIZE * 0.1)
#######
healAreaImageSize = renderConstants.CELLSIZE * 3 + constants.LINE_WIDTH * 2
healAreaImage = pygame.transform.scale(pygame.image.load(r'Assets/HealArea.png'), (healAreaImageSize, healAreaImageSize))
#######
humanImage = pygame.transform.scale(pygame.image.load(r'Assets/Human Assets (Hannah Added)/HumanNormal1.png'), (renderConstants.CELLSIZE, renderConstants.CELLSIZE))
zombieImage = pygame.transform.scale(pygame.image.load(r'Assets/Zombie Assets (Hannah Added)/ZombieRoam1.png'), (renderConstants.CELLSIZE, renderConstants.CELLSIZE))
#######
resultFont = pygame.font.Font('freesansbold.ttf', int(renderConstants.SIZE / 40))
resultFont2 = pygame.font.Font('freesansbold.ttf', int(renderConstants.SIZE / 45))
#######
arrowImageSize = 0.04 * renderConstants.SIZE
arrowImageOff = (0.01 * renderConstants.SIZE, 0.09 * renderConstants.SIZE)
arrowImageForward = pygame.image.load(r'Assets/UI/arrowForward.png')
arrowImageForward = pygame.transform.scale(arrowImageForward, (arrowImageSize * arrowImageForward.get_width() / arrowImageForward.get_height(), arrowImageSize))
arrowImageBackward = pygame.transform.scale(pygame.image.load(r'Assets/UI/arrowBackward.png'), (arrowImageForward.get_width(), arrowImageForward.get_height()))
arrowImagePosY = renderConstants.SIZE - int(arrowImageForward.get_height()/2 + arrowImageOff[1])
##
finishImage = pygame.image.load(r'Assets/UI/FinishTurn.png')
finishSpace = arrowImageOff[1] - arrowImageForward.get_height()/2
finishImageOff = (0.1 * finishSpace)
finishImageHeight = finishSpace - 2 * finishImageOff
finishImage = pygame.transform.scale(finishImage, (finishImageHeight * finishImage.get_width() / finishImage.get_height(), finishImageHeight))
finishImagePos = (int(renderConstants.SIZE/2 - finishImage.get_width()/2), int(renderConstants.SIZE - finishImageOff - finishImage.get_height()))
#######
moveImageLeft = pygame.image.load(r'Assets/UI/MoveArrow.png')
moveImageMult = 7/5
moveImageLeft = pygame.transform.scale(moveImageLeft, (renderConstants.CELLSIZE * moveImageMult, (renderConstants.CELLSIZE * moveImageMult) * moveImageLeft.get_height() / moveImageLeft.get_width()))
moveImageRight = pygame.transform.flip(moveImageLeft, True, False)
moveImageUp = pygame.transform.rotate(moveImageRight, 90)
moveImageDown = pygame.transform.flip(moveImageUp, False, True)
##
healTurnImage = pygame.image.load(r'Assets/UI/cure2Transparent.png')
healImageMult = 0.8
healTurnImage = pygame.transform.scale(healTurnImage, (renderConstants.CELLSIZE * healImageMult * healTurnImage.get_width() / healTurnImage.get_height(), renderConstants.CELLSIZE * healImageMult))
##
moveLockImage = pygame.image.load(r'Assets/UI/moveLock.png')
moveLockImageHeight = renderConstants.CELLSIZE * 0.6
moveLockImage = pygame.transform.scale(moveLockImage, (moveLockImageHeight * healTurnImage.get_width() / healTurnImage.get_height(), moveLockImageHeight))
#######
mapImageSize = renderConstants.SIZE * 0.08
mapImageOff = ((renderConstants.GRIDDIST * renderConstants.SIZE - mapImageSize) / 2, renderConstants.SIZE * 0.03)
mapImage = pygame.transform.scale(pygame.image.load(r'Assets/UI/Compass.png'), (mapImageSize, mapImageSize))
mapImagePos = (renderConstants.SIZE - mapImage.get_width() - mapImageOff[0], healImagePos[1] + healImage.get_height() + mapImageOff[1])
#######
healing = False
#######
timeCounterSize = renderConstants.SIZE * 0.075
timeCounterPos = (renderConstants.SIZE * 0.983 - timeCounterSize, renderConstants.SIZE * 0.97 - timeCounterSize)
timeCounts = []
for i in range(9):
    path = r'Assets/UI/Time/' + str(int(i / 2 + 1))
    if(i % 2 == 0):
        path = path + "D"
    else:
        path = path + "N"
    timeCounts.append(pygame.transform.scale(pygame.image.load(path + ".png"), (timeCounterSize, timeCounterSize)))
#######
#GameBoard.isValidCoordinate(new_coords)
#self.States[new_coords[1]][new_coords[0]].person is None and self.States[new_coords[1]][new_coords[0]].cellType.passable
class ActionType:
    def __init__(self, ap):
        self.ap = ap
class Action:
    def __init__(self, actionType, coord, coord2 = None):
        self.actionType = actionType
        self.coord = coord
        if(coord2 == None):
            self.coord2 = coord
        else:
            self.coord2 = coord2
class ActionTypes(Enum):
    move = ActionType(1)
    heal = ActionType(2)

actions = []
actionSlot = -1
actionsAPCost = 0
actionsAPCostShow = 0
firstActor = None
selectedActor = None
def reset_actions():
    global actions
    global actionsAPCost
    global actionsAPCostShow
    global actionSlot
    global selectedActor
    global firstActor
    actions = []
    actionsAPCost = 0
    actionsAPCostShow = 0
    actionSlot = -1
    selectedActor = None
    firstActor = None
def init_selectedActor(GameBoard):
    global selectedActor
    global firstActor
    if(selectedActor == None):
        for arr in GameBoard.States:
            finished = False
            for state in arr:
                if(state.person != None and state.person.isZombie == False):
                    selectedActor = state.location
                    firstActor = selectedActor
                    return
def add_action(GameBoard, action):
    global actionSlot
    global actionsAPCost
    global selectedActor
    global actionsAPCostShow
    if(GameBoard.resources[0].currentValue - actionsAPCostShow < action.actionType.ap):
        return False
    for i in range(actionSlot + 1):
        act = actions[i]
        if(act.actionType == action.actionType and act.coord2 == action.coord2):
            return False
    while(len(actions) > actionSlot + 1):
        act = actions.pop()
        actionsAPCost -= act.actionType.ap
    actions.append(action)
    actionSlot += 1
    actionsAPCost += action.actionType.ap
    actionsAPCostShow = actionsAPCost
    return True
def get_action(GameBoard, pixel_x: int, pixel_y: int):
    global healing
    global selectedActor
    global firstActor
    global actionSlot
    global actionsAPCostShow
    """
    Get the action that the click represents.
    If the click was on the heal button, returns "heal"
    Else, returns the board coordinates of the click (board_x, board_y) if valid
    Return None otherwise
    """
    init_selectedActor(GameBoard)
    clickPos = [pixel_x, pixel_y]
    healClickPos = (clickPos[0] - healImagePos[0], clickPos[1] - healImagePos[1])
    finishClickPos = (clickPos[0] - finishImagePos[0], clickPos[1] - finishImagePos[1])
    arrowClickPos = (clickPos[0] - (int(renderConstants.SIZE/2) - arrowImageForward.get_width() - arrowImageOff[0]), clickPos[1] - arrowImagePosY)
    arrowClickSize = (int((arrowImageForward.get_width() + arrowImageOff[0]) * 2), int(arrowImageSize))
    if(healClickPos[0] >= 0 and healClickPos[0] <= healImage.get_width() and healClickPos[1] >= 0 and healClickPos[1] <= healImage.get_height()):
        healing = not healing
        if(healing):
            audios.append(Audio(r"Assets/Audio/Cure.wav"))
        return "heal"
    if(finishClickPos[0] >= 0 and finishClickPos[0] <= finishImage.get_width() and finishClickPos[1] >= 0 and finishClickPos[1] <= finishImage.get_height()):
        return "finish"
    if(arrowClickPos[0] >= 0 and arrowClickPos[0] <= arrowClickSize[0] and arrowClickPos[1] >= 0 and arrowClickPos[1] <= arrowClickSize[1]):
        if(arrowClickPos[0] <= arrowClickSize[0]/2):
            if(actionSlot != -1):
                actionSlot -= 1
                actionsAPCostShow -= actions[actionSlot + 1].actionType.ap
                if(actions[actionSlot + 1].actionType == ActionTypes.move.value):
                    selectedActor = actions[actionSlot + 1].coord
        else:
            if(actionSlot != len(actions) - 1):
                actionSlot += 1
                actionsAPCostShow += actions[actionSlot].actionType.ap
                if(actions[actionSlot].actionType == ActionTypes.move.value):
                    selectedActor = actions[actionSlot].coord2

        return None
    mapClickPos = (clickPos[0] - mapImagePos[0], clickPos[1] - mapImagePos[1])
    if(mapClickPos[0] >= 0 and mapClickPos[0] <= mapImageSize and mapClickPos[1] >= 0 and mapClickPos[1] <= mapImageSize):
        if(GameBoard.resources[0].currentValue == 8):
            audios.append(Audio(r"Assets/Audio/Page Flip.wav"))
            return GameBoard.newBoard()
        else:
            audios.append(Audio(r"Assets/Audio/NotAllowed.wav"))
            return None
    clickOff = renderConstants.GRIDRECT.left + constants.LINE_WIDTH + renderConstants.CELLOFF
    clickPos[0] -= clickOff
    clickPos[1] -= clickOff
    gridPos = (int(clickPos[0] / (constants.LINE_WIDTH + renderConstants.CELLSIZE)), int(clickPos[1] / (constants.LINE_WIDTH + renderConstants.CELLSIZE)))
    if(gridPos[0] < 0 or gridPos[1] < 0 or gridPos[0] >= constants.COLUMNS or gridPos[1] >= constants.ROWS):
        return None
    state = GameBoard.States[gridPos[1]][gridPos[0]]
    canAct = (actionSlot == -1 or actions[actionSlot].actionType != ActionTypes.heal.value)
    if(healing and state.person is not None):
        if(canAct and ((abs(gridPos[0] - selectedActor[0]) <= 1 and abs(gridPos[1] - selectedActor[1]) <= 1) or (gridPos[0] == firstActor[0] and gridPos[1] == firstActor[1]))):
            if(not add_action(GameBoard, Action(ActionTypes.heal.value, gridPos))):
                audios.append(Audio(r"Assets/Audio/NotAllowed.wav"))
        else:
            audios.append(Audio(r"Assets/Audio/NotAllowed.wav"))
    elif(state.person == None):
        if(canAct and state.passable()):
            path = GameBoard.findPath(selectedActor, gridPos)
            if(path != None):
                worked = False
                for i in path:
                    if(add_action(GameBoard, Action(ActionTypes.move.value, selectedActor, i))):
                        worked = True
                        selectedActor = i
                    else:
                        break
                if(worked):
                    audios.append(Audio(r"Assets/Audio/Walksount.mp3"))
                else:
                    audios.append(Audio(r"Assets/Audio/NotAllowed.wav"))
        else:
            audios.append(Audio(r"Assets/Audio/NotAllowed.wav"))
    elif(state.person.isZombie == False):
        reset_actions()
        selectedActor = gridPos
        firstActor = gridPos
    healing = False
    return gridPos[0], gridPos[1]
    #reset_move_check = (
    #    pixel_x >= RESET_MOVE_COORDS[0]
    #    and pixel_x <= RESET_MOVE_COORDS[0] + RESET_MOVE_DIMS[0]
    #    and pixel_y >= RESET_MOVE_COORDS[1]
    #    and pixel_y <= RESET_MOVE_COORDS[1] + RESET_MOVE_DIMS[1]
    #)
    #return "reset move"
def cellCoord(coord):
        cellX = int(renderConstants.GRIDRECT.left + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * coord[0] + renderConstants.CELLOFF)
        cellY = int(renderConstants.GRIDRECT.top + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * coord[1] + renderConstants.CELLOFF)
        return (cellX, cellY)
def run(GameBoard):
    renderConstants.frame_time = time.process_time()
    for i in range(len(audios) - 1, -1, -1):
        aud = audios[i]
        if(renderConstants.frame_time >= aud.endTime):
            aud.audio.toggle_pause()
            audios.pop(i)
    turn = GameBoard.timeCounter
    ap = GameBoard.resources[0].currentValue
    resources = min(GameBoard.resources[1].currentValue, GameBoard.resources[1].maxValue)
    display_surface.fill((0, 0, 0))
    #######
    for x in range(constants.ROWS):
        cellX = int(renderConstants.GRIDRECT.left + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * x + renderConstants.CELLOFF)
        for y in range(constants.ROWS):
            cellY = int(renderConstants.GRIDRECT.top + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * y + renderConstants.CELLOFF)
            display_surface.blit(GameBoard.States[y][x].cellType.image, (cellX, cellY))
            if(GameBoard.States[y][x].obstacle != None):
                display_surface.blit(GameBoard.States[y][x].obstacle.image, (cellX, cellY))   
    #######
    for i in range(actionSlot, -1, -1):
        act = actions[i]
        if(act.actionType == ActionTypes.move.value):
            pos1 = cellCoord(act.coord)
            pos2 = cellCoord(act.coord2)
            posT = [(pos1[0] + pos2[0] + renderConstants.CELLSIZE) / 2, (pos1[1] + pos2[1] + renderConstants.CELLSIZE) / 2]
            img = None
            if(pos2[0] > pos1[0]):
                img = moveImageRight
            elif(pos2[0] < pos1[0]):
                img = moveImageLeft
            elif(pos2[1] < pos1[1]):
                img = moveImageUp
            elif(pos2[1] > pos1[1]):
                img = moveImageDown
            display_surface.blit(img, (posT[0] - img.get_width()/2, posT[1] - img.get_height()/2))
    #######
    for y in range(len(GameBoard.States)):
        arr = GameBoard.States[y]
        for x in range(len(arr)):
            state = GameBoard.States[y][x]
            if state.person != None:
                state.person.animation = state.person.animation.getNextAnimation()
                display_surface.blit(state.person.animation.getImage(), cellPosition(x, y))
    #######
    canAct = ((actionSlot == -1 or actions[actionSlot].actionType != ActionTypes.heal.value) and (ap - actionsAPCostShow) != 0)
    if(selectedActor != None and not canAct):
        cellPos = cellPosition(selectedActor[0], selectedActor[1])
        display_surface.blit(moveLockImage, [cellPos[0] + (renderConstants.CELLSIZE - moveLockImage.get_width()) / 2, cellPos[1] + (renderConstants.CELLSIZE - moveLockImage.get_height()) / 2]) 
    #######
    if(selectedActor != None and healing):
        cellPos = cellPosition(selectedActor[0], selectedActor[1])
        display_surface.blit(healAreaImage, (cellPos[0] - renderConstants.CELLSIZE - constants.LINE_WIDTH, cellPos[1] - renderConstants.CELLSIZE - constants.LINE_WIDTH))
    #######
    for i in range(actionSlot + 1):
        act = actions[i]
        if(act.actionType == ActionTypes.heal.value):
            pos = cellCoord(act.coord)
            display_surface.blit(healTurnImage, (pos[0] + (renderConstants.CELLSIZE - healTurnImage.get_width())/2, pos[1] + (renderConstants.CELLSIZE - healTurnImage.get_height())/2))
            a=1
    #######
    if(GameBoard.isDay):
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
    resourceDrain = min((1+(GameBoard.resources[2].currentValue)), resources)
    resourceDrainWidth = resourceRectBound * resourceDrain / GameBoard.resources[1].maxValue
    display_surface.blit(resourceBar, resourceBarPos)
    display_surface.blit(resourceIcon, (iconDist, iconDist - iconYOff))
    resourceBarRect.width = resourceRectBound * resources / GameBoard.resources[1].maxValue
    pygame.draw.rect(display_surface, (202, 0, 69), resourceBarRect)
    pygame.draw.rect(display_surface, (121, 0, 41), pygame.Rect(resourceBarRect.width + resourceBarRect.left - resourceDrainWidth, resourceBarRect.top, resourceDrainWidth, resourceBarRect.height))
    resourceText = resourceFont.render('Resources: ' + str(int(resources)) + "/" + str(GameBoard.resources[1].maxValue), True, renderConstants.BARTEXTCOLOR)
    display_surface.blit(resourceText, resourceTextRect)
    #######
    savedCounter = savedFont.render('People Saved: ' + str(GameBoard.resources[2].currentValue), True, renderConstants.BARTEXTCOLOR)#placeholder
    display_surface.blit(savedIcon, (renderConstants.SIZE - iconDist - savedIcon.get_width(), iconDist - iconYOff))
    display_surface.blit(savedCounter, (renderConstants.SIZE - resourceTextRect[0] - savedCounter.get_width(), resourceBarPos[1]))#(resourceTextRect[0], resourceTextRect[1] - savedCounter.get_width())
    #######
    display_surface.blit(apImage, apImagePos)
    apBarRect.width = apRectBound * ap / GameBoard.resources[0].maxValue
    pygame.draw.rect(display_surface, (239, 73, 52), apBarRect)
    apUsedWidth = apRectBound * actionsAPCostShow / GameBoard.resources[0].maxValue
    apBarRectUsed = pygame.Rect(apBarRect.left + apBarRect.width - apUsedWidth, apBarRect.top, apUsedWidth, apBarRect.height)
    pygame.draw.rect(display_surface, (244, 144, 83), apBarRectUsed)
    apText = apFont.render('Action Points: ' + str(ap - actionsAPCostShow) + "/" + str(GameBoard.resources[0].maxValue), True, renderConstants.APTEXTCOLOR)
    display_surface.blit(apText, apTextRect)
    #######
    if(actionSlot + 1 != len(actions)):
        display_surface.blit(arrowImageForward, (int(renderConstants.SIZE/2) + arrowImageOff[0], arrowImagePosY))
    if(actionSlot != -1):
        display_surface.blit(arrowImageBackward, (int(renderConstants.SIZE/2) - arrowImageForward.get_width() - arrowImageOff[0], arrowImagePosY))
    ##
    display_surface.blit(finishImage, finishImagePos)
    #######
    if(healing):
        display_surface.blit(healImageOpen, healImagePos)
    else:
        display_surface.blit(healImage, healImagePos)
    #######
    display_surface.blit(mapImage, mapImagePos)
    #######
    timeCountInd = int(GameBoard.timeCounter / renderConstants.CYCLELEN) * 2
    if(not GameBoard.isDay):
        timeCountInd += 1
    display_surface.blit(timeCounts[timeCountInd], timeCounterPos)
    pygame.display.update()
    return pygame.event.get()


def display_reset_move_button():
    #rect = pygame.Rect(
    #    RESET_MOVE_COORDS[0],
    #    RESET_MOVE_COORDS[1],
    #    RESET_MOVE_DIMS[0],
    #    RESET_MOVE_DIMS[1],
    #)
    #pygame.draw.rect(screen, BLACK, rect)
    #screen.blit(font.render("Reset move?", True, WHITE), RESET_MOVE_COORDS)
    a=1


resultImageSize = renderConstants.SIZE * 0.4
winImages = [None] * 2
loseImages = [None] * 2
for i in range(1, 3):
    strW = r'Assets/Human Assets (Hannah Added)/HumanWin' + str(i) + ".png"
    strL = r'Assets/Human Assets (Hannah Added)/HumanLose' + str(i) + ".png"
    imgW = pygame.image.load(strW)
    imgL = pygame.image.load(strL)
    winImages[i - 1] = pygame.transform.scale(imgW, (resultImageSize * imgW.get_width() / imgW.get_height(), resultImageSize))
    loseImages[i - 1] = pygame.transform.scale(imgL, (resultImageSize * imgL.get_width() / imgL.get_height(), resultImageSize))
#######
textW = resultFont.render("You win!", True, renderConstants.RESULTTEXTCOLOR)
textW1 = resultFont2.render("You cured everyone!", True, renderConstants.RESULTTEXTCOLOR)
textW2 = resultFont2.render("You survived till the 5th day!", True, renderConstants.RESULTTEXTCOLOR)
textL = resultFont.render("You lose... Noob", True, renderConstants.RESULTTEXTCOLOR)
textL1 = resultFont2.render("Remember to collect resources", True, renderConstants.RESULTTEXTCOLOR)
textL2 = resultFont2.render("Zombie bad", True, renderConstants.RESULTTEXTCOLOR)
#######
def displayResultScreen(won, reason = 1):
    global audios
    for i in audios:
        i.toggle_pause()
    audios = []
    ambience.toggle_pause()
    def movie():
        res = None
        if(won):
            res = Video(r'Assets/UI/LRatio2.mp4')
            res.set_volume(0.1)
        else:
            res = Video(r'Assets/UI/Sadge.mp4')
            res.set_volume(0.9)
        return res
    if(platform != "darwin"):
        resMovie = movie()
        videoDuration = resMovie.video.get_metadata()["duration"]
        ogSize = resMovie.get_file_data()["original size"]
        resMovieSize = (renderConstants.SIZE * 0.25 * ogSize[0] / ogSize[1], renderConstants.SIZE * 0.25)
        resMovie.set_size(resMovieSize) 
        resMovieSpeed = [100, 130]
        resMoviePos = [0, 0]
    deltaTime = 0
    startTime1 = time.process_time()
    while True:
        startTime = time.process_time()
        display_surface.fill(BACKGROUND)
        #######
        if(platform != "darwin"):
            if(resMovieSize[1] + int(resMoviePos[1]) >= renderConstants.SIZE):
                resMovieSpeed[1] = -abs(resMovieSpeed[1])
            elif(int(resMoviePos[1]) <= 0):
                resMovieSpeed[1] = abs(resMovieSpeed[1])
            if(resMovieSize[0] + int(resMoviePos[0]) >= renderConstants.SIZE):
                resMovieSpeed[0] = -abs(resMovieSpeed[0])
            elif(int(resMoviePos[0]) <= 0):
                resMovieSpeed[0] = abs(resMovieSpeed[0])
            resMoviePos[0] += resMovieSpeed[0] * deltaTime
            resMoviePos[1] += resMovieSpeed[1] * deltaTime
            resMovie.draw(display_surface, (int(resMoviePos[0]), resMoviePos[1]))
        #######
        if(won):
            text = textW
            if(reason == 1):
                text2 = textW1
            else:
                text2 = textW2
            images = winImages
        else:
            text = textL
            if(reason == 1):
                text2 = textL1
            else:
                text2 = textL2
            images = loseImages
        img = images[int(startTime) % 2]
        #######
        textPos = (renderConstants.SIZE * 0.5, renderConstants.SIZE * 0.1)
        textPos2 = (textPos[0], textPos[1] + renderConstants.SIZE * 0)
        imgPos = renderConstants.SIZE * 0.01
        #######
        display_surface.blit(text, (textPos[0] - text.get_width() / 2, textPos[1]))
        display_surface.blit(img, (textPos[0] - img.get_width() / 2, textPos2[1] + text2.get_height() / 2 + text.get_height() + imgPos))
        display_surface.blit(text2, (textPos2[0] - text2.get_width() / 2, textPos2[1] + text2.get_height() / 2 + text.get_height() + img.get_height() + imgPos))
        #######

        pygame.display.update()
        endTime = time.process_time()
        deltaTime = endTime - startTime
        if(platform != "darwin" and endTime - startTime1 >= videoDuration - 1):
            resMovie.close()
            startTime1 = time.process_time()
            resMovie = movie()
            resMovie.set_size(resMovieSize) 

        # catch quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                resMovie.close()
                return
        

def direction(coord1: Tuple[int, int], coord2: Tuple[int, int]):
    if coord2[1] > coord1[1]:
        return "moveDown"
    elif coord2[1] < coord1[1]:
        return "moveUp"
    elif coord2[0] > coord1[0]:
        return "moveRight"
    elif coord2[0] < coord1[0]:
        return "moveLeft"

    #rumeysa:
def dataWrite(path: str, toWrite: Tuple):
    f = open(path, "a", newline="")
    csv.writer(f).writerow(toWrite)
    f.close()

    #reads the data from data collection1: 
dataFrame1 = pd.read_csv("dataCollectionAI1.csv")
    #make a dataFrame2 if nessecary
dataFrame2 = pd.read_csv("dataCollectionAI2.csv")
