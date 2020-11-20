# Library for solving sudoku
# Run module to solve sample cases
#
# Written by Jim Ogren
#
import copy
import time
import requests

NROWS = 9
NCOLS = 9

def printSudoku(board):
    for i in range(NROWS):
        # every third row, make horizontal line
        if i%3==0 :
            for j in range(len(board[i])):
                if j%3 == 0:
                    print("|",end='')
                print("———", end='')
            print("|")

        # print all numbers
        for j in range(len(board[i])):
            # everythird digit, make vertical line
            if j%3 == 0:
                print("|",end='')
            print(" {} ".format(board[i][j]), end='')
        print("|")

    # add horizontal line at the end
    for j in range(len(board[i])):
        if j%3 == 0:
            print("|",end='')
        print("———", end='')
    print("|")

def validateRowsAndColumns(board):
    for i in range(NROWS):
        d1 = dict()
        d2 = dict()
        for j in range(NCOLS):
            if board[i][j] != '.':
                if board[i][j] not in d1:
                    d1[board[i][j]] = 1
                else:
                    return False
            if board[j][i] != '.':
                if board[j][i] not in d2:
                    d2[board[j][i]] = 1
                else:
                    return False
    return True

def validateBoxes(board):
    # check 3-by-3 boxes, first row
    for k in range(0,3):
        d = dict()
        for i in range(0,3):
            for j in range(0+k*3,3+k*3):
                if board[i][j] != '.':
                    if board[i][j] not in d:
                        d[board[i][j]] = 1
                    else:
                        return False

    # check 3-by-3 boxes, second row
    for k in range(0,3):
        d = dict()
        for i in range(3,6):
            for j in range(0+k*3,3+k*3):
                if board[i][j] != '.':
                    if board[i][j] not in d:
                        d[board[i][j]] = 1
                    else:
                        return False

    # check 3-by-3 boxes, third row
    for k in range(0,3):
        d = dict()
        for i in range(6,9):
            for j in range(0+k*3,3+k*3):
                if board[i][j] != '.':
                    if board[i][j] not in d:
                        d[board[i][j]] = 1
                    else:
                        return False
    return True

def validateSudoku(board):
    if validateRowsAndColumns(board):
        if validateBoxes(board):
            return True
    return False

def validateCandidate(board, index):
    d1 = dict()
    d2 = dict()
    for i in range(NROWS):
        if board[i][index[1]] != '.':
            if board[i][index[1]] not in d1:
                d1[board[i][index[1]]] = 1
            else:
                return False
        if board[index[0]][i] != '.':
            if board[index[0]][i] not in d2:
                d2[board[index[0]][i]] = 1
            else:
                return False

    if index[0] < 3: row = 0
    elif index[0] < 6: row = 1
    else: row = 2

    if index[1] < 3: col = 0
    elif index[1] < 6: col = 1
    else: col = 2

    d = dict()
    for i in range(row*3,row*3+3):
        for j in range(col*3,col*3+3):
            if board[i][j] != '.':
                if board[i][j] not in d:
                    d[board[i][j]] = 1
                else:
                    return False
    return True

def listEmptySlots(board):
    out = list()
    for row in range(NROWS):
        for col in range(NCOLS):
            if board[row][col] == '.':
                out.append((row, col))
    return out

def sudokuIsSolved(board):
    return len(listEmptySlots(board)) == 0 and validateSudoku(board)


def listCandidates(board, index):
    out = list()
    for i in range(1,10):
        board[index[0]][index[1]] = str(i)
        if validateCandidate(board, index):
            out.append(i)
    board[index[0]][index[1]] = '.'
    return out

def listAllCandidates(board):
    out_candidates = list()
    out_indices = list()
    emptySlots = listEmptySlots(board)
    for slot in emptySlots:
        candidates = listCandidates(board, slot)
        out_candidates.append(candidates)
        out_indices.append(slot)
    return out_candidates, out_indices

def isUnSolvable(board):
    if sudokuIsSolved(board):
        return False
    candidates, indices = listAllCandidates(board)
    for candidate in candidates:
        if len(candidate) < 1:
            return True
    return False

def solveSudoku(board):
    while not sudokuIsSolved(board):
        candidates, indices = listAllCandidates(board)
        if len(min(candidates, key=len))<1:
            break

        noProgress = True
        # set obvious values (only single candidate)
        for i in range(len(candidates)):
            candidate = candidates[i]
            index = indices[i]
            if len(candidate) == 1:
                board[index[0]][index[1]] = str(candidate[0])
                noProgress = False

        # test one of two candidates
        if noProgress:
            for j in range(len(candidates)):
                if len(candidates[j]) < 3:
                    candidate = candidates[j]
                    index = indices[j]
                    break

            # Make copy and test first candidate
            board_temp = copy.deepcopy(board)
            board[index[0]][index[1]] = str(candidate[0])
            board_out, success = solveSudoku(board)
            if success:
                break
            else:
                for row in range(NROWS):
                    for col in range(len(board[row])):
                        board[row][col] = board_temp[row][col]
                board[index[0]][index[1]] = str(candidate[1])

    if sudokuIsSolved(board):
        return board, True
    else:
        return list(), False


def run_solver(input):
    print("INPUT:")
    printSudoku(input)
    print("Solving...")

    start_time = time.time()
    solved, success = solveSudoku(copy.deepcopy(input))
    end_time = time.time()
    time_elapsed = end_time-start_time

    if success:
        print("Sudoku successfully solved in %3.2f seconds" % (time_elapsed))
        printSudoku(solved)
    else:
        print("Could not solve Sudoku. Exiting...")


def fetchSudoku(level='1'):
    url = 'http://nine.websudoku.com/?level='+level
    print('\nFetching a Sudoku of level %s from: %s' % (level, url))


    data = requests.get(url)
    words = data.text.split()
    start_of_puzzle = 0
    for i in range(len(words)):
        if words[i] == "id=\"puzzle_container\"":
            start_of_puzzle = i

    board = list()
    counter = 0
    while len(board) < 9:
        line = list()
        while len(line) < 9:
            word = words[start_of_puzzle + counter]
            if len(word) > 6 and word[:6]=="onBlur":
                line.append('.')
            if len(word) > 6 and word[:5]=="VALUE":
                line.append(str(word[-2]))
            counter+=1
        board.append(line)

    return board

def run_sample_cases():
    # sample sudokus
    # Easy
    sudoku1 = [
      ["5","3",".",".","7",".",".",".","."],
      ["6",".",".","1","9","5",".",".","."],
      [".","9","8",".",".",".",".","6","."],
      ["8",".",".",".","6",".",".",".","3"],
      ["4",".",".","8",".","3",".",".","1"],
      ["7",".",".",".","2",".",".",".","6"],
      [".","6",".",".",".",".","2","8","."],
      [".",".",".","4","1","9",".",".","5"],
      [".",".",".",".","8",".",".","7","9"]
    ]

    # Medium
    sudoku2 = [
      ["2",".",".","4",".",".","8",".","."],
      [".",".",".","2","6","5",".",".","9"],
      ["6","1",".",".","3",".",".",".","."],
      ["5",".","4",".",".",".","1",".","."],
      [".","3","8",".","2",".","6","7","."],
      [".",".","2",".",".",".","9",".","5"],
      [".",".",".",".","5",".",".","6","8"],
      ["4",".",".","3","8","2",".",".","."],
      [".",".","9",".",".","6",".",".","3"]
    ]

    # Hard
    sudoku3 = [
      [".",".","2","1","9",".",".","5","."],
      ["4",".",".",".","6",".",".",".","3"],
      ["3",".",".",".",".",".",".",".","."],
      ["6","9",".",".","2","8",".",".","."],
      [".",".","7",".",".",".","4",".","."],
      [".",".",".","6","5",".",".","9","8"],
      [".",".",".",".",".",".",".",".","1"],
      ["8",".",".",".","1",".",".",".","2"],
      [".","2",".",".","8","5","7",".","."]
    ]

    # Evil
    sudoku4 = [
      [".","6",".",".",".",".",".",".","."],
      ["1",".",".","6",".",".","3",".","."],
      [".",".",".","4","9","1",".",".","5"],
      [".",".","1",".",".","2",".",".","4"],
      [".","3",".",".","1",".",".","6","."],
      ["2",".",".","7",".",".","1",".","."],
      ["5",".",".","1","3","4",".",".","."],
      [".",".","6",".",".","5",".",".","9"],
      [".",".",".",".",".",".",".","2","."]
    ]

    # Run sample cases
    print("\nExample 1: EASY")
    run_solver(sudoku1)

    print("\nExample 2: MEDIUM")
    run_solver(sudoku2)

    print("\nExample 3: HARD")
    run_solver(sudoku3)

    print("\nExample 4: EVIL")
    run_solver(sudoku4)


if __name__ == "__main__":
    run_sample_cases()
