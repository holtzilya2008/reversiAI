
from ReversiPiece import *
from ReversiBoard import *
from GuiBoard import *

# Constants
###############################################################################
AI_Constants = {
	'baseCoeff': 100,
	'totalCells': 144
}
###############################################################################

# function - used by the heuristic function h to determine the weight 
# of a specific cell on the board


# Minimax function:
# @param playerAColor - string "black" or "white"
# @param playerBColor - string "black" or "white"
# @param board - an object of class Board for the board representation
# @return - move: a list of two items (coordinates on the board) that the current player should play next
def getBestMinimaxMove(playerAColor, playerBColor, board, depth):
	if depth % 2 == 1:
		liteBoard = LiteBoard(board,playerAColor,playerBColor)  # translates the guiBoard
		possibleMoves = liteBoard.getPossMoves(playerAColor, playerBColor)
		bestMoveResult = -10000
		for move in possibleMoves:
		
			liteBoard2 = LiteBoard(board,playerAColor,playerBColor, liteBoard)
			liteBoard2.applyMove(move, playerAColor)
			move2, moveResult = getBestMinimaxMove(playerBColor, playerAColor, liteBoard2, depth+1)
			if moveResult > bestMoveResult:
				bestMoveResult = moveResult
				bestMove = move
				
	else:
	
		liteBoard = LiteBoard(board,playerAColor,playerBColor)  # translates the guiBoard
		possibleMoves = liteBoard.getPossMoves(playerAColor, playerBColor)
		bestMoveResult = 10000
		for move in possibleMoves:
		
			liteBoard2 = LiteBoard(board,playerAColor,playerBColor, liteBoard)
			liteBoard2.applyMove(move, playerAColor)
			if depth == 4:
				moveResult = h(liteBoard2, playerBColor)
			else:
				move2, moveResult = getBestMinimaxMove(playerBColor, playerAColor, liteBoard2, depth+1)
			if moveResult < bestMoveResult:
				bestMoveResult = moveResult
				bestMove = move
	print(str(bestMoveResult) + " " + str(bestMove))
	return bestMove, bestMoveResult

# Alphabeta function:
def getBestAlphaBetaMove(playerAColor, playerBColor, board, depth, alpha, beta):
    
    return 3
	
	#liteBoard = LiteBoard(board,playerAColor,playerBColor)
    
    #
    #
    #

def h(board, playerAColor):

	
	aPiecesCount = 0
	bPiecesCount = 0
	pieces = board.pieceCount()
	boardData = board.getBoardData()
	if playerAColor == "white":
		aPiecesCount = pieces[0]
		bPiecesCount = pieces[1]
	else:
		aPiecesCount = pieces[1]
		bPiecesCount = pieces[0]
	
	weights = board.calculateWeights(playerAColor)
	aWeights = weights[0]
	bWeights = weights[1]
	
	if aPiecesCount + bPiecesCount >= 120:
	
		coeff = 0.9
		
	else:
	
		coeff = 0.2
		
	value = coeff * (aPiecesCount - bPiecesCount) + (1-coeff) * (aWeights - bWeights)
	return value
	
	
	
	
	
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