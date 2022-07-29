import time
from turtle import position
import renderConstants
import random as rd
class ZombieAI :
    currentState = "Roam"
    active = False
    states = ["Roam", "Seek", "Attack"]
    seekPosition = [1, 1]
    ID = 0
    Pathfinding = [[0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0]]
    selfPosition = [2,2]
    actionlist = {""}
    board = None
    vision = 3
    
    def __init__(self):
        self.active = True
        self.ID = ZombieAI.ID + 1

    def performAction(self, board):
        self.positionUpdate(board)
        self.seekPosition = board.findPlayer()
        if abs(self.seekPosition[0] - self.position[0]) + abs(self.seekPosition[1] - self.position[1]) <= 4:
            self.setState(1)
        if board.isAdjacentTo(self.position, False):
            self.setState(2)
        stateactions = {
            "Roam" : self.stateRoam(board),
            "Attack" : self.stateAttack(board),
            "Seek" : self.stateSeek(board)
        }
        stateactions[self.currentState]
        self.setState(0)
        
    def setState(self, state):
        self.currentState = self.states[state]

    def positionUpdate(self, gameBoard):
        self.position = gameBoard.findPerson(self.ID)

    def stateSeek(self, board):           
        if self.seekPosition == self.position():
            self.setState(0)
        possiblemoves = self.getLegalMoves(board)
        prevDistance = abs(self.seekPosition[0] - self.position[0]) + abs(self.seekPosition[1] - self.position[1]) 
        chosenMove = possiblemoves[0]
        for Move in possiblemoves:
            if abs(self.seekPosition[0] - (self.position[0] + Move[0])) + abs(self.seekPosition[1] - (self.position[1] + Move[1])) <= prevDistance:
                distance = prevDistance
                chosenMove = Move
        return chosenMove

    def stateAttack(self, board):
        return ["Bite", self.seekPosition]

    def stateRoam(self, gameBoard):
        possibleMoves = self.getLegalMoves(gameBoard)
        move = rd.random(possibleMoves) 
        return move

    def getLegalMoves(self, gameBoard):
        possible_move_coords = []
        
        vals = [
            (self.position[0], self.position[1] + 1),
            (self.position[0], self.position[1] - 1),
            (self.position[0] + 1, self.position[1]),
            (self.position[0] - 1, self.positiond[1]),
        ]
        for coordinate in vals:
            if gameBoard.isValidCoordinate(coordinate) and gameBoard.States[coordinate[1]][coordinate[0]].person == None:
                if gameBoard.States[coordinate[1]][coordinate[0]].isPassable == True:
                     possible_move_coords.append(coordinate)
        return possible_move_coords