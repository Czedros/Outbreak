from Board import Board
import PygameFunctions as PF 

actions = ['moveUp', 'moveDown','moveLeft', 'moveRight', 'heal']
#don't need pick_resource 

class Node:
    #A representation of a single board state.
    #MCTS works by constructing a tree of these Nodes.
    #Could be e.g. a chess or checkers board state.

    def __init__(self, parent = None, state = None, board = None): 
        #Human location (needs to access Board.py)
        #1 Block Radius (needs to accesss Board.py)
        self.board = board #the current Gameboard
        self.p_actions = [] #all the possible actions it can make
        self.parent = parent #for the starter node its None
        self.children = [] #none at first
        self.state = state

        #get_possible_moves returns a list of set(x,y)
        for i in actions:
            a_move = [i,Board.get_possible_moves(action = i, role = 'Human')]
            #the action, and a list of possible coordinates for that action
            self.p_actions.append(a_move)
            print(self.p_actions)
    
    def find_children(self):
        pass

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

