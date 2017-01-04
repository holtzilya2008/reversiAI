
import copy
from GuiBoard import *
from ReversiPiece import *


#--------------------------------------------------------------------
# LiteBoard is non-graphical representation of the real board
# The constructor gets the real board and converts it.
# Squares are identified by 3 values:
# Empty = None, White = 1, Black = 0
#--------------------------------------------------------------------

# function - used by the heuristic function h() in reversi AI.py
# to determine the weight of a specific cell on the board
# @param cell : a list of two items (x,y)
# @param leftUpperCorner : *
# @param rightUpperCorner : *
# @param leftBottomCorner : *
# @param rightBottomCorner : *
# 	* four boolean params that tell if the corners are captured
# @returnes : The weight of the given cell on the board
# 
# The Idea: 
# According to the strategy of the Reversi game, there are a better and worse
# positions that the player could be in.
# 1) Taking the Corners: this can be an advantage, because the opponent
#    can't take them back. each corner gives us opportunities to capture 
#    cells on the main diagonal and the side row and column. 
#    The corners will have value +2
# 2) The "cells near the corners" are dangerous, in case the corners 
#	 are not captured yet.
#    If we take for example the corner (1,1), we can are talking about 
#    the cells : (1,2),(2,1),(2,2)
#    The near the corner on the  main diagonal will have a value of -3, 
#    it is the most dangerous. (2,2) in our example.
# 3) Other cells near the corner will have value -1.5. 
#    in our example (1,2), (2,1)
# 4) The cells in the "third level to the corner" are better then other cells
#    (in our example its: [1,3],[2,3],[3,3],[3,2],[3,1]) when we take them, 
#    at the end we leave the oponnent no choise but to step on the dangerous
#    ones (the cells near the corner) 
#    So we gice them a value of +0.5
#
def getCellWeight(cell, leftUpperCorner, rightUpperCorner, leftBottomCorner, rightBottomCorner):
	CellWeights = {
		'CORNER': 8,
		'NEAR_CORNER_DIAGONAL': -12,
		'NEAR_CORNER_OTHER': -6,
		'THIRD_LEVEL_NEAR_CORNER': 2,
		'OTHER_CELLS': 0
	}
	# Checking corners: value +2
	if cell[0] in [1, 12] and cell[1] in [1, 12]:
		return CellWeights['CORNER']

	# Checking the "cells near the corners". 
	# The cells on the main diagonal : 
	# value NEAR_CORNER_DIAGONAL, unless the corner is captured 
	elif cell[0] == 2 and cell[1] == 2:
		if leftUpperCorner == True:
			return CellWeights['OTHER_CELLS']
		else:
			return CellWeights['NEAR_CORNER_DIAGONAL']
	elif cell[0] == 11 and cell[1] == 11:
		if rightBottomCorner == True:
			return CellWeights['OTHER_CELLS']
		else:
			return CellWeights['NEAR_CORNER_DIAGONAL']
	elif cell[0] == 2 and cell[1] == 11:
		if rightUpperCorner == True:
			return CellWeights['OTHER_CELLS']
		else:
			return CellWeights['NEAR_CORNER_DIAGONAL']
	elif cell[0] == 11 and cell[1] == 2:
		if leftBottomCorner == True:
			return CellWeights['OTHER_CELLS']
		else:
			return CellWeights['NEAR_CORNER_DIAGONAL']
			
	# Other cells near the corners: 
	# value NEAR_CORNER_OTHER, unless the corner is captured
	elif cell[0] == 1 and cell[1] == 2:
		if leftUpperCorner == True:
			return CellWeights['OTHER_CELLS']
		else:
			return CellWeights['NEAR_CORNER_OTHER']
	elif cell[0] == 1 and cell[1] == 11:
		if rightUpperCorner == True:
			return CellWeights['OTHER_CELLS']
		else:
			return CellWeights['NEAR_CORNER_OTHER']
	elif cell[0] == 2 and cell[1] == 1:
		if leftUpperCorner == True:
			return CellWeights['OTHER_CELLS']
		else:
			return CellWeights['NEAR_CORNER_OTHER']
	elif cell[0] == 2 and cell[1] == 12:
		if rightUpperCorner == True:
			return CellWeights['OTHER_CELLS']
		else:
			return CellWeights['NEAR_CORNER_OTHER']
	elif cell[0] == 11 and cell[1] == 1:
		if leftBottomCorner == True:
			return CellWeights['OTHER_CELLS']
		else:
			return CellWeights['NEAR_CORNER_OTHER']
	elif cell[0] == 11 and cell[1] == 12:
		if rightBottomCorner == True:
			return CellWeights['OTHER_CELLS']
		else:
			return CellWeights['NEAR_CORNER_OTHER']
	elif cell[0] == 12 and cell[1] == 2:
		if leftBottomCorner == True:
			return CellWeights['OTHER_CELLS']
		else:
			return CellWeights['NEAR_CORNER_OTHER']
	elif cell[0] == 12 and cell[1] == 11:
		if rightBottomCorner == True:
			return CellWeights['OTHER_CELLS']
		else:
			return CellWeights['NEAR_CORNER_OTHER']
			
	# cells in the "third level near the corner"
	# value THIRD_LEVEL_NEAR_CORNER, unless the corner is captured
	elif cell[0] == 3:
		if cell[1] in [1, 2, 3] and leftUpperCorner == False:
			return CellWeights['THIRD_LEVEL_NEAR_CORNER']
		elif cell[1] in [10, 11, 12] and rightUpperCorner == False:
			return CellWeights['THIRD_LEVEL_NEAR_CORNER']
		else:
			return CellWeights['OTHER_CELLS']
	elif cell[0] == 10:
		if cell[1] in [1, 2, 3] and leftBottomCorner == False:
			return CellWeights['THIRD_LEVEL_NEAR_CORNER']
		elif cell[1] in [10, 11, 12] and rightBottomCorner == False:
			return CellWeights['THIRD_LEVEL_NEAR_CORNER']
		else:
			return CellWeights['OTHER_CELLS'] 
	elif cell[1] == 3:
		if cell[0] in [1, 2] and leftUpperCorner == False:
			return CellWeights['THIRD_LEVEL_NEAR_CORNER']
		elif cell[0] in [11, 12] and leftBottomCorner == False:
			return CellWeights['THIRD_LEVEL_NEAR_CORNER']
		else:
			return CellWeights['OTHER_CELLS'] 
	elif cell[1] == 10:
		if cell[0] in [1, 2] and rightUpperCorner == False:
			return CellWeights['THIRD_LEVEL_NEAR_CORNER']
		elif cell[0] in [11, 12] and rightBottomCorner == False:
			return CellWeights['THIRD_LEVEL_NEAR_CORNER']
		else:
			return CellWeights['OTHER_CELLS'] 
	
	# All other cells on the board have the same weight.
	return CellWeights['OTHER_CELLS']

class LiteBoard:

	leftUpperCornerConquered = False
	rightUpperCornerConquered = False
	leftBottomCornerConquered = False
	rightBottomCornerConquered = False


	def __init__(self, board, playerTeam, compTeam, lboard=None):

		self.board = board
		self.playerTeam = playerTeam
		self.compTeam = compTeam
		self.piecesCount = board.piecesCount

		#Copy constructor
		if (lboard != None):
			self.boardData = copy.deepcopy(lboard.boardData)
		# Initializes the board data. Two-dimensional array that stores
		# 0,1 or None values according to Piece objects (or None) at each index of the board
		else:
			self.boardData = []
			self.boardData.append([])
			for i in range(1,13):
				row = []
				row.append([])
				for j in range(1,13):
					if board.boardData[i][j] == None:
						row.append(None)
					elif board.boardData[i][j] == []:
						row.append([])
					elif board.boardData[i][j] == "":
						row.append("")
					else:
						#print("type is " + str(type(board.boardData[i][j])))
						if board.boardData[i][j] == 1:
							row.append(1)
						elif board.boardData[i][j] == 0:
							row.append(0)
						elif board.boardData[i][j].getTeam() == "white":
							row.append(1)
						elif board.boardData[i][j].getTeam() == "black":
							row.append(0)
				self.boardData.append(row)
					
			with open("boardFile.txt", "w") as boardFile:
				for i in range(1, 13):
					for j in range(1, 13):
						boardFile.write(str(self.boardData[i][j]) + " ")
					boardFile.write("\n")
			
		
	def getBoardData(self):
		return self.boardData
	
	# apply move on this board
	def applyMove(self, move, playerColor):
	
		#print(type(move[0]))
		# if type(move[0]) == str:
			# print(move)
			
		if playerColor == "white":
			self.boardData[move[0]][move[1]] = 1
		elif playerColor == "black":
			self.boardData[move[0]][move[1]] = 0
			
		for enemyCo in self.getSwappSquares(move, playerColor):
			self.flip(self.boardData[enemyCo[0]][enemyCo[1]])                

		return self
	
	  
	def getPossMoves(self, teamColor, enemyColor):
		moves = []
		for x in range(1,13):
			for y in range(1,13):
				if self.isValidMove([x,y], teamColor, enemyColor):
					moves.append([x,y])
		if moves == []:
			return "No moves"
		return moves
	
	# Returns the squares ( (i,j) indexes) that will be swapped after applying move to the board
	def getSwappSquares(self,move,playerColor):
		
		x,y = move[0],move[1]
		allSwaps = []
		
		# Iterates counterclockwise starting with the Eastward branch. 
		iterats = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
		for i in iterats:
			
			# 'b' is a list of all squares in a certain branch (includes all empty squares
			# and non-flippable squares)
			b = []
			for j in range(1,13):
				xMod = x + j*i[0]
				yMod = y + j*i[1]
				if not (xMod > 12 or xMod < 1 or yMod > 12 or yMod < 1):
					b.append([xMod,yMod])
					
			# Modifies the 'b' list to include only flippable square coords
			bMod = self.getOneBranchSwaps(b,playerColor)
			for sq in bMod:
				allSwaps.append(sq)

		return allSwaps
	
	# Returns all flippable tiles from a certain branch in a list.
	# All square/tile coords must be sandwiched by two team colors.
	def getOneBranchSwaps(self,branchSquares,playerColor):
	
		# numrows = len(self.boardData)
		# print("numrows " + str(numrows))
		# for i in range(numrows):
			# print("numcols" + str(len(self.boardData[i])))
		
		if playerColor == "white":
			pColor = 1
			eColor = 0
		elif playerColor == "black":
			pColor = 0
			eColor = 1
		swaps = []
		for sq in branchSquares:
			# print(str(sq[0]) + ", " + str(sq[1]))
			occ = self.boardData[sq[0]][sq[1]]

			try: 
				t = occ
			except: 
				t = ""

			if t == pColor:
				# Successful sandwich
				swaps.append("Roger")
				break
			elif t == "" or t == None:
				# Unsuccessful sandwich
				swaps = []
				break
			elif t == eColor:
				swaps.append(sq)
				
		# Final sandwich test. 
		if len(swaps) > 0 and swaps[-1] != "Roger":
			swaps = []
		else:
			swaps = swaps[:-1]
			
		return swaps
	
	
	def isValidMove(self, move, pColor, eColor):
		return not (self.boardData[move[0]][move[1]] != None or self.getSwappSquares(move,pColor) == [])
	
	
	def flip(self, color):
		if color == "white":
			return "black"
		if color == "black":
			return "white"
		if color == 1:
			return 0
		if color == 0:
			return 1
		return color
	
	# FOR DEBUG
	def Print(self):
		for i in range (1,13):
			for j in range (1,13):
				print (self.boardData[i][j], end=" ")
			print("\n")


	def calculateWeights(self, playerColor):
		color = self.GetNumberByColor(playerColor)
		enemyColor = self.flip(color)
		playerWeights = 0
		enemyWeights = 0
		for i in range (1, 13):
			for j in range (1,13):
				if self.boardData[i][j] == color:
					playerWeights += getCellWeight([i,j], self.leftUpperCornerConquered, self.rightUpperCornerConquered, self.leftBottomCornerConquered, self.rightBottomCornerConquered)
				elif self.boardData[i][j] == enemyColor:
					enemyWeights += getCellWeight([i,j], self.leftUpperCornerConquered, self.rightUpperCornerConquered, self.leftBottomCornerConquered, self.rightBottomCornerConquered)

		return [playerWeights, enemyWeights]
		
	def setCorners(self):
		if self.boardData[1][1] == 1 or self.boardData[1][1] == 0:
			self.leftUpperCornerConquered = True
		if self.boardData[1][12] == 1 or self.boardData[1][12] == 0:
			self.rightUpperCornerConquered = True
		if self.boardData[12][1] == 1 or self.boardData[12][1] == 0:
			self.leftBottomCornerConquered = True
		if self.boardData[12][12] == 1 or self.boardData[12][12] == 0:
			self.rightBottomCornerConquered = True
			
	def CheckCorners(self, color):
		count = 0
		eCount = 0
		cornerValue = 12
		if color == "white":
			if self.boardData[1][1] == 1:
				count += cornerValue
			elif self.boardData[1][1] == 0:
				eCount += cornerValue
				
			if self.boardData[1][12] == 1:
				count += cornerValue
			elif self.boardData[1][12] == 0:
				eCount += cornerValue
				
			if self.boardData[12][1] == 1:
				count += cornerValue
			elif self.boardData[12][1] == 0:
				eCount += cornerValue
				
			if self.boardData[12][12] == 1:
				count += cornerValue
			elif self.boardData[12][12] == 0:
				eCount += cornerValue
				
		else:
		
			if self.boardData[1][1] == 0:
				count += cornerValue
			elif self.boardData[1][1] == 1:
				eCount += cornerValue
				
			if self.boardData[1][12] == 0:
				count += cornerValue
			elif self.boardData[1][12] == 1:
				eCount += cornerValue
				
			if self.boardData[12][1] == 0:
				count += cornerValue
			elif self.boardData[12][1] == 1:
				eCount += cornerValue
				
			if self.boardData[12][12] == 0:
				count += cornerValue
			elif self.boardData[12][12] == 1:
				eCount += cornerValue
		
		return count, eCount

	def GetNumberByColor(self, color):
		if color == "white":
			return 1
		else:
			return 0
			
	def pieceCount(self):
		wSco = 0
		bSco = 0
		for x in range(1,13):
			for y in range(1,13):
				pc = self.boardData[x][y]
				if pc != None:
					if pc == 1:
						wSco += 1
					else:
						bSco += 1
		return [wSco,bSco]
