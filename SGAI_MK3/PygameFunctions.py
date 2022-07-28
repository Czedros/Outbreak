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
from pyvidplayer import Video
from Animator import Animations
from Animator import Animation
import Animator


def imageToGrid(path, States):
    im = Image.open(path, 'r').convert('RGB')
    pix = list(im.getdata())
    if(im.size[0] != constants.ROWS or im.size[1] != constants.ROWS):
        raise Exception("Image isn't correct size, must be a " + str(constants.ROWS) + " by " + str(constants.ROWS) + " pixel image")
    for x in range(constants.ROWS):
        for y in range(constants.ROWS):
            pixel = pix[x + y * constants.ROWS]
            match pixel:
                case (0, 255, 0):
                    States[y][x].cellType = Cells.grass.value
                    continue
                case (255, 255, 0):
                    States[y][x].cellType = Cells.sand.value
                    continue
                case (0, 0, 255):
                    States[y][x].cellType = Cells.water.value
                    continue
                case (123, 60, 0):
                    States[y][x].cellType = Cells.woodWall.value
                    continue
                case (211, 103, 0):
                    States[y][x].cellType = Cells.woodFloor.value
                    continue
                case _:
                    States[y][x].cellType = Cells.nan.value
                    continue
def cellPosition(x, y):
    cellX = int(renderConstants.GRIDRECT.left + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * x + renderConstants.CELLOFF)
    cellY = int(renderConstants.GRIDRECT.top + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * y + renderConstants.CELLOFF)
    return (cellX, cellY)
# Initialize pygame
pygame.init()
display_surface = pygame.display.set_mode((renderConstants.SIZE, renderConstants.SIZE))
ctypes.windll.user32.SetProcessDPIAware()#If you're not using Windows, here's an L -> L :).
pygame.display.set_caption("Sussy Baka") #Nice name - Hannah

# Initialize variables
start = renderConstants.frame_time

#######
day = pygame.transform.scale(pygame.image.load(r'Assets/UI/Backgrounds/SunBackground.png'), (renderConstants.SIZE, renderConstants.SIZE))
noon = pygame.transform.scale(pygame.image.load(r'Assets/UI/Backgrounds/SunDownBackground.png'), (renderConstants.SIZE, renderConstants.SIZE))
night = pygame.transform.scale(pygame.image.load(r'Assets/UI/Backgrounds/MoonBackground.png'), (renderConstants.SIZE, renderConstants.SIZE))
dayProgressBarHeight = renderConstants.SIZE * 0.06
dayProgress = pygame.image.load(r'Assets/UI/DayProgressBar.png')
dayProgress = pygame.transform.scale(dayProgress, (dayProgress.get_width() / dayProgress.get_height() * dayProgressBarHeight, dayProgressBarHeight))
dayProgressPos = (renderConstants.SIZE * (1 - 0.13) - dayProgress.get_width(), renderConstants.SIZE * (1 - 0.005) - dayProgress.get_height())
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
apImage = pygame.image.load(r'Assets/UI/APBar.png')
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
healImage = pygame.image.load(r'Assets/cure2.png')
healImage = pygame.transform.scale(healImage, (healImageSize, healImageSize * healImage.get_height() / healImage.get_width()))
healImageOpen = pygame.transform.scale(pygame.image.load(r'Assets/cure2Open.png'), (healImageSize, healImageSize * healImage.get_height() / healImage.get_width()))
healImagePos = (renderConstants.SIZE * (1 - renderConstants.GRIDDIST) + (renderConstants.GRIDDIST * renderConstants.SIZE - healImage.get_width()) / 2, renderConstants.SIZE * 0.1)
#######
humanImage = pygame.transform.scale(pygame.image.load(r'Assets/Human Assets (Hannah Added)/HumanNormal1.png'), (renderConstants.CELLSIZE, renderConstants.CELLSIZE))
zombieImage = pygame.transform.scale(pygame.image.load(r'Assets/Zombie Assets (Hannah Added)/ZombieRoam1.png'), (renderConstants.CELLSIZE, renderConstants.CELLSIZE))
#######
resultFont = pygame.font.Font('freesansbold.ttf', int(renderConstants.SIZE / 40))
resultFont2 = pygame.font.Font('freesansbold.ttf', int(renderConstants.SIZE / 45))
#######
healing = False
#######
def get_action(GameBoard, pixel_x: int, pixel_y: int):
    global healing
    """
    Get the action that the click represents.
    If the click was on the heal button, returns "heal"
    Else, returns the board coordinates of the click (board_x, board_y) if valid
    Return None otherwise
    """
    clickPos = [pixel_x, pixel_y]
    healClickPos = (clickPos[0] - healImagePos[0], clickPos[1] - healImagePos[1])
    if(healClickPos[0] >= 0 and healClickPos[0] <= healImage.get_width() and healClickPos[1] >= 0 and healClickPos[1] <= healImage.get_height()):
        healing = not healing
        return "heal"
    healing = False
    if(clickPos[0] < renderConstants.GRIDRECT.left or clickPos[1] < renderConstants.GRIDRECT.top or clickPos[0] > renderConstants.GRIDRECT.right or clickPos[1] > renderConstants.GRIDRECT.bottom):
        return None
    clickOff = renderConstants.GRIDRECT.left + constants.LINE_WIDTH + renderConstants.CELLOFF
    clickPos[0] -= clickOff
    clickPos[1] -= clickOff
    gridPos = (int(clickPos[0] / (constants.LINE_WIDTH + renderConstants.CELLSIZE)), int(clickPos[1] / (constants.LINE_WIDTH + renderConstants.CELLSIZE)))
    return gridPos[0], gridPos[1]
    #reset_move_check = (
    #    pixel_x >= RESET_MOVE_COORDS[0]
    #    and pixel_x <= RESET_MOVE_COORDS[0] + RESET_MOVE_DIMS[0]
    #    and pixel_y >= RESET_MOVE_COORDS[1]
    #    and pixel_y <= RESET_MOVE_COORDS[1] + RESET_MOVE_DIMS[1]
    #)
    #return "reset move"

def run(GameBoard):
    renderConstants.frame_time = time.process_time()
    turn = GameBoard.timeCounter
    ap = GameBoard.resources[0].currentValue
    resources = min(50, GameBoard.resources[2].maxValue)
    display_surface.fill((0, 0, 0))
    #######
    for x in range(constants.ROWS):
        cellX = int(renderConstants.GRIDRECT.left + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * x + renderConstants.CELLOFF)
        for y in range(constants.ROWS):
            cellY = int(renderConstants.GRIDRECT.top + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * y + renderConstants.CELLOFF)
            display_surface.blit(GameBoard.States[y][x].cellType.image, (cellX, cellY))
    #######
    for y in range(len(GameBoard.States)):
        arr = GameBoard.States[y]
        for x in range(len(arr)):
            state = GameBoard.States[y][x]
            if state.person != None:
                state.person.animation = state.person.animation.getNextAnimation()
                display_surface.blit(state.person.animation.getImage(), cellPosition(x, y))
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
    display_surface.blit(resourceBar, resourceBarPos)
    display_surface.blit(resourceIcon, (iconDist, iconDist - iconYOff))
    resourceBarRect.width = resourceRectBound * resources / GameBoard.resources[2].maxValue
    pygame.draw.rect(display_surface, (202, 0, 69), resourceBarRect)
    resourceText = resourceFont.render('Resources: ' + str(int(resources)) + "/" + str(GameBoard.resources[2].maxValue), True, (255, 255, 255))
    display_surface.blit(resourceText, resourceTextRect)
    #######
    display_surface.blit(apImage, apImagePos)
    apBarRect.width = apRectBound * ap / GameBoard.resources[0].maxValue
    pygame.draw.rect(display_surface, (239, 73, 52), apBarRect)
    apText = apFont.render('Action Points: ' + str(ap) + "/" + str(GameBoard.resources[0].maxValue), True, (255, 255, 255))
    display_surface.blit(apText, apTextRect)
    #######
    if(healing):
        display_surface.blit(healImageOpen, healImagePos)
    else:
        display_surface.blit(healImage, healImagePos)
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


def display_image(
    screen: pygame.Surface,
    itemStr: str,
    dimensions: Tuple[int, int],
    position: Tuple[int, int],
):
    """
    Draw an image on the screen at the indicated position.
    """
    #v = pygame.image.load(itemStr).convert_alpha()
    #v = pygame.transform.scale(v, dimensions)
    #screen.blit(v, position)
    a=1


def build_grid(GameBoard):
    """
    Draw the grid on the screen.
    """
    grid_width = GameBoard.columns * CELL_DIMENSIONS[0]
    grid_height = GameBoard.rows * CELL_DIMENSIONS[1]
    # left
    pygame.draw.rect(
        screen,
        BLACK,
        [
            MARGIN - LINE_WIDTH,
            MARGIN - LINE_WIDTH,
            LINE_WIDTH,
            grid_height + (2 * LINE_WIDTH),
        ],
    )
    # right
    pygame.draw.rect(
        screen,
        BLACK,
        [
            MARGIN + grid_width,
            MARGIN - LINE_WIDTH,
            LINE_WIDTH,
            grid_height + (2 * LINE_WIDTH),
        ],
    )
    # bottom
    pygame.draw.rect(
        screen,
        BLACK,
        [
            MARGIN - LINE_WIDTH,
            MARGIN + grid_height,
            grid_width + (2 * LINE_WIDTH),
            LINE_WIDTH,
        ],
    )
    # top
    pygame.draw.rect(
        screen,
        BLACK,
        [
            MARGIN - LINE_WIDTH,
            MARGIN - LINE_WIDTH,
            grid_width + (2 * LINE_WIDTH),
            LINE_WIDTH,
        ],
    )
    # Fill the inside wioth the cell color
    pygame.draw.rect(
        screen,
        CELL_COLOR,
        [MARGIN, MARGIN, grid_width, grid_height],
    )

    # Draw the vertical lines
    i = MARGIN + CELL_DIMENSIONS[0]
    while i < MARGIN + grid_width:
        pygame.draw.rect(screen, BLACK, [i, MARGIN, LINE_WIDTH, grid_height])
        i += CELL_DIMENSIONS[0]
    # Draw the horizontal lines
    i = MARGIN + CELL_DIMENSIONS[1]
    while i < MARGIN + grid_height:
        pygame.draw.rect(screen, BLACK, [MARGIN, i, grid_width, LINE_WIDTH])
        i += CELL_DIMENSIONS[1]


def display_people(GameBoard):
    """
    Draw the people (government, vaccinated, and zombies) on the grid.
    """
    for arr in GameBoard.States:
        for state in arr:
            if state.person != None:
                p = state.person
                char = "Assets/" + IMAGE_ASSETS[0]
                if p.isVaccinated:
                    char = "Assets/" + IMAGE_ASSETS[1]
                elif p.isZombie:
                    char = "Assets/" + IMAGE_ASSETS[2]
                coords = (
                    int(x % GameBoard.rows) * CELL_DIMENSIONS[0] + MARGIN + 35,
                    int(x / GameBoard.columns) * CELL_DIMENSIONS[1] + MARGIN + 20,
                )
                display_image(screen, char, (35, 60), coords)


def display_cur_move(cur_move: List):
    # Display the current action
    #screen.blit(
    #    font.render("Your move is currently:", True, WHITE),
    #    CUR_MOVE_COORDS,
    #)
    #screen.blit(
    #    font.render(f"{cur_move}", True, WHITE),
    #    (
    #        CUR_MOVE_COORDS[0],
    #        CUR_MOVE_COORDS[1] + font.size("Your move is currently:")[1] * 2,
    #    ),
    #)
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
textW = resultFont.render("You win!", True, WHITE)
textW2 = resultFont2.render("You understood the assignment", True, WHITE)
textL = resultFont.render("You lose... Noob", True, WHITE)
textL2 = resultFont2.render("You know you're supposed to keep the human alive?", True, WHITE)
#######
def displayResultScreen(won):
    def movie():
        res = None
        if(won):
            res = Video(r'Assets/UI/LRatio2.mp4')
            res.set_volume(0.1)
        else:
            res = Video(r'Assets/UI/Sadge.mp4')
            res.set_volume(0.9)
        return res
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
        text = textW
        text2 = textW2
        images = winImages
        if(not won):
            text = textL
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
        if(endTime - startTime1 >= videoDuration - 1):
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
