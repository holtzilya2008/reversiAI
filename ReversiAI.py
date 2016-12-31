
from ReversiPiece import *
from ReversiBoard import *
from GuiBoard import *

# Constants
###############################################################################
AI_Constants = {
	'baseCoeff': 100,
	'totalCells': 144,
	'defaultBestMaxValue': -1000,
	'defaultBestMinValue': 1000
}
###############################################################################

# function - used by the heuristic function h to determine the weight 
# of a specific cell on the board

maxDepth = 3

# Minimax function:
# @param playerAColor - string "black" or "white"
# @param playerBColor - string "black" or "white"
# @param board - an object of class Board for the board representation
# @return - move: a list of two items (coordinates on the board) that the current player should play next
def getBestMinimaxMove(playerAColor, playerBColor, board, depth):
	piecesNumber = board.piecesCount
	if piecesNumber >= 136:
		maxDepth = 8
	else:
		maxDepth = 3
	
	liteBoard = LiteBoard(board,playerAColor,playerBColor)  # translates the guiBoard
	liteBoard.setCorners()
	possibleMoves = liteBoard.getPossMoves(playerAColor, playerBColor)
	if possibleMoves == "No moves":
		return None, None
			
	if depth % 2 == 1:
		
		bestMoveResult = -1000
		for move in possibleMoves:
			liteBoard2 = LiteBoard(board,playerAColor,playerBColor, liteBoard)
			liteBoard2.applyMove(move, playerAColor)
			
			if depth == maxDepth:
				with open("Minimax.txt", "a") as minimaxFile:
					minimaxFile.write("Heuristic function\n")
				moveResult = h(liteBoard2, playerAColor)
			else:
				move2, moveResult = getBestMinimaxMove(playerBColor, playerAColor, liteBoard2, depth+1)
				if move2 == None:
					with open("Minimax.txt", "a") as minimaxFile:
						minimaxFile.write("Heuristic function\n")
					moveResult = h(liteBoard2, playerAColor)
			if moveResult > bestMoveResult:
				bestMoveResult = moveResult
				bestMove = move
				
	else:
	
		bestMoveResult = 1000
		for move in possibleMoves:

			liteBoard2 = LiteBoard(board,playerAColor,playerBColor, liteBoard)
			liteBoard2.applyMove(move, playerAColor)		
			if depth == maxDepth:
				moveResult = h(liteBoard2, playerBColor)
			else:
				move2, moveResult = getBestMinimaxMove(playerBColor, playerAColor, liteBoard2, depth+1)
				if move2 == None:
					with open("Minimax.txt", "a") as minimaxFile:
						minimaxFile.write("Heuristic function\n")
					moveResult = h(liteBoard2, playerBColor)
			if moveResult < bestMoveResult:
				bestMoveResult = moveResult
				bestMove = move
	if depth == 1:
		with open("Minimax.txt", "a") as minimaxFile:
			minimaxFile.write("\n\n\n")
	return bestMove, bestMoveResult

# Alphabeta function:
def getBestAlphaBetaMove(playerAColor, playerBColor, board, depth, alpha, beta):
	piecesNumber = board.piecesCount
	if piecesNumber >= 130:
		maxDepth = 8
	else:
		maxDepth = 3
	if depth % 2 == 1:

		liteBoard = LiteBoard(board,playerAColor,playerBColor)  # translates the guiBoard
		liteBoard.setCorners()
		with open("AlphaBeta.txt", "a") as alphaFile:
			alphaFile.write("Before get possMoves\n")
		possibleMoves = liteBoard.getPossMoves(playerAColor, playerBColor)
		if possibleMoves == "No moves":
			return None, None
		bestMoveResult = alpha
		bestMove = None
		with open("AlphaBeta.txt", "a") as alphaFile:
			alphaFile.write("Possible moves: " + str(len(possibleMoves)) + "\n")
		counter = 1
		#print("Alphabeta 1")
		for move in possibleMoves:
		
			liteBoard2 = LiteBoard(board,playerAColor,playerBColor, liteBoard)
			liteBoard2.applyMove(move, playerAColor)
				
			if depth == maxDepth:
				moveResult = h(liteBoard2, playerAColor)
			else:
				move2, moveResult = getBestAlphaBetaMove(playerBColor, playerAColor, liteBoard2, depth+1, alpha, bestMoveResult)
				if move2 == None:
					moveResult = h(liteBoard2, playerAColor)
			if moveResult >= beta:
				return move, moveResult

			if moveResult > bestMoveResult:
				bestMoveResult = moveResult
				bestMove = move
				
			counter += 1
			
		with open("AlphaBeta.txt", "a") as alphaFile:
			alphaFile.write("\n")

	else:

		liteBoard = LiteBoard(board,playerAColor,playerBColor)  # translates the guiBoard
		liteBoard.setCorners()
		with open("AlphaBeta.txt", "a") as alphaFile:
			alphaFile.write("Before get possMoves\n")
		possibleMoves = liteBoard.getPossMoves(playerAColor, playerBColor)
		if possibleMoves == "No moves":
			return None, None
		bestMoveResult = beta
		bestMove = None
		with open("AlphaBeta.txt", "a") as alphaFile:
			alphaFile.write("Possible moves: " + str(len(possibleMoves)) + "\n")
		counter = 1
		#print("Alphabeta 2")
		for move in possibleMoves:
		
			liteBoard2 = LiteBoard(board,playerAColor,playerBColor, liteBoard)
			liteBoard2.applyMove(move, playerAColor)
			if depth == maxDepth:
				moveResult = h(liteBoard2, playerAColor)
			else:
				move2, moveResult = getBestAlphaBetaMove(playerBColor, playerAColor, liteBoard2, depth+1, bestMoveResult, beta)
				if move2 == None:
					moveResult = h(liteBoard2, playerBColor)
			if moveResult <= alpha:
				return move, moveResult

			if moveResult < bestMoveResult:
				bestMoveResult = moveResult
				bestMove = move
				
				
			counter += 1
			
		with open("AlphaBeta.txt", "a") as alphaFile:
			alphaFile.write("\n")

			
	#print(str(bestMoveResult) + " " + str(bestMove))
	return bestMove, bestMoveResult


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
	
	playerBColor = board.flip(playerAColor)
	
	aPossibleMoves = board.getPossMoves(playerAColor, playerBColor)
	if aPossibleMoves == "No moves":
		aPossibleMoves = 0
	else:
		aPossibleMoves = len(aPossibleMoves)
		
	bPossibleMoves = board.getPossMoves(playerBColor, playerAColor)
	if bPossibleMoves == "No moves":
		bPossibleMoves = 0
	else:
		bPossibleMoves = len(bPossibleMoves)
	
	if aPiecesCount + bPiecesCount >= 138:
	
		piecesCoeff = 0.8
		posMovesCoeff = 0.1
		weightsCoeff = 0.1
		
	elif aPiecesCount + bPiecesCount >= 141:
	
		piecesCoeff = 1
		posMovesCoeff = 0
		weightsCoeff = 0
		
	else:
	
		piecesCoeff = 0.2
		posMovesCoeff = 0.15
		weightsCoeff = 0.65
		
	value = piecesCoeff * (aPiecesCount - bPiecesCount) + weightsCoeff * (aWeights - bWeights) + posMovesCoeff * (aPossibleMoves - bPossibleMoves)
	return value
	