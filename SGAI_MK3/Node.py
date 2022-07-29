from Board import Board
import PygameFunctions as PF 
import numpy as np

actions = ['moveUp', 'moveDown','moveLeft', 'moveRight', 'heal']
#don't need pick_resource 

class Node:
    #A representation of a single board state.
    #MCTS works by constructing a tree of these Nodes.
    #Could be e.g. a chess or checkers board state.

    def __init__(self, parent = None, state = None): 
        #Not sure about board
        self.p_actions = self.get_actions() #all the possible actions it can make
        self.parent = parent #for the starter node its None
        self.children = [] #none at first
        self.state = state #GameBoard
        self.wins = 0
        self.visits = 0
     
    
    def uct_select_child(self):
        """Use the UCB1 formula to select a child node
            lamba c is the expression that uses the formula
           return one child node 
        """
        s = sorted(self.children, key=lambda c: c.wins / c.visits + np.sqrt(2 * np.log(self.visits) / c.visits))[-1]
        return s
    
    def get_actions(self):
        """
            For this node, a list of possible actions is created and returned 
            [name of action, [coord(x,y...)] ]
        """
        a_move = []
        #get_possible_moves returns a list of set(x,y)
        for i in actions: 
            a_move.append([i,Board.get_possible_moves(action = i, role = 'Human')]) 
            return a_move
    
    def find_children(self): 
        #TODO: think about AP system later
        
        
    def randon_children(self):
        #random successor of this board state 
        pass
    
    def is_terminal(self):
        #return True if the node has no children
        return self.children == None

    def reward(self):
        pass
    #maybe hashable function
    #maybe compareTo function

