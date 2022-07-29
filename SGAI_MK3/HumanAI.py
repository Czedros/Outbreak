##HumanAI.py 
# Defintion:
# Monte-Carlo Tree Search is a planning algorithm that accumulates value estimates obtained from Monte Carlo simulations in order to successively direct
# simulations towards more highly-rewarded trajectories. We execute MCTS after encountering each new state to select an agent's action for that state: it is executed again to select the action for the next state. Each execution is an iterative process that simulates many trajectories starting from the current state to the terminal state. The core idea is to successively focus 
# multiple simulations starting at the current state by extending the initial portions of trajectories that have received high evaluations 
# from earlier simulations

#selection, expansion, simulation, back propogation 

import random as rd
class Engine():
    role = ""
    gamma = 0
    alpha = 0
    epsilon = 0
    budget = 0
    QTable = []
    rand = False
    ACTION_SPACE = ["moveUp","moveDown","moveLeft","moveRight","heal","bite"]
    '''
    Role is either Government or Zombie
    Budget = how far your ML model thinks ahead- mainly used for Monte Carlo Tree Search but can be applied
    to other areas
    QTable = given your model- remove if not q-learning
    '''
    def __init__(self,r,b,learning,BoardSize, ra) -> None:
        self.role = r
        self.budget = b
        self.gamma = learning[0]
        self.alpha = learning[1]
        self.epsilon = learning[2]
        self.rand = ra
        
        
        self.QTable = [0] * BoardSize #change this  
        #Board size is totalrows*totalcolumns. Remove if not QTable
        pass
    def think(self,GameBoard): #redefine for MonteCarlo Tree Search 
        '''
        This is where you put your ML Function
        Returns array with [action, coordinate, reward]
        '''
        i = 0
        r = rd.uniform(0.0, 1.0)
        st = rd.randint(0, len(GameBoard.States) - 1)
        state = self.QTable[st]
        if r < self.gamma or self.rand:
            while GameBoard.States[st].person is None:
                st = rd.randint(0, len(GameBoard.States) - 1)
            #Random values onto Q Table - replace it with not just randominess 
        else:
            biggest = None #Biggest Reward
            for x in range(len(GameBoard.States)):
                arr = self.QTable[x]
                exp = sum(arr) / len(arr)
                if biggest is None:
                    biggest = exp
                    i = x
                elif biggest < exp and self.role == "Government":
                    biggest = exp
                    i = x
                elif biggest > exp and self.role != "Government":
                    biggest = exp
                    i = x
                    state = self.QTable[i]
                    b = 0
                    j = 0
                    ind = 0
                for v in state:
                    if v > b and self.role == "Government":
                        b = v
                        ind = j
                    elif v < b and self.role != "Government":
                        b = v
                        ind = j
                    j += 1
                action_to_take = self.ACTION_SPACE[ind]
                old_qval = b
                old_state = i
            
            return [action_to_take, old_state, old_qval]

    #Not needed              
    def update_q_table(self,NewBoard, action_info):
        # action_info: exactly what is returned in think function with reward and nextstate qvalue at the end * 
        idx = self.ACTION_SPACE.index(action_info[0])
        self.QTable[action_info[1]][idx] = self.QTable[action_info[1]][idx] + self.alpha * (action_info[3] + self.gamma * action_info[4]) -  self.QTable[action_info[1]][idx]
        # GameBoard.QTable[i] = GameBoard.QTable[i] + alpha * (reward[0] + gamma * NS) - GameBoard.QTable[i]

"""
Pseudo Code for MCTS 

def _select(self, node):
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            TODO: rework variable children in Node class
            if node not in self.children or not self.children[node]: 
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys() #the number children of that node - all of the nodes recorded
            if unexplored:
                n = unexplored.pop() #pick the latest node
                path.append(n) #add it to our path 
                return path
            node = self._uct_select(node)  # descend a layer deeper

#run this many times 
def simulate (self, node):
    while(turns not ended):
        reward = node.reward() #calculate rewarad based on how long it survived and people saved
        return node.find_random_child() or node 

TODO: Understand UCT Equation and tweak it 
def _uct_select(self, node):
    #all children are expanded
    assert all(n in self.children for n in self.children[node])
    
"""







"""
def _backpropagate(self, path, reward):
        "Send the reward back up to the ancestors of the leaf"
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa
"""

"""
MCTS: 
# main function for the Monte Carlo Tree Search
#the starting parameter is the human's first position? root = human first position
  def monte_carlo_tree_search(root):
     
    while resources_left(time, computational power):
        
        leaf = traverse(root) #SELECTION: returns a node with the most promise to explore
        simulation_result = rollout(leaf) #EXPANSION and SIMULATION  
        backpropagate(leaf, simulation_result)#BACKPROPAGATION it 
         
    return best_child(root)
 
# function for node traversal
def traverse(node):
    while fully_expanded(node): #until reach a leaf node
        node = best_uct(node) # UCT chose best node
         
    # in case no children are present  / node is terminal just pick another unvisited node and try again
    return pick_unvisited(node.children) or node  
 
# function for the result of the simulation
#multiple simulations are 'rolled out'
def rollout(node):
    while non_terminal(node): #while not terminal
        node = rollout_policy(node) #pick a random child from that node
    return result(node) #return terminal node
 
# function for randomly selecting a child node
def rollout_policy(node):
    return pick_random(node.children)
 
# function for backpropagation; easiest to understand 
def backpropagate(node, result):
    if is_root(node) return #base case 
    node.stats = update_stats(node, result) #at this node, update it based on our results
    backpropagate(node.parent) #go backwards to its parent thats all
 
# function for selecting the best child
# node with highest number of visits 
def best_child(node):
    pick child with highest number of visits
"""