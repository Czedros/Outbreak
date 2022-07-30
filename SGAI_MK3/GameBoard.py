import pygame
import PygameFunctions as PF
import Board

class GameBoard:
    #return the initial game state (TBC)
    def start(self):
        """
        13x13 grid
        """
        pass

    def next_state(self, state, play):
        """
        advance the given state and return the new state
        """
        pass
    def legal_plays(self, state):
        """
         return the current player's legal moves from given state
        """
        pass 
    def winner(self,state):
        """
        return winner 1: human -1: zombie 0: ongoing

        """
        pass
    
        


"""

    
    def get_actions(self, states_history):
        """
        For this node, a list of possible actions is created and returned 
        [name of action, [coord(x,y...)] ]

        states_history: the history of full list of games history
        """
        a_move = []
        actions = ['moveUp', 'moveDown','moveLeft', 'moveRight', 'heal']
        #get_possible_moves returns a list of set(x,y)
        for i in actions: 
            a_move.append([i, states_history.get_possible_moves(action = i, role = 'Human')]) 
        print(a_move)
        return a_move
    def winner(self, state_history):
        """
        takes a sequence of game states representing the full game history
        if the game is now over and human won, return the player number
        if the game is still ongoing, return zero
        if the game is tied, return a different distinct value

        """
        state = state_history[-1] #recent node
        if state.board.num_zombies() == 0:
            print("won")
            return board.current_player(state) #won
        elif state.board.num_zombies() == state.board.population():
            print("lost")
            return -1
        else:
            print("Still ongoing")
            return 0

    def current_player(self, state):
        """
        return players current number based on game state
        player's current number is the last element in state, hence [-1]
        (UNFINISHED)
        """
        return state[-1]
"""