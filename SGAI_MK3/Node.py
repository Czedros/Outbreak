from ast import Pass
from Board import Board
import PygameFunctions as PF 
import numpy as np
from random import choice
import datetime
import math
import Person 
#needs to be improted




class Node:
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

        self.parent = parent #for the starter node its None
        self.states = [] #none at first
        self.board = board #GameBoard
        self.wins = {} #initally zero for each new node
        self.plays = {}
        self.budget = 30 #how many iterations
        self.calculation_time = datetime.timedelta(seconds = 30)
        self.C = 1.4 #constant C
     
    
    def uct_select_child(self):
        """Use the UCB1 formula to select a child node
            lamba c is the expression that uses the formula
           return one child node 
        """
        s = sorted(self.states, key=lambda c: c.wins / c.visits + np.sqrt(2 * np.log(self.visits) / c.visits))[-1]
        return s
    
    
    #add_child
    def update(self, s):
         # Takes a game state, and appends it to the history.
        self.states.append(s)

    #play the game multiple times from this current state. this is time-based
    #Note this is different from budget, as it runs the simulations multiple times
    #ROLLOUT
    def get_play(self):
        """
            calls run_simulation a number of times until a certain amount of time has passed
            return the best move from it
            some debugging notes at the bottom, but the print format
            might be outdated
        """
        self.max_depth = 0
        state = self.states[-1] #current state
        player = self.board.current_player(state) #current player
        legal = self.board.get_actions(self.states[:])
    
        #No real choices bail out. or only one choice return it
        if not legal:
            return
        if len(legal) == 1:
            return legal[0]

        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
            games+=1
        
        moves_states = [(p, self.board.next_state(state, p)) for p in legal]
        #number of games and time taken
        print (games, datetime.datetime.utcnow() - begin)

        #pick the move with the highest percentage of wins
        percent_wins, move = max(
            (self.wins.get((player, S), 0) /
            self.plays.get((player, S), 1),
            p)
            for p, s in moves_states
        )
        #display the states for each possible play
        
        for x in sorted(
            ((100 * self.wins.get((player, S), 0) /
              self.plays.get((player, S), 1),
              self.wins.get((player, S), 0),
              self.plays.get((player, S), 0), p)
             for p, S in moves_states),
            reverse=True
        ):
            print(f"{3}: {0:.2f}% ({1} / {2})".format(*x))
            #i think this is python 2 format not sure if this works

        print("Maximum depth searched:", self.max_depth)

        return move #return best move


        
    
    #simulation: 4-step process
    def run_simulation(self):
        plays, wins = self.plays, self.wins

        visited_states = set()
        states_copy = self.states[:] #get a copy of self.states. it is an authoraitative record of what has happened so far in the game
        state = states_copy[-1] #get a recent state
        player = self.board.current_player(state) #Return the Person 

        expand = True
        #SELECTION
        for t in range(1, self.budget + 1): #limits the amount of moves forward that the AI will play
            legal = self.board.get_actions(states_copy) #get a list of possible actions
            moves_states = [(p, self.board.next_state(state, p)) for p in legal]
            #list of (the play, the board after the play is made). these plays are all legal

            if all(plays.get((player, S)) for p, S in moves_states):
                # If we have stats on all of the legal moves here, use them
                #TODO: implement the uct function because tf is this
                #Some info about our constant C:
                    # Larger values of C will encourage more exploration of 
                    # the possibilities, and smaller values will cause the AI
                    # to prefer concentrating on known good moves.
                log_total = math.log(
                    sum(plays[(player, S)] for p, S in moves_states))
                value, move, state = max(
                    ((wins[(player, S)] / plays[(player, S)]) + self.C * math.sqrt(log_total / plays[(player, S)]), p, S)
                    for p, S in moves_states
                )
            else:

                #otherwise, just make an arbitrary decision
                move, state = choice(moves_states)
            states_copy.append(state)

            #'player' here and below refers to the player
            #who moved into that particular state
            #EXPANSION 
            if expand and (player, state) not in self.plays: #new encountereted state
                expand = False #expanding this
                self.plays[(player, state)] = 0
                self.wins[(player, state)] = 0 #creation of new state/node
                if t < self.max_depth: 
                    self.max_depth = t #a new layer is added
            visited_states.add((player, state)) #used to update stats in backpropagation

            player = self.board.current_player(state)
            winner = self.board.winner(states_copy)

            if winner: break
        #BACKPROPAGATION
        for player, state in visited_states:
            if (player, state) not in self.plays: #unexplored don't touch!
                continue
            self.plays[(player, state)] += 1
            if player == winner:
                self.wins[(player, state)] +=1



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