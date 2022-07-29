from ast import Pass
from Board import Board
import PygameFunctions as PF 
import numpy as np
from random import choice

actions = ['moveUp', 'moveDown','moveLeft', 'moveRight', 'heal']
#don't need pick_resource 

class Node:
    #A representation of a single board state.
    #MCTS works by constructing a tree of these Nodes.
    #Could be e.g. a chess or checkers board state.

    def __init__(self, state, parent = None ): 

        self.parent = parent #for the starter node its None
        self.children = [] #none at first
        self.state = state #GameBoard
        self.wins = 0 #initally zero for each new node
        self.visits = 0
        self.budget = 100 #how many iterations
     
    
    def uct_select_child(self):
        """Use the UCB1 formula to select a child node
            lamba c is the expression that uses the formula
           return one child node 
        """
        s = sorted(self.children, key=lambda c: c.wins / c.visits + np.sqrt(2 * np.log(self.visits) / c.visits))[-1]
        return s
    
    def get_actions(self, state):
        """
            For this node, a list of possible actions is created and returned 
            [name of action, [coord(x,y...)] ]
        """
        a_move = []
        #get_possible_moves returns a list of set(x,y)
        for i in actions: 
            a_move.append([i, state.get_possible_moves(action = i, role = 'Human')]) 
            return a_move
    
    #add_child
    def update(self, s):
         # Takes a game state, and appends it to the history.
        self.children.append(s)
    
    #simulation: 4-step process
    def run_simulation(self):
        states_copy = self.children[:]
        state = states_copy[-1]

        for t in range(self.budget):
            legal = self.get_actions(states_copy) #get a list of possible actions

            play = choice(legal) #play a random move for now 
            state = self.state.next_state(state, play) #TODO: define 
            
            winner = self.state.winner(states_copy)
            if winner: break


"""
def select(self):
        if not self.is_fully_expanded() or self.mdp.is_terminal(self.state):
            return self
        else:
            actions = list(self.children.keys())
            action = self.bandit.select(self.state, actions, self.qfunction)
            return self.get_outcome_child(action).select()
"""

"""
    We need to link the HumanAi with our board (state)
    when we call similar to make_move it theorizes the move 



    Board:
    1. start : returns a represntation of the tarting state of the game
    2. current_player: returns the current palyer's number
    3. next)state: takes the game state, and the move to be applied
        and returns the new game state
    4. legal_players(self, state_history):
        get possible moves
    5. winner return who won with numerical values; 0 if ongoing

"""