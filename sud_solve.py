import numpy as np

def solvable(board) : 
	for row in range(9):
		for i in range(1,10) : 
			temp_row = [1 for a in board[row] if a==i]
			temp_column = [1 for a in board[:,row] if a==i]
			if row%3 == 0 : 
				for col in range(0,9,3) :
					temp_sq = [1 for a in board[row:row+3,col:col+3].flatten() if a == i]	
					if temp_sq> 1 : 
						return False
			if len(temp_row) > 1 or len(temp_column) > 1 : 
				return False 
	return True 

def check_violation(board,ele,row,col) : 
	if ele in board[row] or ele in board[:,col] : 
		return True 
	small_sqaure = board[ 3*int(row/3) : 3*int(row/3) + 3 , 3*int(col/3) : 3*int(col/3) + 3 ].flatten()
	if ele in small_sqaure : 
		return True 
	return False # checks whether inserting an element in the board causes a violation 

def find_possible( pos, board) : # returns the values that can possibly occupy a particular position 
	row,col  = pos # unpack 
	possible = [i for i in range(1,10)] 
	small_sqaure = board[ 3*int(row/3) : 3*int(row/3) + 3 , 3*int(col/3) : 3*int(col/3) + 3 ].flatten()   # for the small square
	for i in range(9) :   			
		if(board[row][i] in possible) : 
			possible.remove(board[row][i]) 		# since that number cant appear again... 
		if (board[i][col] in possible) : 
			possible.remove(board[i][col])					
		if(small_sqaure[i] in possible) : 
			possible.remove(small_sqaure[i])
	return possible 

def get_pos(board) : #Returns the positino of the first 0 present in the board [only called if there exists a 0 in a board ]
	for i in range(9) : 
		for j in range(9) : 
			if board[i][j] == 0 : 
				return (i,j) 
