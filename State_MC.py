
class State_MC:
    """
    This is a copy of self.States in the Board 
    State_MC is class for a state of the entire game, and ITS PLAYHISTORY that brings it to here
    """
    def __init__(self, playHistory, board, player, zombiesID = None):
        self.playHistory = playHistory
        self.board = board
        self.player = player
        self.zombiesID = zombiesID
    
    def isPlayer(self, player):
        #keep track who is who
        #+1 human (winner for Ai) -1 Zombie (loser for AI)
        return self.player == player
    
    def __hash__(self): 
        #hashable; equality in playHistory
        #So if two State_MC have the same playhistory that gets it to this State, then they are the same
        return hash(str(self.playHistory))
    
    def playHistoryArray(self):
        ret = []
        for i in self.playHistory:
            if(i.Z == None):
                ret.append(str(i.row) + "," + str(i.col) + "," + str(i.player)) 
        return ret

#TODO: I want to put two classes in one file because i think it's too spaced out lol