#Python 2.7
#psutil is an external package, install it before running the program

import copy as cp
import time
import os
import psutil
import sys

'''
Uncomment if want the script to install psutil package
try:
    import psutil  # for computing memory usage
except ImportError:  # try to install requests module if not present
    print ("Trying to Install required module: psutil\n")
    os.system('sudo python -m pip install psutil')
import psutil
'''

def iterative_deepening_depth_search(iInitialState, iFinalState):
    '''
    :param iInitialState: initial state of the puzzle
    :param iFinalState: goal state of the puzzle
    :return: solution path if any (action)
    '''

    node = str(iInitialState)
    final = str(iFinalState)

    if node == final:
        return node

    actionPath = []

    for i in xrange(sys.maxint): #the cutoff value theoretically is as good as infinity

        #Memory sanity check
        process = psutil.Process(os.getpid())
        memory = process.memory_info().rss / 1000000
        if memory > 200:
            print ("Memory limit exceeded")
            return None

        solutionPath = depth_limited_search([node], final, i, actionPath)
        if solutionPath:
            return solutionPath

        if i == sys.maxint: #If i reaches final cutoff value and no solution exists return none
            return None


def depth_limited_search(iCurrentPath, iFinalState, iDepth, oActionPath):
    '''

    :param iCurrentPath: The current path of the search tree
    :param iFinalState: Goal state
    :param iDepth: cutoff depth of the limited depth tree
    :param oActionPath: action path of the puzzle
    :return: action path of the puzzle
    '''
    depth = iDepth
    currentPath = iCurrentPath
    currentActionPath = oActionPath

    lastNode = currentPath[len(currentPath)-1]


    if(lastNode == iFinalState):
        return currentActionPath

    for currentState, actionMove in possibleStates(lastNode).iteritems():
        if currentState in currentPath: #Repeated states check
            continue

        if depth == 0: #depth limit for this iteration is over
            return None

        #recursively check in the depth limited tree
        solutionPath = depth_limited_search(currentPath + [currentState], iFinalState, depth - 1, currentActionPath + [actionMove])

        if solutionPath is not None:
            return solutionPath


# find possible states
def possibleStates(iCurrentState):
    '''
    :definition: returns the possible states from current state
    :param iInterState: the row or column in which the movement is to be done
    :return: return all possible states after tile is moved
    '''
    oPossibleStates = {}
    state = eval(iCurrentState)
    zeroIndex = [(ix, iy) for ix, row in enumerate(state) for iy, i in enumerate(row) if i == 0]
    iX = zeroIndex[0][0]
    iY = zeroIndex[0][1]

    minIndex = 0
    maxIndex = 3

    if iX > minIndex:  # move pieces up and append to possible states
        state[iX][iY], state[iX - 1][iY] = state[iX - 1][iY], state[iX][iY]
        tmp = cp.deepcopy(state)
        sequenceActionPair = {repr(tmp):"UP"}
        oPossibleStates.update(sequenceActionPair)
        # revert back to original state
        state[iX][iY], state[iX - 1][iY] = state[iX - 1][iY], state[iX][iY]

    if iX < maxIndex:  # move pieces down and append to possible states
        state[iX][iY], state[iX + 1][iY] = state[iX + 1][iY], state[iX][iY]
        tmp = cp.deepcopy(state)
        sequenceActionPair = {repr(tmp): "DOWN"}
        oPossibleStates.update(sequenceActionPair)
        # revert back to original state
        state[iX][iY], state[iX + 1][iY] = state[iX + 1][iY], state[iX][iY]

    if iY > minIndex:  # move pieces left and append to possible states
        state[iX][iY], state[iX][iY - 1] = state[iX][iY - 1], state[iX][iY]
        tmp = cp.deepcopy(state)
        sequenceActionPair = {repr(tmp): "LEFT"}
        oPossibleStates.update(sequenceActionPair)
        # revert back to original state
        state[iX][iY], state[iX][iY - 1] = state[iX][iY - 1], state[iX][iY]

    if iY < maxIndex:  # move pieces right and append to possible states
        state[iX][iY], state[iX][iY + 1] = state[iX][iY + 1], state[iX][iY]
        tmp = cp.deepcopy(state)
        sequenceActionPair = {repr(tmp): "RIGHT"}
        oPossibleStates.update(sequenceActionPair)
        # revert back to original state
        state[iX][iY], state[iX][iY + 1] = state[iX][iY + 1], state[iX][iY]

    return oPossibleStates


#main
if __name__ == '__main__':
    startTime = time.time()
    initialState = [[1, 2, 0, 4],
                    [5, 6, 3, 12],
                    [13, 9, 8, 7],
                    [14, 11, 10, 15]]

    # End state is the final solved state of the puzzle
    endState = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12],
                [13, 14, 15, 0]]

    path = iterative_deepening_depth_search(initialState, endState)

    if path == None:
        print "Solution does not exist"
    else:
        print "Action path of the solution is (in terms of 0 tile)- "
        for i in path:
            print i

    time = time.time() - startTime
    print ("Depth of Solution is: ", len(path))
    print ("Number of seconds to solve: ", time)
    process = psutil.Process(os.getpid())
    memory = process.memory_info().rss
    print ("Memory used:(in MB)", memory / 1000000)