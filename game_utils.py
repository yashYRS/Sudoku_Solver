import turtle
import numpy as np


def is_solvable(board):
    board = np.array(board)
    for row in range(9):
        for i in range(1, 10):
            temp_row = [1 for a in board[row] if a == i]
            temp_column = [1 for a in board[:, row] if a == i]
            if row % 3 == 0:
                for col in range(0, 9, 3):
                    temp_sq = [1 for a in board[row:row+3, col:col+3].flatten() if a == i]
                    if len(temp_sq) > 1:
                        return False
            if len(temp_row) > 1 or len(temp_column) > 1:
                return False
    return True


def check_violation(board, ele, row, col):
    if ele in board[row] or ele in board[:, col]:
        return True
    small_sqaure = board[3*int(row/3): 3*int(row/3) + 3,
                         3*int(col/3): 3*int(col/3) + 3].flatten()
    if ele in small_sqaure:
        return True
    # checks whether inserting an element in the board causes a violation
    return False


def find_possible(pos, board):
    # returns the values that can possibly occupy a particular position
    row, col = pos
    # unpack
    possible = [i for i in range(1, 10)]
    # for the small square
    small_sqaure = board[3*int(row/3): 3*int(row/3) + 3, 3*int(col/3): 3*int(col/3) + 3].flatten()
    for i in range(9):
        if(board[row][i] in possible):
            # since that number cant appear again...
            possible.remove(board[row][i])
        if (board[i][col] in possible):
            possible.remove(board[i][col])
        if(small_sqaure[i] in possible):
            possible.remove(small_sqaure[i])
    return possible


def find_empty_cell(board):
    # Returns the positino of the first 0 present in the board
    # [only called if there exists a 0 in a board ]
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)


def write_text(text, x, y, size, pen):
    pen.penup()
    pen.goto(x, y)
    # writes the value at the position defined
    pen.write(text, align="left", font=('Arial', size, 'normal'))


def make_board(board, pen, Xboard_start, Yboard_start):
    dimension = 50      # dimension of each box [ the ones containing numbers ]
    for row in range(10):
        pen.pensize(1)
        if (row % 3) == 0:
            pen.pensize(3)   # bold for rows and columns
        pen.penup()
        pen.goto(Xboard_start, Yboard_start - row*dimension)
        pen.pendown()
        # make the line
        pen.goto(Xboard_start + 9*dimension, Yboard_start-row*dimension)
    for col in range(10):
        pen.pensize(1)
        if (col % 3) == 0:
            pen.pensize(3)
        pen.penup()
        pen.goto(Xboard_start + col*dimension, Yboard_start)
        pen.pendown()
        # make the line
        pen.goto(Xboard_start + col*dimension, Yboard_start - 9*dimension)

    for row in range(0, 9):
        # enter the values in the board just made
        for col in range(0, 9):
            if board[row][col] != 0:
                write_text(board[row][col], Xboard_start + col*dimension + 20,
                     Yboard_start - row*dimension - dimension + 10, 18, pen)
                # 20 added to row, and 10 to the column to
                # center the number withing a box


def solve(board, pen, Xboard_start, Yboard_start):
    if not(0 in board.flatten()):
        print(" Solved ")
        print(board)
        return True
    # get the first element of the possible array
    row, col = find_empty_cell(board)
    # since the function reaches here,
    # that implies there is at least one 0 in the board
    remaining = find_possible((row, col), board)
    for no in remaining:
        if not(check_violation(board, no, row, col)):
            board[row][col] = no
            pen.clear()
            make_board(board, pen, Xboard_start, Yboard_start)
            # draw the board again
            pen.getscreen().update()
            if solve(board, pen, Xboard_start, Yboard_start):
                return True
            # reverse the change made
            board[row][col] = 0
    # since if the function reaches till the end that implies
    # incorrect combination, so backtracking happens
    return False
