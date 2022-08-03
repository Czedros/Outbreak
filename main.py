from asyncio import constants
import pygame
from Board import Board
import PygameFunctions as PF
import random as rd
from constants import *
import time
import renderConstants
from MCTS import MCTS
from Animator import Animations
from Animator import Animation
import datetime
SELF_PLAY = False  # whether or not a human will be playing
player_role = "Government"  # Valid options are "Government" and "Zombie"
# Create the game board
GameBoard = Board((ROWS, COLUMNS), player_role)
GameBoard.populate()
# Self play variables
alpha = 0.1
gamma = 0.6
epsilon = 0.1
epochs = 1000
epochs_ran = 0
Original_Board = GameBoard.clone(GameBoard.States, GameBoard.player_role)

# Initialize variables
running = True
take_action = []
playerMoved = False
while running:
    if SELF_PLAY:
        P = PF.run(GameBoard)
        if not playerMoved:
            if GameBoard.resources[1].currentValue < 1:
                print("")
                print("****************You lost!****************")
                print("Resources Remaining:", GameBoard.resources[1].currentValue)
                print("People Saved:", GameBoard.resources[2].currentValue)
                print("Days Survived:", GameBoard.timeCounter)
                print("")
                PF.dataWrite("dataCollectionPlayer.csv", [GameBoard.resources[1].currentValue, GameBoard.resources[2].currentValue, GameBoard.timeCounter, 'lose', "Starvation"])
                PF.displayResultScreen(False)
                running = False
                
            elif (not GameBoard.containsPerson(False)):
                print("")
                print("****************You lost!****************")
                print("Resources Remaining:", GameBoard.resources[1].currentValue)
                print("People Saved:", GameBoard.resources[2].currentValue)
                print("Days Survived:", GameBoard.timeCounter)
                print("")
                PF.dataWrite("dataCollectionPlayer.csv", [GameBoard.resources[1].currentValue, GameBoard.resources[2].currentValue, GameBoard.timeCounter, 'lose', "Infection"])
                PF.displayResultScreen(False)
                running = False

                continue
            # Event Handling
            finished = False
            for event in P:
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    action = PF.get_action(GameBoard, x, y)
                    if(action == "finish"):
                        finished = True
                        break
                if event.type == pygame.QUIT:
                    running = False


            # Action handling
            if finished:
                moveMult = 0
                for i in range(PF.actionSlot + 1):
                    if(PF.actions[i].actionType == PF.ActionTypes.move.value):
                        moveMult += 1
                        GameBoard.pickup(PF.actions[i].coord2)
                for i in range(PF.actionSlot + 1):
                    act = PF.actions[i]
                    if(act.actionType == PF.ActionTypes.heal.value):
                        GameBoard.heal(act.coord, infRange=True)
                if(moveMult != 0):
                    GameBoard.move(PF.firstActor, PF.selectedActor, mult= moveMult)
                #elif take_action[0] == "heal" or take_action[0] == "bite":
                #    result = GameBoard.actionToFunction[take_action[0]](take_action[1])
                #    if result[0] is not False:
                #        playerMoved = True
                #        print("Cure, Vaccinate, or Infect either failed or succeeded, action completed successfully in Main")
                #    take_action = []
                playerMoved = True
                GameBoard.update()
                PF.reset_actions()

        # AI running
        else:
            #Hi I think the issue is that all the zombie ai have the same ID!
            #I print the ID and new are all the same 
            #When you first intilalize the board, I think that's when you
            #created a new ZombieAi. So I think is Board.populate
            zombies = []
            moves = []
            for arr in GameBoard.States:
                for state in arr:
                    if state.person is not None and state.person.isZombie == True:
                        tup = (state.person, state.person.ai.ID) 
                        print(tup)
                        zombies.append(tup)
                        #zombies.append(state.person)
                        #zombies.append(state.person.ai.ID) #class State -> class Person -> class ZombieAi
            for zomb, id in zombies:
                #this part is confusing? but idk lol - Hannah
                moves.append(zomb.ai.performAction(GameBoard))
                #print("performaction")
            for x in range(len(zombies)):
                currentZom = zombies[x][0] #returns a Person
                Action = moves[x]
                if Action[0] == 'move':
                    GameBoard.move(currentZom.ai.position, Action[1])     
                else:
                    GameBoard.bite(Action[1])

            # Implement the selected action

            # update the board's states
            playerMoved = False
            GameBoard.update(False)

        # Update the display
        pygame.display.update()

    else:
        #TODO: implement HUMAN_AI
        #Create the MCTS
        mcts = MCTS(GameBoard)
        state = GameBoard.start() #Return State_MC
        winned = GameBoard.winner(state)
        while winned is None:
            P = PF.run(GameBoard)
            print("player position before", state.board.findPlayer())
            print("Running MCTS")
            mcts.runSearch(state) #TODO: make the MCTS know to make a move for player
            print("Getting stats")
            stats = mcts.stats(state) #States about this search on this state
            print(stats)
            print("Getting best play")
            play = mcts.bestPlay(state) #get the best play
            if state.isPlayer(1):
                print("Play's row:", play.row, "Play's col", play.col, "and move", play.Zmove)
            else:
                for p in play:
                    print("Play's row:", p.row, "Play's col", p.col, "and move", p.Zmove)
            #Go to next state
            print("player position before", state.board.findPlayer())
            print("Next State")
            state = GameBoard.next_state(state, play)
            winned = GameBoard.winner(state)
            print("player position after", state.board.findPlayer())
            GameBoard.update()
            pygame.display.update()
            #break #ADDED TO TEST ONE ITERATION
        running = False
        