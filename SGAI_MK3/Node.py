
class Node:
    #A representation of a single board state.
    #MCTS works by constructing a tree of these Nodes.
    #Could be e.g. a chess or checkers board state.

    def __init__(self, location, one_block_radius): 
        #Human location (needs to access Board.py)
        #1 Block Radius (needs to accesss Board.py)
        self.state, action, children, parent
    
    def find_children(self):
        pass

    def randon_children(self):
        pass
    
    def is_terminal(self):
        pass

    def reward(self):
        pass
    #maybe hashable function
    #maybe compareTo function

