import turtle 
import numpy as np 
import sud_solve 

def text(no,x,y,size,pen) :  
	pen.penup() 
	pen.goto(x,y)
	pen.write(no,align="left",font=('Arial',size,'normal')) # writes the value at the position defined 


def make_board(board,pen,Xboard_start,Yboard_start):
	dimension = 50 		# dimension of each box [ the ones containing numbers ]
	for row in range(10):
		pen.pensize(1)
		if (row%3)==0:
			pen.pensize(3) 	 # bold for rows and columns 
		pen.penup()		
		pen.goto( Xboard_start, Yboard_start - row*dimension )	
		pen.pendown()
		pen.goto( Xboard_start + 9*dimension , Yboard_start-row*dimension ) # make the line 
	for col in range(10):
		pen.pensize(1)    
		if (col%3)==0:
			pen.pensize(3)
		pen.penup()
		pen.goto( Xboard_start + col*dimension, Yboard_start )
		pen.pendown()
		pen.goto( Xboard_start + col*dimension, Yboard_start - 9*dimension ) # make the line 

	for row in range (0,9) :  # enter the values in the board just made 
		for col in range (0,9) :
			if board[row][col] != 0 : 
				text( board[row][col] , Xboard_start + col*dimension + 20, Yboard_start - row*dimension - dimension + 10 , 18,pen)
				# 20 added to row, and 10 to the column to center the number withing a box 


def solve(board,pen,Xboard_start,Yboard_start) : 	
	if not(0 in board.flatten()) : 
		print(" Solved ")
		print(board) 						# puzzle complete 
		return True
	row,col = sud_solve.get_pos(board) # get the first element of the possible array 
	# since the function reaches here, that implies there is at least one 0 in the board 
	remaining = sud_solve.find_possible((row,col),board)
	for no in remaining : 
		if not(sud_solve.check_violation(board,no,row,col)) : 
			board[row][col] = no 
			pen.clear() 
			make_board(board,pen,Xboard_start,Yboard_start)   
			pen.getscreen().update()  # draw the board again 
			if solve(board,pen,Xboard_start,Yboard_start) : 
				return True 
			board[row][col] = 0 # reverse the change made
	return False # since if the function reaches till the end that implies incorrect combination, so backtracking happens  




