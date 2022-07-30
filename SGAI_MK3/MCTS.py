from ast import Pass
from Board import Board
import PygameFunctions as PF 
import numpy as np
from random import choice
import datetime
import math
import Person 
#needs to be improted

#reward for each action (pick up resources or something)
#state is a board #TODO: create a GameBoard Class 


class MCTS:
    #A representation of a single board state.
    #MCTS works by constructing a tree of these Nodes.
    #Could be e.g. a chess or checkers board state.
    """
        A Node holds a board, its parent, list of children (states), number of plays
        and visits.

        list of states are really different boards that represnt different states of the game
    """

    def __init__(self, board: Board, parent = None ): 
        # **kwargs take in a arbitrary amount of keyword arguments
        pass



"""
    We need to link the HumanAi with our board (state)
    when we call similar to make_move it theorizes the move 



    Board:
    1. start : returns a represntation of the starting state of the game
    2. current_player: returns the current palyer's number
    3. next)state: takes the game state, and the move to be applied
        and returns the new game state
    4. legal_players(self, state_history):
        get possible moves
    5. winner return who won with numerical values; 0 if ongoing

"""