from Board import Board
import random as rd
from SGAI_MK3.Person import Person
from main import main

class ZombieAI :
    currentState = ""
    active = False
    seekPosition = [1, 1]
    currentBoard = [[0,0,0],
                    [0,0,0],
                    [0,0,0]]
    def __init__(self, gameboard):
        self.active = True
        self.states = {
            "Roam" : self.stateRoam(),
            "Seek" : self.stateSeek(),
            "Attack" : self.stateAttack()
        }
        self.createmap(gameboard)
    def act(self):
        self.states[self.currentState]

    def setState(self, state):
        self.currentState = self.states[state]

    def stateSeek(self ):
        Board.move()
        if(self.seekPosition = Board.currentPosition()):
            return False
    def stateAttack(self, board):
        return False
    def playerFind(self, board):
        return False
    def stateRoam(self, board):
        if(Board.)