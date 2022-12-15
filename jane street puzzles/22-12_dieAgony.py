'''Script to solve Jane Street Puzzle for December 2022'''
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt

board = np.array([
    [57, 33, 132, 268, 492, 732],
    [81, 123, 240, 443, 353, 508],
    [186, 42, 195, 704, 452, 228],
    [-7, 2, 357, 452, 317, 395],
    [5, 23, -4, 592, 445, 620],
    [0, 77, 32, 403, 337, 452],
    ])

# die starts in bottom left corner of board
startPos = (5, 0)
# nth move of die starts at 0
n = 0
# dictionary storing values on each face of the die
nums = {
    1: None,
    2: None,
    3: None,
    4: None,
    5: None,
    6: None,
}
# define starting orientation of the die
# these are the initial locations of each face described from bird's eye view
front = 1
top = 2
right = 3
bottom = 4
left = 5
back = 6


# recursive search function
def search(currentPos, count, numDict, front, top, right, bottom, left, back):
    # base case
    # die has arrived at upper right square of board
    if currentPos == (0, 5):
        return [currentPos]
    else:
        # increment count of moves (n)
        count += 1
        # loop over possible moves
        for move in range(1, 5):
            # 1 = roll die UP board
            if ((move == 1) and (currentPos[0] > 0)):
                # identify new position
                newPos = (currentPos[0] - 1, currentPos[1])
                # copy of die face values needed because likely to need to
                # roll back to previous values as search progresses
                tempNums = deepcopy(numDict)
                # rolling up means the previous bottom face becomes the front
                # assign a value if face does not yet have one
                if tempNums[bottom] is None:
                    tempNums[bottom] = ((board[newPos] - board[currentPos])
                                        / count)
                # check if move is invalid due to value of face and board
                elif board[newPos] != (board[currentPos]
                                       + count * tempNums[bottom]):
                    # try next possible move
                    continue
                # move must be valid
                # call search again to try moves from new position
                # use new face locations where original args are:
                # front, top, right, bottom, left, back
                # parameters given are those faces that are now in these
                # locations having just made the move above
                result = search(newPos, count, tempNums,
                                bottom, front, right, back, left, top)
                # only true once algorithm has arrived at base case
                if result:
                    # add current position to list of visited squares
                    result.insert(0, currentPos)
                    return result
            # 2 = roll die to the RIGHT on board
            elif ((move == 2) and (currentPos[1] < 5)):
                newPos = (currentPos[0], currentPos[1] + 1)
                tempNums = deepcopy(numDict)
                if tempNums[left] is None:
                    tempNums[left] = ((board[newPos] - board[currentPos])
                                      / count)
                elif board[newPos] != (board[currentPos]
                                       + count * tempNums[left]):
                    continue
                result = search(newPos, count, tempNums,
                                left, top, front, bottom, back, right)
                if result:
                    result.insert(0, currentPos)
                    return result
            # 3 = roll die DOWN board
            elif ((move == 3) and (currentPos[0] < 5)):
                newPos = (currentPos[0] + 1, currentPos[1])
                tempNums = deepcopy(numDict)
                if tempNums[top] is None:
                    tempNums[top] = ((board[newPos] - board[currentPos])
                                     / count)
                elif board[newPos] != (board[currentPos]
                                       + count * tempNums[top]):
                    continue
                result = search(newPos, count, tempNums,
                                top, back, right, front, left, bottom)
                if result:
                    result.insert(0, currentPos)
                    return result
            # 4 = roll die to the LEFT on board
            elif ((move == 4) and (currentPos[1] > 0)):
                newPos = (currentPos[0], currentPos[1] - 1)
                tempNums = deepcopy(numDict)
                if tempNums[right] is None:
                    tempNums[right] = ((board[newPos] - board[currentPos])
                                       / count)
                elif board[newPos] != (board[currentPos]
                                       + count * tempNums[right]):
                    continue
                result = search(newPos, count, tempNums,
                                right, top, back, bottom, front, left)
                if result:
                    result.insert(0, currentPos)
                    return result
        # all possible moves checked for current location
        return False


# run exhaustive search until valid route to upper right square is found
# returns a list of tuples, where tuples are coordinates of squares visited
allMoves = search(startPos, n, nums, front, top, right, bottom, left, back)
# compute list of tuples, where tuples are coordinates of all squares on board
allPositions = [(row, col) for row in range(6) for col in range(6)]
# compute list of un-visited squares
unusedPositions = [pos for pos in allPositions if pos not in allMoves]
# sum board value of all un-visited squares
answer = 0
for pos in unusedPositions:
    answer += board[pos]
print(answer)

# convert to np array for plotting route
movesArr = np.asarray(allMoves)
fig, ax = plt.subplots()
ax.plot(
    movesArr[:, 1],
    movesArr[:, 0],
)
ax.invert_yaxis()
plt.show()
