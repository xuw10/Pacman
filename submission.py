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
  def __init__(self):
    self.lastPositions = []
    self.dc = None


  def getAction(self, gameState):
    """
    getAction chooses among the best options according to the evaluation function.

    getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East, Stop}
    ------------------------------------------------------------------------------
    Description of GameState and helper functions:

    A GameState specifies the full game state, including the food, capsules,
    agent configurations and score changes. In this function, the |gameState| argument 
    is an object of GameState class. Following are a few of the helper methods that you 
    can use to query a GameState object to gather information about the present state 
    of Pac-Man, the ghosts and the maze.
    
    gameState.getLegalActions(): 
        Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

    gameState.generateSuccessor(agentIndex, action): 
        Returns the successor state after the specified agent takes the action. 
        Pac-Man is always agent 0.

    gameState.getplayerState():
        Returns an AgentState object for player (in game.py)
        state.pos gives the current position
        state.direction gives the travel vector

    gameState.getGhostStates():
        Returns list of AgentState objects for the ghosts

    gameState.getNumAgents():
        Returns the total number of agents in the game

    
    The GameState class is defined in player.py and you might want to look into that for 
    other helper methods, though you don't need to.
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best




    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    The evaluation function takes in the current and proposed successor
    GameStates (player.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and player position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of player having eaten a power pellet.
    """
    # Useful information you can extract from a GameState (player.py)
    successorGameState = currentGameState.generateplayerSuccessor(action)
    newPos = successorGameState.getplayerPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


    return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the player GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxplayerAgent, AlphaBetaplayerAgent & ExpectimaxplayerAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # player is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

######################################################################################
# Problem 1b: implementing minimax

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (problem 1)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction. Terminal states can be found by one of the following: 
      player won, player lost or there are no legal moves. 

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means player, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
	
      gameState.isWin():
        Returns True if it's a winning state
	
      gameState.isLose():
        Returns True if it's a losing state

      self.depth:
        The depth to which search should continue
    """

    # BEGIN_YOUR_CODE (around 30 lines of code expected)
    player = 0
    def maxAgent(state, depth):
            if state.isWin() or state.isLose():
                return state.getScore()
            actions = state.getLegalActions(player)
            optimalScore = float("-inf")
            score = optimalScore
            optimalAction = Directions.STOP
            for action in actions:
                score = optAgent(state.generateSuccessor(player, action), depth, 1)
                if score > optimalScore:
                    optimalScore = score
                    optimalAction = action
            if depth == 0:
                return optimalAction
            else:
                return optimalScore

    def optAgent(state, depth, ghost):
            if state.isLose() or state.isWin():
                return state.getScore()
            sucessorG = ghost + 1
            if ghost == state.getNumAgents() - 1:
                sucessorG = player
            actions = state.getLegalActions(ghost)
            optimalScore = float("inf")
            score = optimalScore
            for action in actions:
                if sucessorG == player:
                    if depth == self.depth - 1:
                        score = self.evaluationFunction(state.generateSuccessor(ghost, action))
                    else:
                        score = maxAgent(state.generateSuccessor(ghost, action), depth + 1)
                else:
                    score = optAgent(state.generateSuccessor(ghost, action), depth, sucessorG)
                if score < optimalScore:
                    optimalScore = score
            return optimalScore
    return maxAgent(gameState, 0)
    # raise Exception("Not implemented yet")
    # END_YOUR_CODE

######################################################################################
# Problem 2a: implementing alpha-beta

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (problem 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """

    # BEGIN_YOUR_CODE (around 50 lines of code expected)
    player = 0
    def maxAgent(state, depth, alpha, beta):
            if state.isWin() or state.isLose():
                return state.getScore()
            actions = state.getLegalActions(player)
            optimalScore = float("-inf")
            score = optimalScore
            optimalAction = Directions.STOP
            for action in actions:
                score = minAgent(state.generateSuccessor(player, action), depth, 1, alpha, beta)
                if score > optimalScore:
                    optimalScore = score
                    optimalAction = action
                alpha = max(alpha, optimalScore)
                if optimalScore > beta:
                    return optimalScore
            if depth == 0:
                return optimalAction
            else:
                return optimalScore

    def minAgent(state, depth, ghost, alpha, beta):
            if state.isLose() or state.isWin():
                return state.getScore()
            sucessorG = ghost + 1
            if ghost == state.getNumAgents() - 1:   
                sucessorG = player
            actions = state.getLegalActions(ghost)
            optimalScore = float("inf")
            score = optimalScore
            for action in actions:
                if sucessorG == player:
                    if depth == self.depth - 1:
                        score = self.evaluationFunction(state.generateSuccessor(ghost, action))
                    else:
                        score = maxAgent(state.generateSuccessor(ghost, action), depth + 1, alpha, beta)
                else:
                    score = minAgent(state.generateSuccessor(ghost, action), depth, sucessorG, alpha, beta)
                if score < optimalScore:
                    optimalScore = score
                beta = min(beta, optimalScore)
                if optimalScore < alpha:
                    return optimalScore
            return optimalScore
    return maxAgent(gameState, 0, float("-inf"), float("inf"))
    # raise Exception("Not implemented yet")
    # END_YOUR_CODE

######################################################################################
# Problem 3b: implementing expectimax

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (problem 3)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """

    # BEGIN_YOUR_CODE (around 25 lines of code expected)
    player = 0
    def maxAgent(state, depth):
            if state.isWin() or state.isLose():
                return state.getScore()
            actions = state.getLegalActions(player)
            optimalScore = float("-inf")
            score = optimalScore
            optimalAction = Directions.STOP
            for action in actions:
                score = minAgent(state.generateSuccessor(player, action), depth, 1)
                if score > optimalScore:
                    optimalScore = score
                    optimalAction = action
            if depth == 0:
                return optimalAction
            else:
                return optimalScore

    def minAgent(state, depth, ghost):
            if state.isLose():
                return state.getScore()
            sucessorG = ghost + 1
            if ghost == state.getNumAgents() - 1:
                sucessorG = player
            actions = state.getLegalActions(ghost)
            optimalScore = float("inf")
            score = optimalScore
            for action in actions:
                probability = float(1.0/len(actions))
                if sucessorG == player:
                    if depth == self.depth - 1:
                        score = self.evaluationFunction(state.generateSuccessor(ghost, action))
                        score += probability * score
                    else:
                        score = maxAgent(state.generateSuccessor(ghost, action), depth + 1)
                        score += probability * score
                else:
                    score = minAgent(state.generateSuccessor(ghost, action), depth, sucessorG)
                    score += probability * score
            return score
    return maxAgent(gameState, 0)
    # raise Exception("Not implemented yet")
    # END_YOUR_CODE

######################################################################################
# Problem 4a (extra credit): creating a better evaluation function

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (problem 4).

    DESCRIPTION: <write something here so we know what you did>
  """

  # BEGIN_YOUR_CODE (around 30 lines of code expected)
  def nearestD(pacmanCur, food_pos):
        food_distances = []
        for food in food_pos:
            food_distances.append(util.manhattanDistance(food, pacmanCur))
        return min(food_distances) if len(food_distances) > 0 else 1
  def nearestGhost(pacmanCur, ghosts):
        food_distances = []
        for food in ghosts:
            food_distances.append(util.manhattanDistance(food.getPosition(), pacmanCur))
        return min(food_distances) if len(food_distances) > 0 else 1
  def nearestCap(pacmanCur, coordCapsules):
        capsule_distances = []
        for caps in coordCapsules:
            capsule_distances.append(util.manhattanDistance(caps, pacmanCur))
        return min(capsule_distances) if len(capsule_distances) > 0 else 9999999
  def ghostT(pacmanCur, ghost_states, radius, scores):
        num_ghosts = 0
        for ghost in ghost_states:
            if util.manhattanDistance(ghost.getPosition(), pacmanCur) <= radius:
                scores -= 30
                num_ghosts += 1
        return scores
  def foodT(pacmanCur, food_positions):
        food_distances = []
        for food in food_positions:
            food_distances.append(util.manhattanDistance(food, pacmanCur))
        return sum(food_distances)
  def Nfood(pacmanCur, food):
        return len(food)
  def minGhosts(ghost_states, pacmanCur, scores):
        scoresAll = []
        for ghost in ghost_states:
            if ghost.scaredTimer > 8 and util.manhattanDistance(ghost.getPosition(), pacmanCur) <= 4:
                scoresAll.append(scores + 50)
            if ghost.scaredTimer > 8 and util.manhattanDistance(ghost.getPosition(), pacmanCur) <= 3:
                scoresAll.append(scores + 60)
            if ghost.scaredTimer > 8 and util.manhattanDistance(ghost.getPosition(), pacmanCur) <= 2:
                scoresAll.append(scores + 70)
            if ghost.scaredTimer > 8 and util.manhattanDistance(ghost.getPosition(), pacmanCur) <= 1:
                scoresAll.append(scores + 90)
        return max(scoresAll) if len(scoresAll) > 0 else scores
  def aggressions(ghost_states, pacmanCur, scores):
        scoresAll = []
        for ghost in ghost_states:
            if ghost.scaredTimer == 0:
                scoresAll.append(scores - util.manhattanDistance(ghost.getPosition(), pacmanCur) - 10)
        return max(scoresAll) if len(scoresAll) > 0 else scores
  def scorePacman(pacmanCur, food_pos, ghost_states, coordCapsules, score):
        if nearestCap(pacmanCur, coordCapsules) < nearestGhost(pacmanCur, ghost_states):
            return score + 40
        if nearestD(pacmanCur, food_pos) < nearestGhost(pacmanCur, ghost_states) + 3:
            return score + 20
        if nearestCap(pacmanCur, coordCapsules) < nearestD(pacmanCur, food_pos) + 3:
            return score + 30
        else:
            return score
  coordCap = currentGameState.getCapsules()
  coordAgent = currentGameState.getPacmanPosition()
  score = currentGameState.getScore()
  food = currentGameState.getFood().asList()
  ghosts = currentGameState.getGhostStates()    
  score = scorePacman(coordAgent, food, ghosts, coordCap, score)
  score = minGhosts(ghosts, coordAgent, score)
  score = aggressions(ghosts, coordAgent, score)
  score -= .35 * foodT(coordAgent, food)
  return score

  # raise Exception("Not implemented yet")
  # END_YOUR_CODE

# Abbreviation
better = betterEvaluationFunction


