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


import random

import util
from game import Agent, Directions
from util import manhattanDistance


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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states/north/south/east/wert
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [
            index for index in range(len(scores)) if scores[index] == bestScore
        ]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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

        #newCapsules = successorGameState.getCapsules()
        #currentCapsules = currentGameState.getCapsules()

        "*** YOUR CODE HERE ***"
        foodList = newFood.asList()
        Fdistances = []
        scaredGhosts = []
        dangerousGhosts =[]
        foodWeight = 3
        scaredWeight = 2
        dangerousWeight = 4
        dangerThreshold = 5
        score = 0

        for foodPosition in foodList:
            distance = manhattanDistance(newPos, foodPosition)
            Fdistances.append(distance)
            

        for ghost in newGhostStates:
            ghostPosition = ghost.getPosition()
            distance = manhattanDistance(newPos, ghostPosition)

            if ghost.scaredTimer > 0:
                scaredGhosts.append(distance)
            else:
                dangerousGhosts.append(distance)

        
        
        if len(Fdistances) > 0:
            closestFood = min(Fdistances)
        else:
             closestFood = None

        if len(scaredGhosts) > 0:
            closestScaredGhost = min(scaredGhosts)
        else:
            closestScaredGhost = None

        if len(dangerousGhosts) > 0:
            closestDangerousGhost = min(dangerousGhosts)
        else:
            closestDangerousGhost = None

           
        if closestFood is not None:
            score += foodWeight / (closestFood + 1)

        if closestScaredGhost is not None:
            score += -closestScaredGhost * scaredWeight

        if closestDangerousGhost is not None:
            #score += closestDangerousGhost * dangerousWeight
            if closestDangerousGhost <= dangerThreshold and closestDangerousGhost > 0:
                penalty = -dangerousWeight/closestDangerousGhost
                score += penalty

        #if action == Directions.STOP:
        #    score -= 10

        #if len(newCapsules) < len(currentCapsules):
        #    score += 50

        return successorGameState.getScore() + score

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
        return successorGameState.getScore()


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

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        
        def minimax(gameState, agentIndex, depth):

            #stop searching when game ends or at max depth
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
        
            legalActions = gameState.getLegalActions(agentIndex)

            if not legalActions:
                return self.evaluationFunction(gameState)

            #setting score to either max or min
            if agentIndex == 0:
                bestScore = float('-inf')
            else:
                bestScore = float('inf')

            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)

                #finding next agent
                nextAgent = (agentIndex + 1) % gameState.getNumAgents()

                #increase depth after all agent made thier move
                if nextAgent == 0:
                    nextDepth = depth +1
                else:
                    nextDepth = depth

                #recurs for successor
                value = minimax(successor, nextAgent, nextDepth)

                #Pacman
                if agentIndex == 0:
                    bestScore = max(bestScore, value)
                #Ghosts
                else:
                    bestScore = min(bestScore, value)

            return bestScore
        #pacman's turn
        legalActions = gameState.getLegalActions(0)

        bestScore = float('-inf')
        bestAction = None

        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)

            #first ghost moves
            score = minimax(successor, 1, 0)

            if score > bestScore:
                bestScore = score
                bestAction = action

        return bestAction
        #util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphaBeta(state, turn_index, alpha, beta):
            agent_index = turn_index % gameState.getNumAgents()
            current_depth = turn_index // state.getNumAgents()

            if state.isWin() or state.isLose() or current_depth == self.depth:
                return self.evaluationFunction(state), None

            legal_actions = state.getLegalActions(agent_index)

            if not legal_actions:
                return self.evaluationFunction(state), None

            best_action = None

            if agent_index == 0:
                v = -float('inf')
                for action in legal_actions:
                    successor = state.generateSuccessor(agent_index, action)
                    score, _ = alphaBeta(successor, turn_index + 1, alpha, beta)

                    if score > v:
                        v, best_action =  score, action

                    if v > beta:
                        return v, best_action

                    alpha = max(alpha, v)
                return v, best_action

            else:
                v = float("inf")
                for action  in legal_actions:
                    successor = state.generateSuccessor(agent_index, action)
                    score, _ = alphaBeta(successor, turn_index + 1, alpha, beta)

                    if score < v:
                        v, best_action = score, action

                    if v < alpha:
                        return v, best_action

                    beta = min(beta, v)

                return v, best_action


        _, action = alphaBeta(gameState, 0, -float("inf"), float("inf"))
        return action


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
        def expecitmax(state, turn_index):
            agent_index = turn_index % state.getNumAgents()
            current_depth = turn_index // state.getNumAgents()

            if state.isWin() or  state.isLose() or current_depth == self.depth:
                return self.evaluationFunction(state), None

            legal_actions = state.getLegalActions(agent_index)

            if not legal_actions:
                return self.evauationFunction(state), None

            if agent_index == 0:
                best_score = -float("inf")
                best_action = None

                for action in legal_actions:
                    successor = state.generateSuccessor(agent_index, action)
                    score, _ = expecitmax(successor, turn_index + 1)

                    if score > best_score:
                        best_score, best_action = score, action

                return best_score, best_action

            else:
                probability = 1.0 / len(legal_actions)
                expected_score = 0.0

                for action in legal_actions:
                     successor = state.generateSuccessor(agent_index, action)
                     score, _ = expecitmax(successor, turn_index + 1)
                     expected_score += score * probability

                return expected_score, None

        _, action = expecitmax(gameState, 0)
        return action


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Starts from the game score, rewards being close to food and
    scared ghosts, penalizes leftover food/capsules and being next to an
    active ghost.
    """
    # Big but finite so expectimax averages stay meaningful
    # (one -inf child would make a whole chance node -inf).
    if currentGameState.isWin():
        return 10000 + currentGameState.getScore()
    if currentGameState.isLose():
        return -10000 + currentGameState.getScore()

    pos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()

    score = currentGameState.getScore()

    # Food features
    if foodList:
        closestFood = min(manhattanDistance(pos, f) for f in foodList)
        score += 10.0 / closestFood
    score -= 4 * len(foodList)

    # Capsule feature
    score -= 20 * len(capsules)

    # Ghost features
    for ghost in ghostStates:
        dist = manhattanDistance(pos, ghost.getPosition())
        if ghost.scaredTimer > dist:
            # Scared ghost we can catch in time: chase it
            score += 50.0 / max(dist, 1)
        elif dist <= 1:
            # Active ghost right next to us: get away
            score -= 500

    return score


# Abbreviation
better = betterEvaluationFunction
