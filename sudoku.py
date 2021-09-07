import cv2
import numpy as np
import pandas as pd
import turtle
from sklearn.externals import joblib
import image_utils as IU
import game_utils as GU


def generate_result(board):

    pen = turtle.Turtle()       # CREATE THE SUDOKU
    pen.speed(0)                # set speed to as fast as possible
    turtle.tracer(0, 0)
    pen.color("#000000")        # draw with black color
    pen.hideturtle()
    Yboard_start = 230
    Xboard_start = -230         # we start from the top left of the screen

    GU.make_board(board, pen, Xboard_start, Yboard_start)
    pen.getscreen().update()    # make the board

    board = np.array(board)
    if solve(board, pen, Xboard_start, Yboard_start):
        GU.write_text(" SOLVED ", -70, 250, 18, pen)
        print("done")
    else:
        GU.write_text(" Can't be done", -90, 250, 18, pen)
        print("no")
    turtle.exitonclick()


def solve_puzzle_from_image(image, model):
    puzzle = cv2.imread(image)
    gray = cv2.cvtColor(puzzle, cv2.COLOR_BGR2GRAY)
    # blur to be able to detect all the edges in the image clearly
    blur_gray = cv2.blur(gray, (3, 3))
    edges = cv2.Canny(puzzle, 30, 90, apertureSize=3)

    # 200 pixels is set to be the minimum length of the line to be detected
    lines = cv2.HoughLines(edges, 2, np.pi/180, 300, 0, 0)
    # sort the lines based on the value of ppd
    lines = sorted(lines, key=lambda line: line[0][0])
    # draw detected lines to see whether lines have been detected ..
    h_list, v_list = IU.flag_lines(lines, puzzle)

    IU.draw_detected(lines, puzzle)
    points = IU.get_intersection(h_list, v_list)
    print("Total points detected -> ", len(points))

    # since number of points have to be 100
    if len(points) == 100:
        # convert to binary image
        bin_img = cv2.adaptiveThreshold(blur_gray, 255,
                                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 101, 1)
        # display_img(bin_img,"binary image")
        model = joblib.load("model.sav")
        board = GU.get_board(bin_img, points, model)
        if GU.is_solvable(board):
            generate_result(board)
        else:
            print("Sorry! Failed to process image, enter SUDOKU manually")
            board = GU.enter_board_manually()
            generate_result(board)
    else:
        print("Sorry! Failed to process image, enter SUDOKU manually !! ")
        board = GU.enter_board_manually()
        generate_result(board)


if __name__ == "__main__":
    import argparse
    import pandas as pd
    from pathlib import Path
    import excel_utils as EU

    parser = argparse.ArgumentParser(description='Page Extraction')
    parser.add_argument("--puzzle", help="Path to Image containing puzzle",
                        default="sample.jpg", type=str)
    parser.add_argument("--model", help="Model for digit recognition",
                        default="True", type=str)
    args = parser.parse_args()
    solve_puzzle_from_image(args.puzzle, args.model)

"""
TO DO :
1. Connect to the rest of the program
2. Improve Digit Recognition model
"""
