# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]



def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    Visited = []                # we are creating an empty list, wchich keeps visited nodes
    frontier = util.Stack()     # we are creting an empty stack
    parentNode = dict()         # creating a dictionary to connect nodes with their parents
    
    startState = problem.getStartState(), []    # startState contains state and path
    frontier.push(startState)        # we are pushing start on the top of the stack
   
    
    while not frontier.isEmpty():   #while the stack is not empty
        node = frontier.pop()       # pops the node on the top of the stack
        Visited.append(node[0])     # adding node to the list with the visited nodes
    
        if problem.isGoalState(node[0]):    # in case we found our goal
            tempNode = node
            Path = []               # this will keep the path to the goal
            while tempNode is not startState:    # iterate through the nodes from end to stasrt
                Path.append(tempNode)   #add node to path
                tempNode = parentNode[tempNode] # tempnode is now its parent
            return [p[1] for p in reversed(Path)] # returning the path # using reversed to show the moves from start to end


        for successor in problem.getSuccessors(node[0]): # for every successor of the current node
            if successor[0] not in Visited:             # check if the successor is not
                frontier.push(successor)                # if it is unvisited, push it to the stack
                parentNode[successor] = node            # save the parent node he came from
                    
    return []
        
    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    
    startSate = problem.getStartState(),[]      # getting starting node
    if problem.isGoalState(startSate[0]):       # check if starting node is a goal
        return []
    
    frontier = util.Queue()             # creating a queue
    frontier.push(startSate)            # pushing starting node inside queue

    Visited= []                         # creating a list of all visited nodes

    while not frontier.isEmpty():       # while the queue is not empty
        tempNode = frontier.pop()       # pop the first node of the queue
        if tempNode[0] not in Visited:  # if the poped node is unvisited
            Visited.append(tempNode[0]) # add node to the list of visited nodes
        
            if problem.isGoalState(tempNode[0]):    # check if node is a goal-node
                return tempNode[1]
            
            for successor in problem.getSuccessors(tempNode[0]):    # for every successor of node
                path = tempNode[1]
                path = path + [successor[1]]        # path is the path of parent node + path to successor
                frontier.push((successor[0],path))  # push succesor at the end of the queue

    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    
    
    frontier = util.PriorityQueue()                 # creating a priority queue
    startState = problem.getStartState(),[], 0      # getting first
    
    Visited = []             # creating a list with all visited nodes
    
    cost = startState[2]     # code of starting node
    frontier.push(startState,cost)      # pushing node inside priority queue based on cost
    
    while not frontier.isEmpty():   # while priority queue is not empty

        tempNode = frontier.pop()   # pop node from the start of priority queue
        if problem.isGoalState(tempNode[0]):    # if we reached the goal-node
            return tempNode[1]

        if tempNode[0] not in Visited:
                Visited.append(tempNode[0])
                tempCost = tempNode[2]
                for successor in problem.getSuccessors(tempNode[0]):
                    path = tempNode[1]
                    path = path + [successor[1]]
                    cost = tempCost
                    cost += successor[2]
                    frontier.push((successor[0], path, cost) ,cost)
    return []

                              # util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    frontier = util.PriorityQueue()           # creating a priority queue
    startState = problem.getStartState(), [],0     # getting start state
    Visited = []        # creating a list of visited nodes
    
    state = startState[0]       # state of starting state
    cost = startState[2]        # cost of starting state
    
    heuristicValue = heuristic(state,problem)   # calculating heuristic value for staring state
    costWithHeuristic = heuristicValue + cost   # adding heusristc value to cost
    frontier.push(startState,costWithHeuristic) # pushing startStare inside priority queue based on cost with heuristic value
    
    while not frontier.isEmpty():       # while priority queue is not empty
        tempNode = frontier.pop()           # pop the first node of priority queue
        if problem.isGoalState(tempNode[0]):    # check if the node is goal
            return tempNode[1]

        if tempNode[0] not in Visited:      # if we hadn't visited node yet
            Visited.append(tempNode[0]) # add node to the list of visited
            tempCost = tempNode[2]
            for successor in problem.getSuccessors(tempNode[0]):    # for every successor of node
                path = tempNode[1]
                path = path + [successor[1]]
                cost = tempCost
                cost += successor[2]        # cost is cost of ancestor + cost of successor
                costWithHeuristic = heuristic(successor[0],problem) + cost # adding heuristc value to cost
                frontier.push((successor[0], path, cost), costWithHeuristic) # pushing successor and its cost with heuristic value in the priority queue
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
