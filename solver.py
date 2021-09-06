import turtle
import numpy as np
import sud_solve


pen = turtle.Turtle()       # CREATE THE SUDOKU
pen.speed(0)                # set speed to as fast as possible
turtle.tracer(0, 0)
pen.color("#000000")        # draw with black color
pen.hideturtle()
Yboard_start = 230
Xboard_start = -230         # we start from the top left of the screen


def text(no, x, y, size):
    pen.penup()
    pen.goto(x, y)
    # writes the value at the position defined
    pen.write(no, align="left", font=('Arial', size, 'normal'))


def make_board(board):
    dimension = 50      # dimension of each box [ the ones containing numbers ]
    for row in range(10):
        pen.pensize(1)
        if (row % 3) == 0:
            # bold for rows and columns
            pen.pensize(3)
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
        pen.goto(Xboard_start + col*dimension, Yboard_start - 9*dimension)

    # enter the values in the board just made
    for row in range(0, 9):
        for col in range(0, 9):
            if board[row][col] != 0:
                text(board[row][col], Xboard_start + col*dimension + 20,
                     Yboard_start - row*dimension - dimension + 10, 18)
                # 20 added to row, and 10 to the column
                # to center the number withing a box


def solve(board):
    if not(0 in board.flatten()):
        print(" Solved ")
        print(board)
        return True
    # get the first element of the possible array
    row, col = sud_solve.get_pos(board)
    # since the function reaches here,
    # that implies there is at least one 0 in the board
    remaining = sud_solve.find_possible((row, col), board)
    for no in remaining:
        if not(sud_solve.check_violation(board, no, row, col)):
            board[row][col] = no
            pen.clear()
            make_board(board)
            pen.getscreen().update()  # draw the board again
            if solve(board):
                return True
            # reverse the change made
            board[row][col] = 0
    # since if the function reaches till the end that implies
    # incorrect combination, so backtracking happens
    return False


""" INPUT STILL TO BE TAKEN FROM A PICTURE """
board = [[5, 6, 7, 1, 3, 2, 8, 4, 9],
         [9, 3, 2, 5, 4, 8, 1, 7, 6],
         [1, 0, 0, 0, 6, 9, 0, 3, 5],
         [3, 1, 0, 0, 9, 0, 0, 0, 8],
         [0, 0, 4, 0, 0, 0, 0, 0, 7],
         [6, 7, 0, 0, 8, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 4, 0, 9, 0],
         [0, 0, 0, 9, 0, 0, 4, 0, 0],
         [4, 0, 0, 0, 0, 3, 0, 8, 2]]
""" For the time being edit the above array to get desired results """
make_board(board)
pen.getscreen().update()    # make the board

board = np.array(board)
if solve(board):
    text(" SOLVED ", -70, 250, 18)
    print("done")
else:
    text(" Can't be done", -90, 250, 18)
    print("no")
turtle.exitonclick()
