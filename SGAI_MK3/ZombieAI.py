class ZombieAI :
    currentState = ""
    active = False
    seekPosition = [1, 1]
    ID = 0
    currentBoard = [[0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0]]
    selfPosition = [2,2]
    def __init__(self):
        self.active = True
        self.ID = ZombieAI.ID + 1
    def createMap(self, gameboard):
        return False
    def positionUpdate(self, gameBoard):
        self.position = gameBoard.findPerson(self.ID)
    def setState(self, state):
        self.currentState = state
    
    def stateSeek(self, ):  
         

        if self.seekPosition == self.position():
            self.setState("Roam")
    def stateAttack(self, board):
        return False
    def playerFind(self, board):
        return False
    def stateRoam(self, board):
        return False