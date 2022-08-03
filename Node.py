import math
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
        #Key: hash value of play
        #Value: the node
        for play in unexpandedPlays: #array of legal Plays that can be made form this node
            self.children[hash(play)] = {"play": play, "node": None}

    
    def childNode(self, play):
        """
        gets the node associated with the play
        #TODO: article in JavaScript so this has to be changed a bit 
        """
        child = self.children[play] #the parameter play in this case is already hashed
        if child["node"] is None:
            print("NOPE") #TODO: might want a debug for child that doesn't exist
        return child["node"]
    
    def expand(self, play, cState, unexpandedPlays):
        """
        expand the child node and return the new child node
        """
        #NOTICE: for the Zombie's play, it is a tuple of plays, not the Class Play
        if hash(play) not in self.children.keys():
            print("NOPE FOR EXPANSION")
        cNode = Node(self, play, cState, unexpandedPlays)
        self.children[hash(play)] = {"play" : play, "node" : cNode}
        
        return cNode
    
    def allPlays(self, bestP = False):
        """
        return all legal plays from this node
        if bestP is True: then appen the tuple of plays instead
        """
        print("allPlays is running")
        acts = []
        for child in self.children.values():
            if type(child["play"]) is tuple:
                if not bestP:
                    for p in child["play"]:
                        acts.append(p)
                else:
                    acts.append(child["play"])
            else:
                acts.append(child["play"])
        return acts

    def unexpandedPlays(self):
        """
        get all unexpanded legal plays from this node 
        """
        acts = []
        for child in self.children.values(): #returns a list of dictionaries, child represent each dic
            if child["node"] is None: #if this node is unexpanded
                if type(child["play"]) is tuple : #all the plays for the zombies ais
                    for p in child["play"]:
                        acts.append(p) #append EVERY play
                else:
                    acts.append(child["play"])
        return acts

    def isFullyExpanded(self):
        """
        return whether this node is fully expanded
        """
        for child in self.children.values():
            if child["node"] is None: return False
        return True 

    def isLeaf(self):
        """
        is this node terminal in game tree
        this is not apart of the case where the player wins
        """
        return len(self.children) == 0

    def getUCB1(self, c):
        """
        get the ucb1 value of this node
        """
        return (self.wins / self.plays) + math.sqrt(c * math.log(self.parent.plays) / self.plays)

            