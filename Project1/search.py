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

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    visited = set()
    stack = util.Stack()
    start = problem.getStartState()
    stack.push((start, []))

    while stack.isEmpty() == False:
        cur_node, path = stack.pop()
        if problem.isGoalState(cur_node):
            return path
        else:
            if cur_node in visited:
                continue
            else:
                visited.add(cur_node)
            successors = problem.getSuccessors(cur_node)
            for (succ, action, cost) in successors:
                new_path = path + [action]
                stack.push((succ, new_path))

    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    visited = set()
    queue = util.Queue()
    start = problem.getStartState()
    queue.push((start, []))

    while queue.isEmpty() == False:
        curNode, path = queue.pop()
        if(problem.isGoalState(curNode) == True):
            return path
        else:
            if curNode in visited:
                continue
            else:
                visited.add(curNode)
            successor = problem.getSuccessors(curNode)
            for(succ, action, cost) in successor:
                newPath = path + [action]
                queue.push((succ, newPath))

    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    pQueue = util.PriorityQueue()
    visited = set()
    start = problem.getStartState()
    cost = {start : 0}
    pQueue.push([start, None, 0], 0)
    path = []
    par = {}
    while(1):
        curCost = 0

        if pQueue.isEmpty():
            return -1
        curNode = pQueue.pop()

        if problem.isGoalState(curNode[0]):
            break
        else:
            if curNode[0] in visited:
                continue
            visited.add(curNode[0])

            for state in problem.getSuccessors(curNode[0]):
                curCost = cost[curNode[0]] + state[2]
                if state[0] not in visited and state not in pQueue.heap:
                    par[state] = curNode
                    cost[state[0]] = curCost
                    pQueue.push(state, curCost)
                elif state in pQueue.heap:
                    if curCost < cost[state[0]]:
                        cost[state[0]] = curCost
                        par[state] = curNode
    end = curNode

    while end != None:
        if end[0] == start:
            end = None
        else:
            path.append(end[1])
            end = par[end]
        
    path.reverse()
    return path
    
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
