
import copy
from GuiBoard import *
from ReversiPiece import *


#--------------------------------------------------------------------
# LiteBoard is non-graphical representation of the real board
# The constructor gets the real board and converts it.
# Squares are identified by 3 values:
# Empty = None, White = 1, Black = 0
#--------------------------------------------------------------------

def getCellWeight(cell, leftUpperCorner, rightUpperCorner, leftBottomCorner, rightBottomCorner):
	if cell[0] in [1, 12] and cell[1] in [1, 12]:
		# Checking Corners
		return 2
	# elif (cell[0] == 2 or cell[0]  == 11) and (cell[1]>1 and cell[1]<12):
		# return -1
	# elif (cell[1] == 2 or cell[1]  == 11) and (cell[0]>1 and cell[0]<12):
		# return -1
	elif cell[0] == 2 and cell[1] == 2:
		if leftUpperCorner == True:
			return 0
		else:
			return -3
	elif cell[0] == 11 and cell[1] == 11:
		if rightBottomCorner == True:
			return 0
		else:
			return -3
	elif cell[0] == 2 and cell[1] == 11:
		if rightUpperCorner == True:
			return 0
		else:
			return -3
	elif cell[0] == 11 and cell[1] == 2:
		if leftBottomCorner == True:
			return 0
		else:
			return -3
			
	elif cell[0] == 1 and cell[1] == 2:
		if leftUpperCorner == True:
			return 0
		else:
			return -1.5
	elif cell[0] == 1 and cell[1] == 11:
		if rightUpperCorner == True:
			return 0
		else:
			return -1.5
			
			
	elif cell[0] == 2 and cell[1] == 1:
		if leftUpperCorner == True:
			return 0
		else:
			return -1.5
	elif cell[0] == 2 and cell[1] == 12:
		if rightUpperCorner == True:
			return 0
		else:
			return -1.5
			
			
	elif cell[0] == 11 and cell[1] == 1:
		if leftBottomCorner == True:
			return 0
		else:
			return -1.5
	elif cell[0] == 11 and cell[1] == 12:
		if rightBottomCorner == True:
			return 0
		else:
			return -1.5
			
			
	elif cell[0] == 12 and cell[1] == 2:
		if leftBottomCorner == True:
			return 0
		else:
			return -1.5
	elif cell[0] == 12 and cell[1] == 11:
		if rightBottomCorner == True:
			return 0
		else:
			return -1.5
			
			
	elif cell[0] == 3:
		if cell[1] in [1, 2, 3] and leftUpperCorner == False:
			return 0.5
		elif cell[1] in [10, 11, 12] and rightUpperCorner == False:
			return 0.5
		else:
			return 0
			
	
	elif cell[0] == 10:
		if cell[1] in [1, 2, 3] and leftBottomCorner == False:
			return 0.5
		elif cell[1] in [10, 11, 12] and rightBottomCorner == False:
			return 0.5
		else:
			return 0 
			
			
	elif cell[1] == 3:
		if cell[0] in [1, 2] and leftUpperCorner == False:
			return 0.5
		elif cell[0] in [11, 12] and leftBottomCorner == False:
			return 0.5
		else:
			return 0 
			
			
	elif cell[1] == 10:
		if cell[0] in [1, 2] and rightUpperCorner == False:
			return 0.5
		elif cell[0] in [11, 12] and rightBottomCorner == False:
			return 0.5
		else:
			return 0 
	
	return 0


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


	# def IfThreatened(self, color, cell):
	# 	xIndex = cell[0]
	# 	yIndex = cell[1]
		
	# 	playerNumber = self.GetNumberByColor(color)
	# 	enemyNumber = self.flip(playerNumber)
		
	# 	xMinus = False
	# 	xPlus = False
	# 	yMinus = False
	# 	yPlus = False
		
	# 	if xIndex > 1:
		
	# 		xMinus = True
		
	# 		if self.boardData[xIndex-1, yIndex] == playerNumber:
			
	# 			xIndex -= 2
		
	# 			while xIndex > 0:
		
	# 				if self.boardData[xIndex, yIndex] == enemyNumber:
					
	# 					return True
						
	# 				elif self.boardData[xIndex, yIndex] == playerNumber:
					
	# 					xIndex -= 1
						
	# 				else:
					
	# 					break
						
	# 	xIndex = cell[0]
		
	# 	if xIndex < 12:
		
	# 		xPlus = True
		
	# 		if self.boardData[xIndex+1, yIndex] == playerNumber:
			
	# 			xIndex += 2
		
	# 			while xIndex < 13:
		
	# 				if self.boardData[xIndex, yIndex] == enemyNumber:
					
	# 					return True
						
	# 				elif self.boardData[xIndex, yIndex] == playerNumber:
					
	# 					xIndex += 1
						
	# 				else:
					
	# 					break
						
	# 	xIndex = cell[0]
		
	# 	if yIndex > 1:
		
	# 		yMinus = True
		
	# 		if self.boardData[xIndex, yIndex-1] == playerNumber:
			
	# 			yIndex -= 2
		
	# 			while yIndex > 0:
		
	# 				if self.boardData[xIndex, yIndex] == enemyNumber:
					
	# 					return True
						
	# 				elif self.boardData[xIndex, yIndex] == playerNumber:
					
	# 					yIndex -= 1
						
	# 				else:
					
	# 					break
						
	# 	yIndex = cell[1]
		
	# 	if yIndex < 12:
		
	# 		yPlus = True
		
	# 		if self.boardData[xIndex, yIndex+1] == playerNumber:
			
	# 			yIndex += 2
		
	# 			while yIndex < 13:
		
	# 				if self.boardData[xIndex, yIndex] == enemyNumber:
					
	# 					return True
						
	# 				elif self.boardData[xIndex, yIndex] == playerNumber:
					
	# 					yIndex += 1
						
	# 				else:
					
	# 					break

						
	# 	if xMinus == True:
		
	# 		if yMinus == True:
			
	# 			xIndex = cell[0]
	# 			yIndex = cell[1]
			
	# 			if self.boardData[xIndex-1, yIndex-1] == playerNumber:
			
	# 			xIndex -= 2
	# 			yIndex -= 2
		
	# 			while xIndex > 0 and yIndex > 0:
		
	# 				if self.boardData[xIndex, yIndex] == enemyNumber:
					
	# 					return True
						
	# 				elif self.boardData[xIndex, yIndex] == playerNumber:
					
	# 					xIndex -= 1
	# 					yIndex -= 1
						
	# 				else:
					
	# 					break