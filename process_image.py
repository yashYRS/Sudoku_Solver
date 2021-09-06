import cv2
import numpy as np
import pandas as pd


def enter():
    board = []
    for i in range(9):
        row = list(input(" Enter first row "))
        row = list(filter(lambda a: a != ' ', row))
        row = [int(i) for i in row]
        board.append(row)
    return board


def show(img, name):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyWindow(name)


def draw_detected(lines, img):
    for line in lines:
        # ppd and theta of each line:ppd = perpendicular dist, theta = angle
        ppd, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        # drawing lines by following the formula, psin(t) + pcos(t) = line
        x1 = int(a*ppd + 1000*(-b))
        y1 = int(b*ppd + 1000*(a))
        x2 = int(a*ppd - 1000*(-b))
        y2 = int(b*ppd - 1000*(a))
        # draw line on the original to verify whether all lines have been drawn
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    show(img, "detected lines")


def flag_lines(lines, img):
    horizontal = 0
    vertical = 0
    horizontal_list = []
    vertical_list = []
    for line in lines:
        # ppd and theta of each line:ppd = perpendicular dist, theta = angle
        ppd, theta = line[0]
        a = np.cos(theta)
        # since sin(angle) increases from 0 - 90
        b = np.sin(theta)
        # line has to be horizontal
        if b > 0.5:
            # to remove the redundant lines
            if ppd - horizontal > 10:
                horizontal = ppd
                horizontal_list.append((ppd, theta))
        else:                                     # vertical lines
            if ppd - vertical > 10:
                vertical = ppd
                vertical_list.append((ppd, theta))
    print(" Total lines detected -> ", len(horizontal_list) + len(vertical_list))
    return horizontal_list, vertical_list


def get_intersection(h, v):
    points = []
    for horizontal in h:
        ppd1, theta1 = horizontal
        for vertical in v:
            ppd2, theta2 = vertical
            xy = [[np.cos(theta1), np.sin(theta1)], [np.cos(theta2), np.sin(theta2)]]
            ppd = [ppd1, ppd2]
            # point exists at the intersection of the horizontal and vertical line
            point = np.linalg.solve(np.array(xy), np.array(ppd))
            points.append(point)
    return points


def get_board(img, points, model):
    board = []
    for row in range(9):
        row_board = []
        # goes till 9, since last diagonal not needed
        for column in range(9):
            x1, y1 = [int(i)+3 for i in points[row*10 + column]]
            # coordinates of the diagonals of the rectangle
            x2, y2 = [int(i)-3 for i in points[row*10 + column + 11]]
            # area of 1 box, each box has 1 digit
            temp = img[y1:y2, x1:x2]
            # invert the images, to conform with the images produced in Sudoku
            # temp = cv2.bitwise_not(temp)
            if(temp.size != 0):
                # to maintain uniformity with the model's requirements
                temp = cv2.resize(temp, (36, 36))
                show(temp, "adf")
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                # predict the label
                row_board.append(int(model.predict(np.reshape(temp, (1, -1)))))
        print(row_board)
        board.append(row_board)
    show(img, "ADF")
    return board