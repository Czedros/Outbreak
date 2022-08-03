from os import system
from types import NoneType
from Cell import Cells
from State import State
import random as rd
from random import Random
from Person import Person
from typing import List, Tuple
from constants import *
from Resource import Resource
import renderConstants
from Animator import Animations
from Animator import Animation
from Obstacle import Obstacles
import Animator
import PygameFunctions as PF
#Human_Ai imports
from State_MC import State_MC
from Play import Play
import copy 
from ZombieAI import ZombieAI

class Board:
    resources = [
            Resource("Human AP", 8, {"Move" : 1 , "Cure": 3, } ), 
            Resource("Food", 100, {"Gather": 5 , "Consume" : 3 }), 
            Resource("Survivors", 10000, {"Gain" : 1} )
        ]
    def __init__(self,  dimensions: Tuple[int, int],
        player_role: str,
    excludeMap = None, rand = 10):
        self.rand = Random()
        self.rand.seed(rand)
        self.randSeed = rand
        self.rows = dimensions[0]
        self.columns = dimensions[1]
        self.player_role = player_role
        self.player_num = ROLE_TO_ROLE_NUM[player_role]
        self.population = 0
        self.States = []
        self.QTable = []
        self.isDay = True
        self.timeCounter = 0

        self.resources = [
            Resource("Human AP", 8, {"Move" : 1 , "Cure": 3, } ), 
            Resource("Food", 100, {"Gather": 5 , "Consume" : 3 }), 
            Resource("Survivors", 10000, {"Gain" : 1} )
        ]
        self.resources[0].alterByValue(8)
        self.resources[1].setToMax()
        for y in range(dimensions[1]):
            a = []
            for x in range(dimensions[0]):
                a.append(State(None, Cells.nan.value, (x, y)))
                self.QTable.append([0] * 6)#Don't know what this does and it's not my problem lol
            self.States.append(a)
        self.map = (self.rand.randint(0, CHUNKS[0] - 1), self.rand.randint(0, CHUNKS[1] - 1))
        while(self.map == excludeMap):
            self.map = (self.rand.randint(0, CHUNKS[0] - 1), self.rand.randint(0, CHUNKS[1] - 1))
        PF.imageToGrid(r'Assets/TestGrids/TrueGrid.png', r'Assets/TestGrids/TrueGridObstacles.png', self.States, self.map)
        self.actionToFunction = {
            "moveUp": self.moveUp,
            "moveDown": self.moveDown,
            "moveLeft": self.moveLeft,
            "moveRight": self.moveRight,
            "heal": self.heal,
            "bite": self.bite,
        }
    
    #MCTS FUNCTIONS
    def start(self):
        """
        return the intial game state
        only call at beginning :)
        """
        boardC = self.clone(self.States, self.player_role) #copy
        copied = State_MC([], boardC, 1)
        return copied
        
    def legal_plays(self, state : State_MC):
        """
         return the current player's legal moves from given state
         Difference for Zombie
         Difference for Human
        """
        print("LEGALPLAYS")
        legalPlays = []
        if state.isPlayer(1):         
            print("LEGAL PLAYS get possible moves for human")
            role = 'Human'
            acts = state.board.get_possible_moves(role)
            for a in acts:
                #list of [coord, action]
                #print("Action is:", a[1], "to coordinates:", a[0][0], a[0][1])
                legalPlays.append(Play(a[0][0], a[0][1], player = 1, Z = None, Zmove = a[1])) #Human Move 
        else: 
            role = 'Zombie'
            coords = state.board.get_possible_moves(role)
            print("LEGAL PLAYS get possible moves for zombie")
            for val in coords:
                #a list 
                 #poss is a list of lists
                  #each list has first element tupe, second element zombie ai
                    #tuple first element is either move or bite, second element is a tuple or coords, third element is the specific string
                print("Action is:", val[0][2], "to coordinates:", val[0][1][0], val[0][1][1])
                legalPlays.append(Play(val[0][1][0], val[0][1][1], player = -1, Z = val[1], Zmove = val[0][2]))  #Zombie Move
        print("End make Legal Moves")
        return legalPlays

    def next_state(self, state: State_MC, play):
        """
        advance the given state and return the new state
        """
      
        print("NEXT_STATE")
        newHistory = copy.copy(state.playHistory)

        if state.isPlayer(-1):
            for p in play:
                newHistory.append(p)
        else: newHistory.append(play)

        oldT = state.board.timeCounter
        newBoard = state.board.clone(state.board.States, state.board.player_role) 
        newBoard.timeCounter = oldT
        print("next_State newBoard check its timeCounter", newBoard.timeCounter)
        
        if state.isPlayer(1): #next_state for player
            print("NEXT_STATE HUMAN ") 
            print("player move is ", play.Zmove)
            if play.Zmove == "move":
                newBoard.move(newBoard.findPlayer(), (play.row, play.col)) #player occupies this place now
            elif play.Zmove == "heal":
                newBoard.heal((play.row, play.col))
            elif play.Zmove == "refresh":
                newBoard.newBoard()
            else: #to wait 
                pass
            newBoard.update() 
        else:
            print("NEXT_STATE ZOMBIES")
            newBoard.pZombieID(newBoard) #debug purposes
            for p in play: #all the plays for each zombie
                if p.Zmove != 'bite':
                    newBoard.move(newBoard.findPerson(p.Z.ID), (p.row, p.col))     
                else:
                    print("bitting at: ", p.row, p.col)
                    biteSuccess = newBoard.bite((p.row, p.col))
                    if biteSuccess: #if bite is successful
                        print("bite success") 
                        return State_MC(newHistory, newBoard, -state.player)
        newPlayer = -state.player #next player's turn
        return State_MC(newHistory, newBoard, newPlayer)
             

    #TODO: change with more mechanics probably
    def winner(self, winstate):
        print("winner is called")
        if winstate is not None:
            print("timeCounter", winstate.board.timeCounter)
            if winstate.board.timeCounter == 40:
                print("survived")
                PF.dataWrite("dataCollectionPlayer.csv", [winstate.board.resources[1].currentValue, winstate.board.resources[2].currentValue, winstate.board.timeCounter, 'win', "Survived"])
                return 1
            if winstate.board.resources[1].currentValue < 1:
                print("lost starvation")
                PF.dataWrite("dataCollectionPlayer.csv", [winstate.board.resources[1].currentValue, winstate.board.resources[2].currentValue, winstate.board.timeCounter, 'lose', "Starvation"])
                return -1 #human lost
            if (not winstate.board.containsPerson(False)):
                print("lost infection")
                PF.dataWrite("dataCollectionPlayer.csv", [winstate.board.resources[1].currentValue, winstate.board.resources[2].currentValue, winstate.board.timeCounter, 'lose', "Infection"])
                return -1 #human lost
            if winstate.board.num_zombies() > 0 and winstate.board.populationF() != winstate.board.num_zombies():
                print("game ongoing")
                return None #no winner yet
        else:
            print("winstate is None")

    def pZombieID(self, board):
        for arr in board.States:
                for s in arr:
                    if s.person is not None and s.person.isZombie == True:
                        print("Zombie ID:", s.person.ai.ID)

    # End of AI

    def newBoard(self):
        coords = self.findPlayer()
        playerCoord = self.findPlayer()
        ret = Board((ROWS, COLUMNS), self.player_role, excludeMap = self.map, rand = (playerCoord[0] + playerCoord[1] * self.columns))
        ret.resources = self.resources
        ret.timeCounter = self.timeCounter
        ret.isDay = self.isDay
        ret.populate()
        return ret

    def num_zombies(self) -> int:
        r = 0
        for arr in self.States:
            for state in arr:
                if state.person is not None and state.person.isZombie:
                    if state.person.isZombie:
                        r += 1
        return r

    def act(self, oldstate: Tuple[int, int], givenAction: str):
        cell = self.toCoord(oldstate)
        f = self.actionToFunction[givenAction](cell)
        reward = self.States[cell[1]][cell[0]].evaluate(givenAction, self)
        if f[0] == False:
            reward = 0
        return [reward, f[1]]

    def containsPerson(self, isZombie: bool):
        for arr in self.States:
            for state in arr:
                if state.person is not None and state.person.isZombie == isZombie:
                    return True
        return False
    def findPerson(self, ID):
        for arr in self.States:
            for state in arr:
                if state.person is not None and state.person.isZombie and state.person.ai.ID == ID:
                    return state.location
    def findPlayer(self):
        for arr in self.States:
            for state in arr:
                if state.person is not None and state.person.isZombie == False:
                    return state.location

    def get_possible_moves(self, role: str):
        """
        Get the coordinates of people (or zombies) that are able
        to make the specified move.
        AHHHHHHHHHHHHHHHHHHHHHHHHH I MISREAD THIS change it to the coordinates of the new move
        @param action - the action to return possibilities for (options are 'bite', 'moveUp', 'moveDown','moveLeft', 'moveRight', and 'heal')
        @param role - either 'Zombie' or 'Human'; helps decide whether an action
        is valid and which people/zombies it applies to
        """
        poss = []
        B = self.clone(self.States, role)

        
        if role == 'Zombie':
            zombies = []
            for arr in B.States:
                for s in arr:
                    if s.person is not None and s.person.isZombie == True:
                        zombies.append(s.person.ai)
            for zomb in zombies:
                poss.append([zomb.performAction(B), zomb])
                #poss is a list of lists
                  #each list has first element tupe, second element zombie ai
                    #tuple first element is either move or bite, second element is a tuple or coords, third element is the specific string
        elif role == 'Human':
            action = ["move", "heal", "wait", "refresh"] #add refresh later
            if not self.containsPerson(False):
                return poss
            for act in action:
                playerPos = self.findPlayer()
                if act == "move" and B.resources[0].currentValue > 0:
                    vals = [
                        (playerPos[0], playerPos[1] + 1),
                        (playerPos[0], playerPos[1] - 1),
                        (playerPos[0] + 1, playerPos[1]),
                        (playerPos[0] - 1, playerPos[1]),
                    ]
                    for coordinate in vals:
                        if B.isValidCoordinate(coordinate) and B.States[coordinate[1]][coordinate[0]].person == None:
                            if B.States[coordinate[1]][coordinate[0]].passable() == True:
                                poss.append([coordinate, "move"])
                if act == "heal" and B.resources[0].currentValue > 1:
                    vals = [
                        (playerPos[0], playerPos[1] + 1),
                        (playerPos[0], playerPos[1] + 1),
                        (playerPos[0], playerPos[1] - 1),
                        (playerPos[0] + 1, playerPos[1]),
                        (playerPos[0] - 1, playerPos[1]),
                        (playerPos[0]+ 1, playerPos[1] + 1),
                        (playerPos[0]- 1, playerPos[1] - 1),
                        (playerPos[0] + 1, playerPos[1] - 1),
                        (playerPos[0] - 1, playerPos[1] + 1),
                        (playerPos[0], playerPos[1])
                    ]
                    for coord in vals:
                        if (B.isValidCoordinate(coord) 
                            and B.States[coord[1]][coord[0]].person is not None ):
                            poss.append([coord, "heal"])
                if act == "refresh" and B.resources[0].currentValue == 8:
                    poss.append([playerPos, "refresh"])
                if act == "wait":
                    poss.append([playerPos, "wait"])
        return poss

    def toCoord(self, i: int):
        return (int(i % self.columns), int(i / self.rows))

    def toIndex(self, coord: Tuple[int, int]):
        try:
            return int(coord[1] * self.columns) + int(coord[0])
        except:
            pass

    def isValidCoordinate(self, coordinates: Tuple[int, int]):
        return (
            coordinates[1] < self.rows
            and coordinates[1] >= 0
            and coordinates[0] < self.columns
            and coordinates[0] >= 0
        )

    def clone(self, L: List[List[State]], role: str):
        Person.classID = 0
        ZombieAI.classID = 0
        playerCoord = self.findPlayer()
        NB = Board(
            (self.rows, self.columns),
            self.player_role, 
            rand = self.randSeed
        )
        #NB.States = [state.clone() for state in L]#No idea what this means :/
        for y in range(len(L)):
            NB.States[y] = [state.clone() for state in L[y]]
            
        NB.player_role = role
        NB.rand.setstate(self.rand.getstate())
        return NB

    def isAdjacentTo(self, coord: Tuple[int, int], is_zombie: bool) -> bool:
        ret = False
        vals = [
            (coord[0], coord[1] + 1),
            (coord[0], coord[1] - 1),
            (coord[0] + 1, coord[1]),
            (coord[0] - 1, coord[1]),
        ]
        for coord in vals:
            if (
                self.isValidCoordinate(coord)
                and self.States[coord[1]][coord[0]].person is not None
                and self.States[coord[1]][coord[0]].person.isZombie == is_zombie
            ):
                ret = True
                break

        return ret

    def isNear(self, coord: Tuple[int, int]) -> bool:
        ret = False
        vals = [
            (coord[0], coord[1] + 1),
            (coord[0], coord[1] - 1),
            (coord[0] + 1, coord[1]),
            (coord[0] - 1, coord[1]),
            (coord[0]+ 1, coord[1] + 1),
            (coord[0]- 1, coord[1] - 1),
            (coord[0] + 1, coord[1] - 1),
            (coord[0] - 1, coord[1] + 1),
            (coord[0], coord[1])
        ]
        for coord in vals:
            #print(coord)
            if (self.isValidCoordinate(coord) 
                and self.States[coord[1]][coord[0]].person is not None 
                and self.States[coord[1]][coord[0]].person.isZombie == False):
                ret = True
                break

        return ret

    def move(
        self, from_coords: Tuple[int, int], new_coords: Tuple[int, int], mult = 1
    ) -> Tuple[bool, int]:
        """
        Check if the move is valid.
        If valid, then implement the move and return [True, destination_idx]
        If invalid, then return [False, None]
        If the space is currently occupied, then return [False, destination_idx]
        """
        # Get the start and destination index (1D)
        start_idx = self.toIndex(from_coords)
        destination_idx = self.toIndex(new_coords)

        # Check if the new coordinates are valid
        if not self.isValidCoordinate(new_coords):
            return [False, destination_idx]
        #Checks if you have enough AP
            
        # Check if the destination is currently occupied
        #print(self.States[new_coords[1]])
        try:    
            if self.States[new_coords[1]][new_coords[0]].passable():
                if self.States[from_coords[1]][from_coords[0]].person.isZombie:
                    if self.States[from_coords[1]][from_coords[0]].person.AP.checkCost("Move") * mult <=  self.States[from_coords[1]][from_coords[0]].person.AP.currentValue:
                        self.States[new_coords[1]][new_coords[0]].person = self.States[from_coords[1]][from_coords[0]].person
                        self.States[from_coords[1]][from_coords[0]].person = None
                        self.States[new_coords[1]][new_coords[0]].person.AP.alterByValue(-mult)
                        return [True, destination_idx]
                    else:
                        print("Not enough AP")
                else:
                    if  self.resources[0].currentValue >= self.resources[0].checkCost("Move") * mult:
                        self.States[new_coords[1]][new_coords[0]].person = self.States[from_coords[1]][from_coords[0]].person
                        self.States[from_coords[1]][from_coords[0]].person = None
                        self.resources[0].alterByValue(-mult)
                        return [True, destination_idx]
            return [False, destination_idx, new_coords]
        except:
            pass

    def moveUp(self, coords: Tuple[int, int]) -> Tuple[bool, int]:
        new_coords = (coords[0], coords[1] - 1)
        print("player moved up if there was enough AP, action completed successfully in Board")
        return self.move(coords, new_coords)

    def moveDown(self, coords: Tuple[int, int]) -> Tuple[bool, int]:
        new_coords = (coords[0], coords[1] + 1)
        print("player moved down if there was enough AP, action completed successfully in Board")
        return self.move(coords, new_coords)

    def moveLeft(self, coords: Tuple[int, int]) -> Tuple[bool, int]:
        new_coords = (coords[0] - 1, coords[1])
        print("player moved left if there was enough AP, action completed successfully in Board")
        return self.move(coords, new_coords)

    def moveRight(self, coords: Tuple[int, int]) -> Tuple[bool, int]:
        new_coords = (coords[0] + 1, coords[1])
        print("player moved right if there was enough AP, action completed successfully in Board")
        return self.move(coords, new_coords)

    def QGreedyat(self, state_id: int):
        biggest = self.QTable[state_id][0] * self.player_num
        ind = 0
        A = self.QTable[state_id]
        i = 0
        for qval in A:
            if (qval * self.player_num) > biggest:
                biggest = qval
                ind = i
            i += 1
        return [ind, self.QTable[ind]]  # action_index, qvalue

    def choose_action(self, state_id: int, lr: float):
        L = lr * 100
        r = rd.randint(0, 100)
        if r < L:
            return self.QGreedyat(state_id)
        else:
            if self.player_num == 1:  # Player is Govt
                d = rd.randint(0, 4)
            else:
                d = rd.randint(0, 5)
                while d != 4:
                    d = rd.randint(0, 4)
            return d

    def choose_state(self, lr: float):
        L = lr * 100
        r = rd.randint(0, 100)
        if r < L:
            biggest = None
            sid = None
            for y in range(len(self.States)):
                arr = self.States[y]
                for x in range(len(arr)):
                    if arr[x].person != None:
                        q = self.QGreedyat(x + y * self.columns)
                        if biggest is None:
                            biggest = q[1]
                            sid = x + y * self.columns
                        elif q[1] > biggest:
                            biggest = q[1]
                            sid = x + y * self.columns
            return self.QGreedyat(sid)
        else:
            if self.player_num == -1:  # Player is Govt
                d = (rd.randint(0, self.columns), rd.randint(0, self.rows))
                while self.States[d[1]][d[0]].person is None or self.States[d[1]][d[0]].person.isZombie:
                    d = (rd.randint(0, self.columns), rd.randint(0, self.rows))
            else:
                d = (rd.randint(0, self.columns), rd.randint(0, self.rows))
                while (
                    self.States[d[1]][d[0]].person is None
                    or self.States[d[1]][d[0]].person.isZombie == False
                ):
                    d = (rd.randint(0, self.columns), rd.randint(0, self.rows))
            return d

    def bite(self, coords: Tuple[int, int]) -> Tuple[bool, int]:
        i = self.toIndex(coords)
        work = self.States[coords[1]][coords[0]].person.calcInfect()
        print("Infection has either failed or succeeded, action completed successfully in Board")
        return [work, i]

    def heal(self, coords: Tuple[int, int], infRange = False) -> Tuple[bool, int]:
        """
        Cures or vaccinates the person at the stated coordinates.
        If there is a zombie there, the person will be cured.
        If there is a person there, the person will be vaccinated
        If no person is selected, then return [False, None]
        if a person is vaccined, then return [True, index]
        """
        i = self.toIndex(coords)
        if self.States[coords[1]][coords[0]].person is None:
            return [False, None]
        if self.isNear(coords) == False and not infRange:
            print("Out of Range!")
            return [False, None]
        if self.resources[0].currentValue < 2:
            print("Not Enough AP")
            return [False, None]
        self.resources[0].alterByValue(-2)
        p = self.States[coords[1]][coords[0]].person

        if p.isZombie:
            if p.calcCureSuccess():
                self.States[coords[1]][coords[0]].person = None
                self.resources[2].alterByValue(1)
            
        else:
            p.get_vaccinated()
            print("Person is now vaccinated, action completed successfully in Board")
            p.animation= Animation(Animations.vaccinate.value)
        return [True, i]

    def get_possible_states(self, role_number: int):
        indexes = []
        i = 0
        for arr in self.States:
            for state in arr:
                if state.person != None:
                    if role_number == 1 and state.person.isZombie == False:
                        indexes.append(i)
                    elif role_number == -1 and state.person.isZombie:
                        indexes.append(i)
                i += 1
        return indexes

    def step(self, role_number: int, learningRate: float):
        P = self.get_possible_states(role_number)
        r = rd.uniform(0, 1)
        if r < learningRate:
            rs = (rd.randrange(0, self.columns - 1), rd.randrange(0, self.rows - 1))
            if role_number == 1:
                while (
                    self.States[rs[1]][rs[0]].person is not None
                    and self.States[rs[1]][rs[0]].person.isZombie
                ):
                    rs = (rd.randrange(0, self.columns - 1), rd.randrange(0, self.rows - 1))
            else:
                while (
                    self.States[rs[1]][rs[0]].person is not None
                    and self.States[rs[1]][rs[0]].person.isZombie == False
                ):
                    rs = (rd.randrange(0, self.columns - 1), rd.randrange(0, self.rows - 1))

            # random state and value
        # old_value = QTable[state][acti]
        # next_max = np.max(QTable[next_state])
        # new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        # QTable[state][acti] = new_value

    def populate(self):
        total = 7
        poss = []
        for arr in self.States:
            for state in arr:
                state.person = None
        humanPos = (self.rand.randint(0, self.columns - 1), self.rand.randint(0, self.rows - 1))
        while(not self.States[humanPos[1]][humanPos[0]].cellType.passable or self.States[humanPos[1]][humanPos[0]].obstacle != None):
            humanPos = (self.rand.randint(0, self.columns - 1), self.rand.randint(0, self.rows - 1))
        self.States[humanPos[1]][humanPos[0]].person = Person(False)
        poss = []
        for i in range(total):
            pos = (self.rand.randint(0, self.columns - 1), self.rand.randint(0, self.rows - 1))
            while(not self.States[pos[1]][pos[0]].cellType.passable or self.States[pos[1]][pos[0]].obstacle != None or self.States[pos[1]][pos[0]].person != None or (abs(pos[0] - humanPos[0]) + abs(pos[1] - humanPos[1])) <= 3):
                pos = (self.rand.randint(0, self.columns - 1), self.rand.randint(0, self.rows - 1))
            p = Person(True)
            #print("zombie", p.ID, p.ai.ID) #ID and aiID are different
            self.States[pos[1]][pos[0]].person = p
        self.population = total + 1
    def zombieWave(self):
        total = self.rand.randint(1,7)
        humanPos = self.findPlayer()
        for i in range(total):
            pos = (self.rand.randint(0, self.columns - 1), self.rand.randint(0, self.rows - 1))
            while(not self.States[pos[1]][pos[0]].cellType.passable or self.States[pos[1]][pos[0]].obstacle != None or self.States[pos[1]][pos[0]].person != None or (abs(pos[0] - humanPos[0]) + abs(pos[1] - humanPos[1])) <= 2 or (abs(pos[0] - humanPos[0]) + abs(pos[1] - humanPos[1])) > 6):
                pos = (self.rand.randint(0, self.columns - 1), self.rand.randint(0, self.rows - 1))
            p = Person(True)
            self.States[pos[1]][pos[0]].person = p

    def pickup(self, coord):
        if(self.States[coord[1]][coord[0]].obstacle == Obstacles.resource.value):
            self.States[coord[1]][coord[0]].obstacle = None
            self.resources[1].alterByPercent(6*self.resources[2].currentValue, False)
    def findPath(self, from_coord, to_coord):#Tiankuo, you can replace this with you're path finding algorithm, but I need to call a path finding algorithm for my UI
        oldCoords = [{from_coord: None}]
        while True:
            newCoords = {}
            curCoordsOld = oldCoords[len(oldCoords) - 2]
            curCoords = oldCoords[len(oldCoords) - 1]
            for i in curCoords:
                if i == to_coord:
                    cur = i
                    res = [cur]
                    for i2 in range(len(oldCoords) - 1, 1, -1):
                        cur = oldCoords[i2][cur]
                        res.append(cur)
                    res.reverse()
                    return res
                news = []
                if (i[0] != 0 and self.States[i[1]][i[0] - 1].passable()):
                    news.append((i[0] - 1, i[1]))
                if (i[1] != 0 and self.States[i[1] - 1][i[0]].passable()):
                    news.append((i[0], i[1] - 1))
                if (i[1] != COLUMNS - 1 and self.States[i[1] + 1][i[0]].passable()):
                    news.append((i[0], i[1] + 1))
                if (i[0] != ROWS - 1 and self.States[i[1]][i[0] + 1].passable()):
                    news.append((i[0] + 1, i[1]))
                for i2 in news:
                    if (i2 not in newCoords.keys() and i2 not in curCoordsOld.keys()):
                        newCoords[i2] = i
            if(len(newCoords) == 0):
                return None
            oldCoords.append(newCoords)
    def update(self, isHuman = True):
        """
        Update each of the states;
        This method should be called at the end of each round
        (after player and computer have each gone once)
        """ 
        self.resources[0].alterByValue(2)
        if(isHuman):
            self.timeCounter += 1
            self.isDay = self.timeCounter % renderConstants.CYCLELEN < renderConstants.CYCLELEN/2
            self.resources[1].alterByPercent(-1*(1+self.resources[2].currentValue), True)
            #TODO: add zombie wave later
            #if(self.timeCounter % renderConstants.CYCLELEN == renderConstants.CYCLELEN/2):
                #self.zombieWave()
                #elif(self.timeCounter % renderConstants.CYCLELEN == 0 and self.timeCounter != 0):
                #    self.populate()
            #print(self.resources[1].currentValue)
        for arr in self.States:
            for state in arr:
                state.update()
        
        def __hash__(self):
            return hash(self.States)
    def populationF(self):  #Hannah added 
        counter = 0
        for arr in self.States:
            for s in arr:
                if s.person is not None:
                    counter+=1
        return counter            



