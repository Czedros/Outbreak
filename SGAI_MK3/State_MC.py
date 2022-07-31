
class State_MC:
    """
    State.py represents each square of the entire Board
    State_MC is class for a state of the entire game
    """
    def __init__(self, playHistory, board, player):
        self.playHistory = playHistory
        self.board = board
        self.player = player
    
    def isPlayer(self, player):
        #keep track who is who
        #+1 human (winner for Ai) -1 Zombie (loser for AI)
        return player == self.player 
    
    def __hash__(self): 
        #hashable; equality in playHistory
        return hash(self.playHistory)

        
