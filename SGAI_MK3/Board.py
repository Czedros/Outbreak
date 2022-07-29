from os import system
from Cell import Cells
from State import State
import random as rd
from Person import Person
from typing import List, Tuple
from constants import *
from Resource import Resource
import renderConstants
from Animator import Animations
from Animator import Animation
from Obstacle import Obstacles
import Animator
import PygameFunctions

class Board:
    def __init__(self,  dimensions: Tuple[int, int],
        player_role: str,
    ):
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
        PygameFunctions.imageToGrid(r'Assets/TestGrids/TrueGrid.png', r'Assets/TestGrids/TrueGridObstacles.png', self.States, (rd.randint(0, CHUNKS[0] - 1), rd.randint(0, CHUNKS[1] - 1)))
        self.actionToFunction = {
            "moveUp": self.moveUp,
            "moveDown": self.moveDown,
            "moveLeft": self.moveLeft,
            "moveRight": self.moveRight,
            "heal": self.heal,
            "bite": self.bite,
        }

    def num_zombies(self) -> int:
        r = 0
        for arr in self.States:
            for state in arr:
                if state.person != None:
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
                if state.person is not None and state.person.ai.ID == ID:
                    return state.location

    def get_possible_moves(self, action: str, role: str):
        """
        Get the coordinates of people (or zombies) that are able
        to make the specified move.
        @param action - the action to return possibilities for (options are 'bite', 'moveUp', 'moveDown','moveLeft', 'moveRight', and 'heal')
        @param role - either 'Zombie' or 'Human'; helps decide whether an action
        is valid and which people/zombies it applies to
        """
        poss = []
        B = self.clone(self.States, role)

        if role == "Zombie":
            if not self.containsPerson(True):
                return poss
            for y in range(len(self.States)):
                arr = self.States[y]
                for x in range(len(arr)):
                    state = arr[x]
                    if state.person is not None:
                        changed_states = False

                        if (
                            action == "bite"
                            and not state.person.isZombie
                            and self.isAdjacentTo((x, y), True)
                            and state.person.AP.currentValue > 1
                        ):
                            # if the current space isn't a zombie and it is adjacent
                            # a space that is a zombie
                            poss.append((x, y))
                            changed_states = True
                        elif (
                            action != "bite"
                            and state.person.isZombie
                            and B.actionToFunction[action]((x, y))[0]
                            and state.person.AP.currentValue > 0
                        ):
                            poss.append((x, y))
                            changed_states = True

                        if changed_states:
                            # reset the states
                            #B.States = [
                            #    self.States[int(i / self.columns)][i % self.columns].clone()
                            #    if self.States[int(i / self.columns)][i % self.columns] != B.States[int(i / self.columns)][i % self.columns]
                            #    else B.States[int(i / self.columns)][i % self.columns]
                            #    for i in range(self.columns * self.rows)
                            #]
                            B.States = []
                            for y in range(len(self.States)):
                                arr = self.States[y]
                                arrB = [None] * self.columns
                                for x in range(len(arr)):
                                    arrB[x] = self.States[y][x].clone()
                                    #if(arr[x] == arrB[x]):
                                B.States.append(arrB)

        elif role == "Human":
            if not self.containsPerson(False):
                return poss
            for y in range(len(self.States)):
                arr = self.States[y]
                for x in range(len(arr)):
                    state = arr[x]
                    if state.person is not None:
                        changed_states = False
                        if action == "heal" and (
                            state.person.isZombie or not 
                            state.person.isVaccinated 
                            and self.resources[0].currentValue > 2
                        ):
                            poss.append((x, y))
                            changed_states = True
                        elif (
                            action != "heal"
                            and not state.person.isZombie
                            and B.actionToFunction[action]((x, y))[0]
                            and self.resources[0].currentValue > 0
                        ):
                            poss.append((x, y))
                            changed_states = True

                        if changed_states:
                            # reset the states
                            #B.States = [
                            #    self.States[int(i / self.columns)][i % self.columns].clone()
                            #    if self.States[int(i / self.columns)][i % self.columns] != B.States[int(i / self.columns)][i % self.columns]
                            #    else B.States[int(i / self.columns)][i % self.columns]
                            #    for i in range(self.columns * self.rows)
                            #]
                            B.States = []
                            for y in range(len(B.States)):
                                arr = self.States.States[y]
                                arrB = [None] * self.columns
                                for x in range(len(arr)):
                                    arrB[x] = self.States[y][x].clone()
                                    #if(arr[x] == arrB[x]):
                                B.States.append(arrB)
        return poss

    def toCoord(self, i: int):
        return (int(i % self.columns), int(i / self.rows))

    def toIndex(self, coordinates: Tuple[int, int]):
        return int(coordinates[1] * self.columns) + int(coordinates[0])

    def isValidCoordinate(self, coordinates: Tuple[int, int]):
        return (
            coordinates[1] < self.rows
            and coordinates[1] >= 0
            and coordinates[0] < self.columns
            and coordinates[0] >= 0
        )

    def clone(self, L: List[List[State]], role: str):
        NB = Board(
            (self.rows, self.columns),
            self.player_role,
        )
        #NB.States = [state.clone() for state in L]#No idea what this means :/
        for y in range(len(L)):
            NB.States[y] = [state.clone() for state in L[y]]
            
        NB.player_role = role
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
        if self.States[new_coords[1]][new_coords[0]].person is None and self.States[new_coords[1]][new_coords[0]].cellType.passable and (self.States[new_coords[1]][new_coords[0]].obstacle == None or self.States[new_coords[1]][new_coords[0]].obstacle.passable):
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

        return [False, destination_idx]

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
        if (
            self.States[coords[1]][coords[0]].person is None
            or self.States[coords[1]][coords[0]].person.isZombie
            or not self.isAdjacentTo(coords, True)
        ):
            return [False, None]
        if  self.States[coords[1]][coords[0]].person.AP.currentValue < 2:
            print("Not Enough AP")
            return [False, None]
        self.States[coords[1]][coords[0]].person.calcInfect()
        print("Infection has either failed or succeeded, action completed successfully in Board")
        return [True, i]

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
        for i in range(total):
            pos = (rd.randint(0, self.columns - 1), rd.randint(0, self.rows - 1))
            while(not self.States[pos[1]][pos[0]].cellType.passable or self.States[pos[1]][pos[0]].obstacle != None):
                pos = (rd.randint(0, self.columns - 1), rd.randint(0, self.rows - 1))
            poss.append(pos)
            self.States[pos[1]][pos[0]].person = Person(False)
        self.population = total
        used = []
        for x in range(total-1):
            s = rd.randint(0, len(poss) - 1)
            while s in used:
                s = rd.randint(0, len(poss) - 1)
            p = self.States[poss[s][1]][poss[s][0]].person
            p.isZombie = True
            p.animation = Animation(Animations.zombie.value)
            used.append(s)
    def pickup(self, coord):
        if(self.States[coord[1]][coord[0]].obstacle == Obstacles.resource.value):
            self.States[coord[1]][coord[0]].obstacle = None
            self.resources[1].alterByValue(5)
    def update(self):
        """
        Update each of the states;
        This method should be called at the end of each round
        (after player and computer have each gone once)
        """ 
        self.resources[0].alterByValue(2)
        self.timeCounter += 1
        self.isDay = self.timeCounter % renderConstants.CYCLELEN < renderConstants.CYCLELEN/2
        self.resources[1].alterByPercent(-1*(1+self.resources[2].currentValue), True)
        #print(self.resources[1].currentValue)
        for arr in self.States:
            for state in arr:
                state.update()
        
"""
Board:
def start(self): basically our __init__()

def current_player(self, state, play): find the player
    find the position of the player

def next_state(self, state, play):
    - state: a copy of our current board
    -specify the play:
        -call one of the Board.functions (moveUp, heal etc)
    -return the state 
def legal_plays(self, state_history):
    loop through state_history and call get_possible_moves

def winner(self, state_history):
    
    




"""