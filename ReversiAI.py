
from ReversiPiece import *
from ReversiBoard import *
from GuiBoard import *

# The function is used by the heuristic function h to determine the weight 
# of a specific cell on the board
def getCellWeight(cell):
	if cell[0] in [0, 11] and cell[1] in [0, 11]:
		# Checking Corners
		return 2
	elif (cell[0] == 1 or cell[0]  == 10) and (cell[1]>0 and cell[1]<11):
		return -1
	elif (cell[1] == 1 or cell[1]  == 10) and (cell[0]>0 and cell[0]<11):
		return -1
	else:
		return 0


# Minimax function:
# @param playerAColor - string "black" or "white"
# @param playerBColor - string "black" or "white"
# @param board - an object of class Board for the board representation
# @return - move: a list of two items (coordinates on the board) that the current player should play next
def getBestMinimaxMove(playerAColor, playerBColor, board, depth):
	# if depth == 5:
	# 	return h(board, playerAColor, playerBColor)
	# if depth % 2 == 1:
	# 	liteBoard = LiteBoard(board,playerAColor,playerBColor)  # translates the guiBoard
	# 	possibleMoves = liteBoard.getPossMoves(playerAColor, playerBColor)
	# 	bestMoveResult = -10000
	# 	for move in possibleMoves:
		
	# 		liteBoard2 = LiteBoard(board,playerAColor,playerBColor, liteBoard.getBoardData())
	# 		liteBoard2.applyMove(move, playerAColor)
	# 		moveResult = getBestMinimaxMove(playerBColor, playerAColor, liteBoard2, depth+1)
	# 		if moveResult > bestMoveResult:
	# 			bestMoveResult = moveResult
	# 			bestMove = move
				
	# else:
	
	# 	liteBoard = LiteBoard(board,playerAColor,playerBColor)  # translates the guiBoard
	# 	possibleMoves = liteBoard.getPossMoves(playerAColor, playerBColor)
	# 	bestMoveResult = 10000
	# 	for move in possibleMoves:
		
	# 		liteBoard2 = LiteBoard(board,playerAColor,playerBColor, liteBoard.getBoardData())
	# 		liteBoard2.applyMove(move, playerAColor)
	# 		moveResult = getBestMinimaxMove(playerBColor, playerAColor, liteBoard2, depth+1)
	# 		if moveResult < bestMoveResult:
	# 			bestMoveResult = moveResult
	# 			bestMove = move
	bestMove = [5,6]
	return bestMove

# Alphabeta function:
def getBestAlphaBetaMove(playerAColor, playerBColor, board, depth, alpha, beta):
    
    return 3
	
	#liteBoard = LiteBoard(board,playerAColor,playerBColor)
    
    #
    #
    #

def h(board, playerAColor, playerBColor):

	aPiecesCount = 0
	bPiecesCount = 0
	pieces = board.pieceCount()
	boardData = board.getBoardData()
	if playerAColor == "white":
		aPiecesCount = pieces[0]
		bPiecesCount = pieceCount[1]
	else:
		aPiecesCount = pieces[1]
		bPiecesCount = pieceCount[0]
		
	corners = board.CheckCorners(playerAColor, playerBColor)
	aPiecesCount += corners[0]
	bPiecesCount += corners[1]
	
	#walls = board.CheckWalls(playerAColor)
		
	
		
	# enemy has opportunity to take some of your cells and\or cells two cells away from corner, corner
	# you are close to wall and enemy cannot take your cells it's good
	# you are close to corner it's not that good(only if enemy cannot take right now your cells)
	# 2 cells from corner it's good
	# take corners is very good
	# it's not a good idea to take some cells near wall if it allows enemy take many of your cells
	# if there is cell between two my cells it's not that good
	# it's good to have cells inside enemy's cells

	# Heuristic functions:
    
    #
    #
    #