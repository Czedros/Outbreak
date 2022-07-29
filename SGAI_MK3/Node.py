from ast import Pass
from Board import Board
import PygameFunctions as PF 
import numpy as np
from random import choice
import datetime
#needs to be improted

actions = ['moveUp', 'moveDown','moveLeft', 'moveRight', 'heal']
#don't need pick_resource 

class Node:
    #A representation of a single board state.
    #MCTS works by constructing a tree of these Nodes.
    #Could be e.g. a chess or checkers board state.

    def __init__(self, board, parent = None ): 
        # **kwargs take in a arbitrary amount of keyword arguments

        self.parent = parent #for the starter node its None
        self.children = [] #none at first
        self.board = board #GameBoard
        self.wins = 0 #initally zero for each new node
        self.plays = 0
        self.budget = 30 #how many iterations
        # seconds = kwargs.get('time', 30) TODO: figre out what this mean 
        self.calculation_time = datetime.timedelta(seconds = 30)
     
    
    def uct_select_child(self):
        """Use the UCB1 formula to select a child node
            lamba c is the expression that uses the formula
           return one child node 
        """
        s = sorted(self.children, key=lambda c: c.wins / c.visits + np.sqrt(2 * np.log(self.visits) / c.visits))[-1]
        return s
    
    def get_actions(self, board):
        """
            For this node, a list of possible actions is created and returned 
            [name of action, [coord(x,y...)] ]
        """
        a_move = []
        #get_possible_moves returns a list of set(x,y)
        for i in actions: 
            a_move.append([i, board.get_possible_moves(action = i, role = 'Human')]) 
            return a_move
    
    #add_child
    def update(self, s):
         # Takes a game state, and appends it to the history.
        self.children.append(s)

    #play the game multiple times from this current state. this is time-based
    #Note this is different from budget, as it runs the simulations multiple times
    def get_play(self):
        """
            calls run_simulation a number of thimes until a certain amount of time has passed
        """
        begin = datetime.datetime.utcnow()
        while datetime.daetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
        
    
    #simulation: 4-step process
    def run_simulation(self):
        plays, wins = self.plays, self.wins

        visited_states = set()
        states_copy = self.children[:] #get a copy of self.children. self.children is an authoraitative record of what has happened so far in the game
        state = states_copy[-1] #get a recent state
        player = self.board.current_player(state) #TOOD: impelment current_player

        expand = True
        for t in range(1, self.budget + 1): #limits the amount of moves forward that the AI will play
            legal = self.get_actions(states_copy) #get a list of possible actions
            moves_states = [(p, self.board.next_state(state, p)) for p in legal]

            if all(plays.get((player, S)) for p, S in moves_states):
                # If we have stats on all of the legal moves here, use them
                log_total = log(
                    sum(plays[(player, S)] for p, S in moves_states))
                value, move, sate = max(
                    ((wins[(player, S)] / plays[(player, S)]) + self.C * sqrt(log_total / plays[(player, S)]), p, S)
                    for p, S in moves_states
                
                )
            else:
                #otherwise, just make an arbitrary decision
                move, state = choice(moves_states)
            states_copy.append(state)

            #'player' here and below refers to the player
            #who moved into that particular state
            if expand and (player, state) not in plays:
                expand = False
                plays[(player, state)] = 0
                wins[(player, state)] = 0
                if t < self.max_depth:
                    self.max_depth = t
            visited_states.add((player, state))

            player = self.board.current_player(state)
            winner = self.board.winner(states_copy)

            if winner: break
        for player, state in visited_states:
            if (player, state) not in plays:
                continue
            plays[(player, state)] += 1
            if player == winner:
                wins[(player, state)] +=1



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