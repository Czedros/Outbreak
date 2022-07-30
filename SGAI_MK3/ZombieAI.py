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
    selfPosition = [2,2]
    board = None
    vision = 3
    
    
    def __init__(self):
        self.active = True
        self.ID = ZombieAI.ID + 1 #creates the ID for the current Ai, for every AI increase by 1

    def performAction(self, board): 
        self.setState(0)
        self.positionUpdate(board) 
        self.seekPosition = board.findPlayer() #coords the player one
        if abs(self.seekPosition[0] - self.position[0]) + abs(self.seekPosition[1] - self.position[1]) <= 4: #a vision scenario: seek
            self.setState(1)
        if board.isAdjacentTo(self.position, False): #a vision scenario: attack
            self.setState(2)
        stateactions = {
            "Roam" : self.stateRoam(board),
            "Attack" : self.stateAttack(board),
            "Seek" : self.stateSeek(board)
        }
        return stateactions[self.currentState]
        
    def setState(self, state):
        self.currentState = self.states[state]

    def positionUpdate(self, gameBoard):
        self.position = gameBoard.findPerson(self.ID)

    def stateSeek(self, board):           
        if self.seekPosition == self.position(): #back to Roam
            self.setState(0)
        possiblemoves = self.getLegalMoves(board) #gets all possible move 
        prevDistance = abs(self.seekPosition[0] - self.position[0]) + abs(self.seekPosition[1] - self.position[1]) 
        chosenMove = possiblemoves[0]
        #find the position that is the closest to the human
        for Move in possiblemoves:
            if abs(self.seekPosition[0] - (self.position[0] + Move[0])) + abs(self.seekPosition[1] - (self.position[1] + Move[1])) <= prevDistance:
                distance = prevDistance 
                chosenMove = Move
        return ["move", chosenMove]

    def stateAttack(self, board):
        #Bite at the seeked position
        return ["bite", self.seekPosition]

    def stateRoam(self, gameBoard):
        possibleMoves = self.getLegalMoves(gameBoard)
        move = rd.choice(possibleMoves) 
        return ["move", move]

    def getLegalMoves(self, gameBoard): #legal moves for this zombie
        possible_move_coords = []
        
        vals = [
            (self.position[0], self.position[1] + 1),
            (self.position[0], self.position[1] - 1),
            (self.position[0] + 1, self.position[1]),
            (self.position[0] - 1, self.position[1]),
        ]
        for coordinate in vals:
            if gameBoard.isValidCoordinate(coordinate) and gameBoard.States[coordinate[1]][coordinate[0]].person == None:
                if gameBoard.States[coordinate[1]][coordinate[0]].passable() == True:
                     possible_move_coords.append(coordinate)
        return possible_move_coords