from ast import Pass
from random import choice
import datetime
import copy
from Node import Node
import time
import PygameFunctions as PF
import sys
import pygame
class MCTS:

    """
        represents the search tree
    """

    def __init__(self, board, c = 2): 
        # **kwargs take in a arbitrary amount of keyword arguments
        self.board = board 
        self.c = c
        self.nodes = {} # key: hashed version of state, value: the node 
        
    def makeNode(self, state):
        """
        if given state does not exist, create dangling node
        """
        print("MAKENODE")
        if self.nodes.get(hash(state)) is None:
            print("MAKENODE: LEGALPLAYS") 
            unexpandedPlays = tuple(copy.copy(self.board.legal_plays(state))) #return a tuple
            node = Node(None, None, state, unexpandedPlays)
            self.nodes[hash(state)] = node
    def runSearch(self, state):
        """
        runs the entire 4-step process in a set amount of time
        """
        print("RUNSEARCH MAKENODE")
        self.makeNode(state)
        self.calculation_time = datetime.timedelta(seconds = 60) #time taken to to do entire 4 step process
        
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            print("RUNSEARCH SELECTION STARTING")
            node = self.select(state) #SELECTION: existing info repeadetly choose successive child node down to end of search tree
            winned = self.board.winner(node.state)
            if node.isLeaf() == False and winned is None :
                print("RUNSEARCH EXPANSION")
                node = self.expand(node) #EXPANSION: seach tree is expanded by adding a node
                print("RUNSEARCH SIMULATION")
                ##self.visualize(node.state)
                winned = self.simulate(node) #SIMULATION: run the game starting form the added node to determine the winner
            print("Winner found-->", winned, "or reached a leaf", node.isLeaf(), "RUNSEARCH BACKPROPAGATION")
            self.back(node, winned) #BACKPROPAGATION: All the nodes in the selected path are updated with new info from simulation

    def bestPlay(self, state):
        """
        Get the best move from available stats
        """
        self.makeNode(state)
        print("state expanded? ", self.nodes[hash(state)].isFullyExpanded())
        #if not self.nodes[hash(state)].isFullyExpanded():
        
        node = self.nodes[hash(state)]
        bPlay = None
        max = float('-inf')

        if state.isPlayer(1):
            allPlays = node.allPlays()
            for play in allPlays:
                cNode = node.childNode(hash(play))
                if cNode is None: 
                    print("this shouldn't run all the time")
                    continue 
                if ( cNode.wins / cNode.plays )>max:
                    bPlay = play
                    max = cNode.wins / cNode.plays 
        else:
            allPlays = node.allPlays(bestP = True)
            cNode = node.childNode(hash(allPlays))
            if cNode is None:
                print("this should be running at all for the zombie ruhoh")
            bPlay = allPlays
            max = cNode.wins / cNode.plays
        print("max wr: ", max)
        print("bestPlay ran with any errors somehow")
        return bPlay 

    def select(self, state):
        """
        MCTS Selection Phase
        1. until not fully expanded 
        2. until Leaf 
        """
        print("SELECTION")
        node = self.nodes[hash(state)]
        while node.isFullyExpanded() and not node.isLeaf():
            print("IF EXPANDED AND NOT TERMINAL")
            if node.state.isPlayer(1):
                plays = node.allPlays() #If true: return tuple of plays for zombie
                bPlay = None
                bUCB1 = float('-inf') #negative infinity
                for play in plays:
                    cUCB1 = node.children[hash(play)]["node"].getUCB1(self.c) 
                    if cUCB1 > bUCB1: #process of pickng the best child 
                        bPlay = hash(play)
                        bUCB1 = cUCB1
                node = node.childNode(bPlay)
            else:
                plays = node.allPlays(True)
                node = node.childNode(hash(plays))
        return node #return the best child slay

    def expand(self, node : Node):
        """
        MCTS Expansion Phase
        expand a unexpanded child node. 
        player: will be random
        zombie: all unexpandedPlays are expanded in one state 
        """
        print("EXPANSION")
        plays = node.unexpandedPlays()
        play_h_or_z = None
        if node.state.isPlayer(1): #if human, only do 1 random play
            play_h_or_z = choice(plays) #random unexpanded child node
            print("human expanded")
        else:
            play_h_or_z = tuple(plays) #all plays are considered
            print("zombie expanded")

        print("EXPANSION NEXT_STATE")
        cState = self.board.next_state(node.state, play_h_or_z ) # play the next state and return it
        print("EXPANSION LEGAL_PLAYS")
        cUnexpandedPlays = tuple(self.board.legal_plays(cState)) #find all the legal_plays for this new child State
        print("EXPANSION Node expand")
        cNode = node.expand(play_h_or_z, cState, cUnexpandedPlays) #expand the child node and return it
        self.nodes[hash(cState)] = cNode #add it to our dict of nodes hahahahah
        
        return cNode

    def simulate(self, node : Node):
        """
        MCTS Simulation Phase
        Play game to terminal state, return winner
        Note no new nodes are stored in this process! 
        """
        print("SIMULATION")
        state = node.state 
        winned = self.board.winner(state)
        while winned == None: #while the game continues 
            print("a new iteration of simulation")
            print("SIMULATION legal_plays")
            plays = self.board.legal_plays(state)
            print("after simulation legal plays winCounter", state.board.timeCounter)
            
            if state.isPlayer(1):
                play = choice(plays) 
                print("SIMULATION next_state for human")
                state = self.board.next_state(state, play)
                print("IN SIMULATION FOR PLAYER AFTER NEXT_STATE the timecounter is", state.board.timeCounter)
            else:
                playList = plays
                print("SIMULATION next_state for zombie")
                state = self.board.next_state(state, playList)
                print("IN SIMULATION FOR PLAYER AFTER NEXT_STATE the timecounter is", state.board.timeCounter)
            print("SIMULATION find winner")
            winned = self.board.winner(state)
            print("The winner is... -->", winned)
            ##self.visualize(state)
        return winned

    def back(self, node, winner):
        """
        MCTS Backpropagation Phase I can never spell this correctly
        Update ancestor node with new hot stats
        """
        print("backpropagation")
        while node is not None:
            node.plays += 1
            if node.state.isPlayer(-winner): #Parent node wins are updaed
                node.wins += 1 
            node = node.parent
    
    def stats(self, state):
        """
        for the node for this state check out its stats
        # plays, # wins, all children
        """
        node = self.nodes[hash(state)]
        stats = [ {"plays" : node.plays},
                  {"wins" : node.wins},
                  ['children',]
                ]
        for child in node.children.values():
            if state.isPlayer(1):
                if child["node"] is None:
                    stats[2].append((child["play"].Zmove, None, None))
                    
                else:
                    stats[2].append( (child["play"].Zmove, child["node"].plays, child["node"].wins))
            else:   
                zombiePlays = []
                if type(child["play"]) != tuple:
                    zombiePlays = child["play"].Zmove
                else:
                    for p in child["play"]:
                        zombiePlays.append(p.Zmove)
                    zombiePlays = tuple(zombiePlays)
                if child["node"] is None:
                    stats[2].append((zombiePlays, None, None))
                else:
                    stats[2].append((zombiePlays, child["node"].plays, child["node"].wins))

        return stats

    def visualize(self, state):
        #AI Visualization, comment out to remove and speed up (meant for debugging)
        st = time.process_time()
        while(time.process_time() - st < 0.5):
            P = PF.run(state.board)
            for event in P:
                if event.type == pygame.QUIT:
                    sys.exit()
        ############


    #Errors: 
    # creating Hashes
    # getting legalMoves for zombie
