# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        " First of all we are going to calculate the distance from pacman to each ghost."
        " In addition to this, we are going to check for ghosts which are close (distance <=1) from pacman."

        nearGhosts = 0
        sumDistanceToGhosts = 1 # this can't be 1 because it is paronomastis when returning
        for ghostPosition in successorGameState.getGhostPositions():
            distance = util.manhattanDistance(newPos, ghostPosition)
            sumDistanceToGhosts += distance # this is the sum of distances from pacman to the ghosts
            if distance <= 1:
                nearGhosts += 1 # this is the number of the very near ghosts

        "Now we are going to calculate the distance to the nearest food."

        minFoodDistance = float("inf")   #setting minFoodDistance to infinty, so as every distance would be shorter than this.
        FoodList = newFood.asList() # list with foods
        for food in FoodList:   # for every food in food list
            distance = util.manhattanDistance(newPos, food) #calculating manhattan distance
            if distance <= minFoodDistance:
                minFoodDistance = distance  # we got a new minimum

        return successorGameState.getScore() + (1 / float(minFoodDistance)) - (1 / float(sumDistanceToGhosts)) - nearGhosts # returning a combination of all the above calculations
        
# return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    
    def miniMax(self, gameState, depth, agentIndex=0):
        if gameState.isWin() or gameState.isLose() or depth ==0: # We are checking whether the game is ending or the depth has been reached
            return self.evaluationFunction(gameState), None # returning current score

        numAgents = gameState.getNumAgents() # getting number of agents
        
        if agentIndex == numAgents -1: # if this is the last agent
            newDepth = depth - 1 # we are decreasing depth
        else:
            newDepth = depth
                    
        newAgentIndex = (agentIndex + 1) % numAgents

        # now we are going to create a list (ListOfActions) which will contain for each legal action all infos
        ListOfActions = [(self.miniMax(gameState.generateSuccessor(agentIndex,aState), newDepth, newAgentIndex)[0],aState) for aState in gameState.getLegalActions(agentIndex)]
        
        
        if (agentIndex != 0): # minimize for ghosts
            return min(ListOfActions) # returning action for minimum score
        else: # maximize for pacman
            return max(ListOfActions) # returning action for the maximun score
       

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        return self.miniMax(gameState, self.depth)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        totalAgents = gameState.getNumAgents()
        
        
        # using this for ghosts
        def findMin(mGameState, agentIndex, currDepth, alpha, beta):
            ghostActions = mGameState.getLegalActions(agentIndex) # get all ghost's actions
            if mGameState.isLose() or not ghostActions: # if the game is lost or there are no ghost actions
                 return self.evaluationFunction(mGameState), Directions.STOP


            bestAction = Directions.STOP
            # checking if pacman is next or not
            if agentIndex == (totalAgents - 1): # pacman is next
                pacmanSt = 1
            else: # pacman is not next
                pacmanSt = 0
            
            minCost = float("inf")
            for action in ghostActions: # for every ghost's action
                successor = mGameState.generateSuccessor(agentIndex, action) # get the successor

                if pacmanSt == 0: # if pacman is not next, we continue with next ghost
                    cost = findMin(successor,agentIndex+1, currDepth, alpha, beta)[0]
                else: # if pacman is next, we pass the score to it
                    cost = findMax(successor, currDepth+1, alpha, beta)[0]
                

                if cost < minCost:
                    minCost = cost
                    bestAction = action
                if minCost < alpha:
                    return minCost, bestAction
                beta = min(beta, minCost)

            return minCost, bestAction
                
        # using this for pacman
        def findMax(mGameState, currDepth, alpha, beta):
            pacmanActions = mGameState.getLegalActions(0)
            
            # First of all, we check whether the game is won, or the depth is reached or there are no actions for pacman. If one or more of these are true, we return score.
            if mGameState.isWin() or currDepth > self.depth or not pacmanActions:
                return self.evaluationFunction(mGameState), Directions.STOP

            bestAction = Directions.STOP
            maxCost = float("-inf")
            for action in pacmanActions:
                successor = mGameState.generateSuccessor(0, action)
                cost = findMin(successor,1,currDepth, alpha, beta)[0]
                if cost > maxCost:
                    maxCost = cost
                    bestAction = action
                if maxCost > beta:
                    return maxCost, bestAction
                alpha = max(alpha, maxCost)
            return maxCost, bestAction

        startAlpha = float("-inf")
        staerBeta = float("inf")

        return findMax(gameState, 1, startAlpha, staerBeta)[1]

        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
       
        totalAgents = gameState.getNumAgents()

        def findMin(mGameState, agentIndex, currDepth):
            ghostActions = mGameState.getLegalActions(agentIndex) # getting all legal actions of ghost
            if mGameState.isLose() or not ghostActions: # if the game has enden or there are no ghost actions
                return self.evaluationFunction(mGameState), None

            successorScore = []
            ALLsuccessors = [mGameState.generateSuccessor(agentIndex,anAction) for anAction in ghostActions]

            if agentIndex == (totalAgents - 1): # pacman is next
                pacmanSt = 1
            else: # pacman is not next
                pacmanSt = 0

            for successor in ALLsuccessors:
                if pacmanSt == 0: # if pacman is not next, we continue with next ghost
                    successorScore.append(findMin(successor, agentIndex+1, currDepth))
                else:  # if pacman is next, we pass the score to it
                    successorScore.append(findMax(successor,currDepth+1))
            
            sumScore = 0
            for score in successorScore:
                sumScore = sumScore + float(score[0])/len(successorScore)
            

            return sumScore, None
                
               
        def findMax(mGameState, currDepth):
            pacmanActions = mGameState.getLegalActions(0) # getting all pacman actions
            
            # First of all, we check whether the game is won, or the depth is reached or there are nO actions for pacman. If one or more of these are true, we return score.
            if mGameState.isWin() or currDepth > self.depth or not pacmanActions:
                return self.evaluationFunction(mGameState), None
                            
            successorScore = []
            for anAction in pacmanActions:
                successor = mGameState.generateSuccessor(0, anAction)
                successorScore.append((findMin(successor, 1, currDepth)[0], anAction))
                                    
            return max(successorScore)

        return findMax(gameState,1)[1]


def betterEvaluationFunction(currentGameState):
    """
        Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
        evaluation function (question 5).
        
        DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
   
    " First of all we are going to calculate the distance from pacman to each ghost."
    " In addition to this, we are going to check for ghosts which are close (distance <=1) from pacman."
    
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    
    nearGhosts = 0
    sumDistanceToGhosts = 1 # this can't be 1 because it is paronomastis when returning
    for ghostPosition in currentGameState.getGhostPositions():
        distance = util.manhattanDistance(newPos, ghostPosition)
        sumDistanceToGhosts += distance # this is the sum of distances from pacman to the ghosts
        if distance <= 1:
            nearGhosts += 1 # this is the number of the very near ghosts

    "Now we are going to calculate the distance to the nearest food."
        
    minFoodDistance = float("inf")   #setting minFoodDistance to infinty, so as every distance would be shorter than this.
    FoodList = newFood.asList() # list with foods
    for food in FoodList:   # for every food in food list
        distance = util.manhattanDistance(newPos, food) #calculating manhattan distance
        if distance <= minFoodDistance:
            minFoodDistance = distance  # we got a new minimum

    "And finally we are going to find the number of current capsules"
    newCapsule = currentGameState.getCapsules()
    sumCapsules = len(newCapsule)



    return (currentGameState.getScore() + (1 / float(minFoodDistance)) - (1 / float(sumDistanceToGhosts)) - nearGhosts) - sumCapsules# returning a combination of all the above calculations




# Abbreviation
better = betterEvaluationFunction

