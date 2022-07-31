from asyncio import constants
import pygame
from Board import Board
import PygameFunctions as PF
import random as rd
from constants import *
import time
import renderConstants
from Animator import Animations
from Animator import Animation
rd.seed(10)
SELF_PLAY = True  # whether or not a human will be playing
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
    P = PF.run(GameBoard)

    if SELF_PLAY:
        if not playerMoved:
            if (GameBoard.resources[1].currentValue < 1):
                PF.displayResultScreen(False, 1)
                running = False
                continue
            if (not GameBoard.containsPerson(False)):
                PF.displayResultScreen(False, 2)
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
                    elif(type(action) == Board):
                        GameBoard = action
                        PF.reset_actions()
                        GameBoard.resources[0].currentValue = 0
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
                GameBoard = GameBoard.update()
                PF.reset_actions()

        # Computer turn
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
            if (not GameBoard.containsPerson(True)):
                PF.displayResultScreen(True, 1)
                running = False
                continue
            elif GameBoard.timeCounter > 40:
                PF.displayResultScreen(True, 2)
                running = False
                continue
            # update the board's states
            playerMoved = False
            GameBoard = GameBoard.update(False)

        # Update the display
        pygame.display.update()

    else:
        if epochs_ran % 100 == 0:
            print("Board Reset!")
            GameBoard = Original_Board  # reset environment
        for event in P:
            i = 0
            r = rd.uniform(0.0, 1.0)
            st = (rd.randint(0, GameBoard.columns - 1), rd.randint(0, GameBoard.rows - 1))
            state = GameBoard.QTable[st[1] * GameBoard.rows + st[0]]

            if r < gamma:
                while GameBoard.States[st[1]][st[0]].person is None:
                    st = (rd.randint(0, GameBoard.columns - 1), rd.randint(0, GameBoard.rows - 1))
            else:
                biggest = None
                for x in range(len(GameBoard.columns * GameBoard.rows)):
                    arr = GameBoard.QTable[x]
                    exp = sum(arr) / len(arr)
                    if biggest is None:
                        biggest = exp
                        i = x
                    elif biggest < exp and player_role == "Government":
                        biggest = exp
                        i = x
                    elif biggest > exp and player_role != "Government":
                        biggest = exp
                        i = x
                state = GameBoard.QTable[i]
            b = 0
            j = 0
            ind = 0
            for v in state:
                if v > b and player_role == "Government":
                    b = v
                    ind = j
                elif v < b and player_role != "Government":
                    b = v
                    ind = j
                j += 1
            action_to_take = ACTION_SPACE[ind]
            old_qval = b
            old_state = i

            # Update
            # Q(S, A) = Q(S, A) + alpha[R + gamma * max_a Q(S', A) - Q(S, A)]
            reward = GameBoard.act(old_state, action_to_take)
            ns = reward[1]
            NewStateAct = GameBoard.QGreedyat(ns)
            NS = GameBoard.QTable[ns][NewStateAct[0]]
            # GameBoard.QTable[i] = GameBoard.QTable[i] + alpha * (reward[0] + gamma * NS) - GameBoard.QTable[i]
            if GameBoard.num_zombies() == 0:
                print("winCase")

            take_action = []
            print("Enemy turn")
            ta = ""
            if player_role == "Government":
                r = rd.randint(0, 5)
                while r == 4:
                    r = rd.randint(0, 5)
                ta = ACTION_SPACE[r]
            else:
                r = rd.randint(0, 4)
                ta = ACTION_SPACE[r]
            poss = GameBoard.get_possible_moves(ta, "Zombie")

            if len(poss) > 0:
                r = rd.randint(0, len(poss) - 1)
                a = poss[r]
                GameBoard.actionToFunction[ta](a)
            if GameBoard.num_zombies() == GameBoard.population:
                print("loseCase")
            if event.type == pygame.QUIT:
                running = False
    