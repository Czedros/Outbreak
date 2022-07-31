from ast import Pass
from random import choice
import datetime
import copy
import Node

class MCTS:

    """
        represents the search tree
    """

    def __init__(self, board, c = 2): 
        # **kwargs take in a arbitrary amount of keyword arguments
        self.board = board 
        self.c = self.c
        self.nodes = {} # TODO: need hashable states. get you any node given its state
        
    def makeNode(self, state):
        """
        if given state does not exist, create root node
        """
        if(self.nodes[hash(state)] == None):
            unexpandedPlays = copy(self.board.legal_plays(state))
            node = Node(None, None, state, unexpandedPlays)
            self.nodes[hash(state), node]
    def runSearch(self,state):
        self.makeNode(state)
        self.calculation_time = datetime.timedelta(seconds = 30) #time taken to to do entire 4 step process
        
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            node = self.select(state) #SELECTION: existing info repeadetly choose successive child node down to end of search tree
            winner = self.board.winner(node.state)

            if(node.isLeaf() == False and winner == None):
                node = self.expand(node) #EXPANSION: seach tree is expanded by adding a node
                winner = self.simulate(node) #SIMULATION: run the game starting form the added node to determine the winner
            self.back(node, winner) #BACKPROPAGATION: All the nodes in the selected path are updated with new info from simulation

    def bestPlay(self, state):
        """
        Get the best move from available stats
        """
        self.makeNode(state)
        if not self.nodes[hash[state]].isFullyExpanded():
            raise("Not enough information to make bestPlay")
        
        node = self.nodes[hash(state)]
        allPlays = node.allPlays()
        bPlay = None
        max = float(-'inf')
        for play in allPlays:
            cNode = node.children[play]
            if cNode.plays>max:
                bPlay = play
                max = cNode.plays #can TODO: change finding max to highest win rate wins/plays
        return bPlay 

    def select(self, state):
        """
        MCTS Selection Phase
        1. until not fully expanded 
        2. until Leaf 
        """
        node = self.nodes[hash(state)]
        while(node.isFullyExpanded() and not node.isLeaf()):
            plays = node.allPlays()
            bPlay = None
            bUCB1 = float('-inf') #this is like java version of like Integer.MIN_VALUE... but python can do -infinity damn

            for play in plays:
                cUCB1 = node.children[play].getUCB1(self.c) 
                if cUCB1 > bUCB1: #process of pickng the best child 
                    bPlay = play
                    bUCB1 = cUCB1
            node = node.children[bPlay] 
        return node #return the best child slay

    def expand(self, node : Node):
        """
        MCTS Expansion Phase
        expand a unexpanded child node. will be random
        """
        plays = node.unexpandedPlays()
        play = choice(plays) #random unexpanded child node

        #c for child!
        cState = self.board.nextState(node.state, play) #play the next state and return it
        cUnexpandedPlays = self.board.legalPlays(cState) #find all the unexpandedplays for this new child State
        cNode = node.expand(play, cState, cUnexpandedPlays) #expand the child node and return it
        self.nodes[hash(cState), cNode] #add it to our dict of nodes hahahahah

        return cNode

    def simulate(self, node : Node):
        """
        MCTS Simulation Phase
        Play game to terminal state, return winner
        Note no new nodes are stored in this process! 
        """
        state = node.state 
        winner = self.board.winner(state)
        while not winner: #while the game continues 
            plays = self.board.legalPlays(state)
            play = choice(plays) #pick a random legal Play
            state = self.board.nextState(state, play)
            winner = self.board.winner(state)
        return winner

    def back(self, node, winner):
        """
        MCTS Backpropagation Phase I can never spell this correctly
        Update ancestor node with new hot stats
        """
        while node != None:
            node.plays +=1
            if(node.state.isPlayer(-winner)): #TODO: add isPlayer method 
                node.wins +=1
            node = node.parent
    def stats(self, state):
        node = self.nodes[hash(state)]
        stats = [ node.plays,
                  node.wins,
                  ['children:' ]
                ]
        for child in node.children.values():
            if child.node == None:
                stats[2].append((child.play, None, None))
            else:
                stats[2].append((child.play, child.plays, child.n_wins))
        return stats