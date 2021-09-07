import cv2
import turtle
import argparse
import numpy as np

import game_utils as GU
import image_utils as IU
import model_utils as MU


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


def solve_puzzle_from_image(image, model_path):
    model = MU.load_model(model_path)
    puzzle = cv2.imread(image)
    gray = cv2.cvtColor(puzzle, cv2.COLOR_BGR2GRAY)
    # blur to be able to detect all the edges in the image clearly
    blur_gray = cv2.GaussianBlur(gray, (5, 5), 0)
    IU.display_img(blur_gray, "EDGEs")
    edges = cv2.Canny(blur_gray, 30, 90, apertureSize=3)
    IU.display_img(edges, "EDGEs")

    # 200 pixels is set to be the minimum length of the line to be detected
    lines = cv2.HoughLines(edges, 1, np.pi/180, 160, 0, 0)
    # sort the lines based on the value of ppd
    lines = sorted(lines, key=lambda line: line[0][0])
    print("Befofe", len(lines))
    # draw detected lines to see whether lines have been detected ..
    h_list, v_list = IU.flag_lines(lines, puzzle)

    IU.draw_detected(lines, puzzle)
    points = IU.get_intersection(h_list, v_list)
    print("Total points detected -> ", len(points))

    # since number of points have to be 100
    if len(points) == 100:
        # convert to binary image
        # display_img(bin_img,"binary image")
        board = IU.get_board(edges, points, model)
        if GU.is_solvable(board):
            generate_result(board)
        else:
            print("Sorry! Failed to process image, enter SUDOKU manually")
            board = IU.enter_board_manually()
            generate_result(board)
    else:
        print("Sorry! Failed to process image, enter SUDOKU manually !! ")
        board = IU.enter_board_manually()
        generate_result(board)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Sudoku solver')
    parser.add_argument("--puzzle", help="Path to Image containing puzzle",
                        default="Images/sample.jpeg", type=str)
    parser.add_argument("--model_path", help="Model for digit recognition",
                        default="model.pt", type=str)
    args = parser.parse_args()
    solve_puzzle_from_image(args.puzzle, args.model_path)
