import numpy
import random
import math
import time
import collections

def readInputFromFile(inputFileName):
    with open(inputFileName) as file:
        Method = file.readline().rstrip('\n')
        n = int(file.readline().rstrip('\n'))
        numberOfLizards = int(file.readline().rstrip('\n'))
        inputMatrix = [[] for i in range(n)]
        i = 0
        for line in file.readlines():
            line = line.rstrip('\n')
            inputMatrix[i] = list(map(int, line))
            i += 1
        return Method, n, numberOfLizards, inputMatrix

Method, n, numberOfLizards, Matrix = readInputFromFile('input.txt')
# collections deque is faster than a list interpretation of queue and queue library in python
stateQ = collections.deque()
start_time = time.time()
# end time
end_time_bfs = start_time + 295

def treeExistsInColumn(row1, row2, column, treeMap):
    for rowNumber in range(row2-1, row1, -1):
        if treeMap[rowNumber] and column in treeMap[rowNumber]:
            return True
    return False

def treeExistsInDiagonal(row1, column1, row2, column2, treeMap):
    if column2 > column1:
        column = column2 - 1
        for rowNumber in range(row2-1, row1, -1):
            if treeMap[rowNumber] and column in treeMap[rowNumber]:
                return True
            column -= 1
    elif column1 > column2:
        column = column2 + 1
        for rowNumber in range(row2-1, row1, -1):
            if treeMap[rowNumber] and column in treeMap[rowNumber]:
                return True
            column += 1
    return False

def isValidMove(state, rowNumber, columnNumber, treeMap):
    if Matrix[rowNumber][columnNumber] == 2:  # if there is a tree on this position
        return False
    else:
        for index in range(rowNumber):
            for col in state[index]:
                if columnNumber == col and not treeExistsInColumn(index, rowNumber, columnNumber, treeMap):
                    return False
                elif rowNumber-index == abs(columnNumber-col) and not treeExistsInDiagonal(index, col, rowNumber, columnNumber, treeMap):
                    return False
        return True

def getNextRowAndColumn(row, column, treeMap):
    # if the last placed position was in the previous row. -1 indicates valid positions have to be checked from start of this row
    if column == -1:
        if row < n:
            for index in range(n):
                if Matrix[row][index] == 0:
                    return row, index
            return getNextRowAndColumn(row+1, -1, treeMap)
        else:
            return -1, -1
    else:
        treeColumn = -1
        for index in range(0, len(treeMap[row])):
            if treeColumn == -1:
                if treeMap[row][index] > column:
                    treeColumn = treeMap[row][index]
            else:
                if not treeMap[row][index] == treeColumn+1:
                    break
                treeColumn += 1

        if treeColumn == -1 or treeColumn == n-1:  # if there is no tree in this row, go to next row
            return getNextRowAndColumn(row+1, -1, treeMap)
        elif treeColumn+1 < n:  # if column after tree column is still within row
            return row, treeColumn+1

# write solution from final state to matrix.
def writeSolutionToMatrix(solutionState):
    for rowNumber in range(n):
        for columnNumber in solutionState[rowNumber]:
            Matrix[rowNumber][columnNumber] = 1
    return Matrix

def writeOutputToFile(outputFileName, success):
    with open(outputFileName, 'w+') as outputfile:
        if success:
            outputfile.write('OK\n')
            for row in Matrix:
                for element in row:
                    outputfile.write(str(element))
                outputfile.write('\n')
        else:
            outputfile.write('FAIL')

# form map of trees on the board
def formTreeMap(Matrix):
    treeMap = {k: [] for k in range(n)}
    for i in range(n):
        for j in range(n):
            if Matrix[i][j] == 2:
                treeMap[i].append(j)
    return treeMap

# add state object to state queue
def addLizardPosToQ(lizardPos, lastVisitedIndex, lizardCount):
    newStateObject = State()
    newStateObject.lizardPos = lizardPos
    newStateObject.lastVisitedIndex = lastVisitedIndex
    newStateObject.lizardCount = lizardCount
    stateQ.append(newStateObject)

class State:
    lizardCount = 0
    # an adjacency list kind of representation is taken, which shows lizard position in each row
    lizardPos = [[] for i in range(n)]
    lastVisitedIndex = (0, -1)

def BFS():
    global Matrix
    global end_time_bfs
    initialState = State()
    stateQ.append(initialState)
    finished = False
    # form a tree map of the trees present on the board before starting algorithm
    treeMap = formTreeMap(Matrix)
    while stateQ and not finished and time.time() < end_time_bfs:
        # state Object consists of lizard positions, lizard count and last visited position for this state
        currentStateObject = stateQ.popleft()
        currentState = currentStateObject.lizardPos
        currentLizardCount = currentStateObject.lizardCount
        # get Next Row and Column where lizard can be placed
        startPosition = getNextRowAndColumn(currentStateObject.lastVisitedIndex[0], currentStateObject.lastVisitedIndex[1], treeMap)
        currentRow = startPosition[0]
        if not currentRow == -1:
            for i in range(startPosition[1], n):
                if isValidMove(currentState, currentRow, i, treeMap):  # check if its a valid move for the current state, row, column and treeMap
                    newState = list(map(list, currentState))  # create new state and append new lizard position to new state
                    newState[currentRow].append(i)
                    if currentLizardCount + 1 == numberOfLizards:  # if solution is found
                        Matrix = writeSolutionToMatrix(newState)
                        finished = True
                        break
                    else:
                        addLizardPosToQ(newState, (currentRow, i), currentLizardCount+1)
                if i == n - 1 and not currentRow == n - 1:  # add Empty child at the end of each row to handle cases where row should be kept empty
                    addLizardPosToQ(currentState, (currentRow+1, -1), currentLizardCount)
    writeOutputToFile('output.txt', finished)

def main():
    global Matrix
    numberOfTrees = numpy.sum(Matrix)/2
    # lizards more than total of n and numberOfTrees cannot be placed on board without conflicts, so early termination
    # if lizards are more than empty positions on board, early terminate
    if numberOfLizards > (n + numberOfTrees) or numberOfLizards > n*n - numberOfTrees:
        writeOutputToFile('output.txt', False)
    else:
        if Method == 'BFS':
            BFS()

main()
print(time.time() - start_time)