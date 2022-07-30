import GameBoard
class Node:
    """
    Node is the statistical information gained from these simulations 
    """
    def __init__(self, parent, play, state, unexpandedPlays):
        self.play = play #The move made from the parent to get to this node 
        self.state = state #the game GameBoard associated with this node

        self.plays = 0
        self.wins = 0

        self.parent = parent #parent Node
        self.children = {}
        for play in unexpandedPlays: #array of legal Plays that can be made form this node
            self.children[hash(play)] = (play, None)
    
    def expand(self, play, childState, unexpandedPlays):
        """
        expand the child node and return the new child node
        """
        pass
    
    def allPlays(self):
        """
        return all legal plays from this node
        """
        pass

    def unexpandedPlays(self):
        """
        get all unexpanded legal plays from this node 
        """
        pass

    def isFullyExpanded(self):
        """
        return whether this node is fully expanded
        """
        pass

    def isLeaf(self):
        """
        is this node terminal in game tree
        this is not apart of the case where the player wins
        """
        pass
    def getUCB1(self, c):
        """
        get the ucb1 value of this node
        """
        pass

            