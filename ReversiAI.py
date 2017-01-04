
from ReversiPiece import *
from ReversiBoard import *
from GuiBoard import *
from random import randint

# Constants
###############################################################################
AI_Constants = {
	'PIECES_TO_FULL_SEARCH': 130,
	'FULL_SEARCH_DEPTH': 8,
	'MAX_SEARCH_TREE_DEPTH': 3,
	'INFINITY': 10000,

	#The Heuristic function
	'GAME_BEGIN_PIECES_FACTOR': 0.2,
	'GAME_BEGIN_POSSIBLE_MOVES_FACTOR': 0.15,
	'GAME_BEGIN_WEIGHTS_FACTOR': 0.65,
	'GAME_LATE_PIECES': 138,
	'GAME_LATE_PIECES_FACTOR': 0.8,
	'GAME_LATE_POSSIBLE_MOVES_FACTOR': 0.1,
	'GAME_LATE_WEIGHTS_FACTOR': 0.1,
	'GAME_END_PIECES': 141,
	'GAME_END_PIECES_FACTOR': 1,
	'GAME_END_POSSIBLE_MOVES_FACTOR': 0,
	'GAME_END_WEIGHTS_FACTOR': 0
}

###############################################################################

### Minimax Implementation:
#
# @param playerAColor - string "black" or "white"
# @param playerBColor - string "black" or "white"
# @param board - an object of class Board for the board representation
# @return - move, value: The move object is the cordinates of the next cell
# we should take (x,y) and the calculated value for this move
def getBestMinimaxMove(playerAColor, playerBColor, board, coefficients, currentDepth, maxDepth):

	# determine if we can do "Full search"
	piecesNumber = board.piecesCount
	if piecesNumber >= AI_Constants['PIECES_TO_FULL_SEARCH'] and AI_Constants['PIECES_TO_FULL_SEARCH'] > maxDepth:
		maxDepth = AI_Constants['FULL_SEARCH_DEPTH']


	# Translate the guiBoard to Liteboard
	liteBoard = LiteBoard(board,playerAColor,playerBColor)
	# Set Indicator that tells if the corners are captured or not
	liteBoard.setCorners()
	possibleMoves = liteBoard.getPossMoves(playerAColor, playerBColor)
	if possibleMoves == "No moves":
		return None, None

	# The Maximizer turn			
	if currentDepth % 2 == 1:
		bestMoveResult = -AI_Constants['INFINITY']
		# loop - for each of the possible moves:
		for move in possibleMoves:
			# apply the move on liteBoard2 (auxiliary board)
			liteBoard2 = LiteBoard(board,playerAColor,playerBColor, liteBoard)
			liteBoard2.applyMove(move, playerAColor)
			
			# If we reach the maximum search tree depth, 
			# evaluate the board using the heuristic function h()
			if currentDepth == maxDepth:
				moveResult = h(liteBoard2, playerAColor, coefficients)

			# else - get down in the search tree (recursive call)
			else:
				move2, moveResult = getBestMinimaxMove(playerBColor, playerAColor, liteBoard2, coefficients, currentDepth+1, maxDepth)
				# If we don't have any possible moves in the further search
				# we want to evaluete the board in the current leveland then
				# compare it to the best option we already have
				if move2 == None:
					moveResult = h(liteBoard2, playerAColor, coefficients)
			if moveResult > bestMoveResult:
				bestMoveResult = moveResult
				bestMove = move

			# Adding randomness
			if moveResult == bestMoveResult:
				randomNumber = randint(0,1)
				if randomNumber == 1:
					bestMoveResult = moveResult
					bestMove = move

	# The Minimizer turn		
	else:
		bestMoveResult = AI_Constants['INFINITY']
		# loop - for each of the possible moves:
		for move in possibleMoves:
			# apply the move on liteBoard2 (auxiliary board)
			liteBoard2 = LiteBoard(board,playerAColor,playerBColor, liteBoard)
			liteBoard2.applyMove(move, playerAColor)	

			# If we reach the maximum search tree depth, 
			# evaluate the board using the heuristic function h()	
			if currentDepth == maxDepth:
				moveResult = h(liteBoard2, playerBColor, coefficients)

			# else - get down in the search tree (recursive call)
			else:
				move2, moveResult = getBestMinimaxMove(playerBColor, playerAColor, liteBoard2, coefficients, currentDepth+1, maxDepth)
				# If we don't have any possible moves in the further search
				# we want to evaluete the board in the current level and then
				# compare it to the best option we already have
				if move2 == None:
					moveResult = h(liteBoard2, playerBColor, coefficients)
			if moveResult < bestMoveResult:
				bestMoveResult = moveResult
				bestMove = move

			# Adding randomness
			if moveResult == bestMoveResult:
				randomNumber = randint(0,1)
				if randomNumber == 1:
					bestMoveResult = moveResult
					bestMove = move

	return bestMove, bestMoveResult

### End of Minimax Implementation

### Alphabeta Implementation:
#
# @param playerAColor - string "black" or "white"
# @param playerBColor - string "black" or "white"
# @param board - an object of class Board for the board representation
# @param depth - defines in witch level of the search tree we are now
# @param alpha - best already explored option, along the path to the root
# for the Maximizer
# @param beta - best already explored option, along the path to the root
# for the Minimizer
# @return - move, value: The move object is the cordinates of the next cell
# we should take (x,y) and the calculated value for this move
def getBestAlphaBetaMove(playerAColor, playerBColor, board, coefficients, currentDepth, maxDepth, alpha, beta):

	# determine if we can do "Full search"
	piecesNumber = board.piecesCount
	if piecesNumber >= AI_Constants['PIECES_TO_FULL_SEARCH']:
		maxDepth = AI_Constants['FULL_SEARCH_DEPTH']


	# Translate the guiBoard to Liteboard
	liteBoard = LiteBoard(board,playerAColor,playerBColor)
	# Set Indicator that tells if the corners are captured or not
	liteBoard.setCorners()
	possibleMoves = liteBoard.getPossMoves(playerAColor, playerBColor)
	if possibleMoves == "No moves":
		return None, None

	# The MAximizer turn
	if currentDepth % 2 == 1:

		bestMoveResult = alpha
		bestMove = None

		# loop - for each of the possible moves:
		for move in possibleMoves:
			# apply the move on liteBoard2 (auxiliary board)
			liteBoard2 = LiteBoard(board,playerAColor,playerBColor, liteBoard)
			liteBoard2.applyMove(move, playerAColor)
			
			# If we reach the maximum search tree depth, 
			# evaluate the board using the heuristic function h()	
			if currentDepth == maxDepth:
				moveResult = h(liteBoard2, playerAColor, coefficients)

			# else - get down in the search tree (recursive call)			
			else:
				move2, moveResult = getBestAlphaBetaMove(playerBColor, playerAColor, liteBoard2, coefficients, currentDepth+1, maxDepth, alpha, bestMoveResult)
				# If we don't have any possible moves in the further search
				# we want to evaluete the board in the current level and then
				# compare it to the best option we already have
				if move2 == None:
					moveResult = h(liteBoard2, playerAColor, coefficients)
			
			# AlphaBeta pruning : cut off the branch if the current 
			# result greater then beta
			if moveResult >= beta:
				return move, moveResult

			if moveResult > bestMoveResult:
				bestMoveResult = moveResult
				bestMove = move

			# Adding randomness
			if moveResult == bestMoveResult:
				randomNumber = randint(0,1)
				if randomNumber == 1:
					bestMoveResult = moveResult
					bestMove = move

	# The Minimizer turn
	else:
		bestMoveResult = beta
		bestMove = None
		# loop - for each of the possible moves:
		for move in possibleMoves:
			# apply the move on liteBoard2 (auxiliary board)
			liteBoard2 = LiteBoard(board,playerAColor,playerBColor, liteBoard)
			liteBoard2.applyMove(move, playerAColor)

			# If we reach the maximum search tree depth, 
			# evaluate the board using the heuristic function h()	
			if currentDepth == maxDepth:
				moveResult = h(liteBoard2, playerAColor, coefficients)

			# else - get down in the search tree (recursive call)
			else:
				move2, moveResult = getBestAlphaBetaMove(playerBColor, playerAColor, liteBoard2, coefficients, currentDepth+1, maxDepth, bestMoveResult, beta)
				# If we don't have any possible moves in the further search
				# we want to evaluete the board in the current level and then
				# compare it to the best option we already have
				if move2 == None:
					moveResult = h(liteBoard2, playerBColor, coefficients)

			# AlphaBeta pruning : cut off the branch if the current 
			# result greater then beta
			if moveResult <= alpha:
				return move, moveResult

			if moveResult < bestMoveResult:
				bestMoveResult = moveResult
				bestMove = move

			# Adding randomness
			if moveResult == bestMoveResult:
				randomNumber = randint(0,1)
				if randomNumber == 1:
					bestMoveResult = moveResult
					bestMove = move

	return bestMove, bestMoveResult
### End of Alphabeta Implementation



### The heuristic function h()
# This function is used to evaluate the board in it's current position
# @param board - The Liteboard on witch we make the evaluation
# @param playerAColor - string "black" or "white"
# @return - The value of the board in it's current position
#
# The Idea
# We use 3 parameters:
# 1) The number of ocupied cells of each player
# 2) The number of possible moves of each player
# 3) The weights of the cells on the board (explained in getCellWeight() in 
#    ReversiBoard.py)
#
# Each of thease parameters has it's factor on the evaluation of the board at 
# the current position. As we get closer to the end of the game, the number of 
# cells becomes more important. 
# In the begining and middle of the game, the main factor is the weight of 
# the cells. The logic behind this, is that we should build a strong basis 
# by using valueble cells. More about the weights of the cells is explained 
# in ReversiBoard.py on the getCellWeight() function.
#
# If playerColor, doesn't have any ocupied cells at the current position, the 
# function will return -AI_Constants['INFINITY'] (it means that he lost), on 
# the other hand, if his opponent has no occupied cells, the function will 
# return +AI_Constants['INFINITY'] (it means he won)
#
def h(board, playerAColor, coefficients):

	#Counting black and white pieces on the liteBoard (auxiliary board)
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
	
	#Counting the possible moves of each player
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

	# If tho opponent captured all our pieces, we lose. and the oposite.
	if aPiecesCount == 0:
		return -AI_Constants['INFINITY']
	elif bPiecesCount == 0:
		return AI_Constants['INFINITY']
	
	if aPiecesCount + bPiecesCount >= AI_Constants['GAME_LATE_PIECES']:
	
		piecesCoeff = AI_Constants['GAME_LATE_PIECES_FACTOR']
		posMovesCoeff = AI_Constants['GAME_LATE_POSSIBLE_MOVES_FACTOR']
		weightsCoeff = AI_Constants['GAME_LATE_WEIGHTS_FACTOR']
		
	elif aPiecesCount + bPiecesCount >= AI_Constants['GAME_END_PIECES']:
	
		piecesCoeff = AI_Constants['GAME_END_PIECES_FACTOR']
		posMovesCoeff = AI_Constants['GAME_END_POSSIBLE_MOVES_FACTOR']
		weightsCoeff = AI_Constants['GAME_END_WEIGHTS_FACTOR']
		
	else:
	
		piecesCoeff = coefficients[0]
		posMovesCoeff = coefficients[1]
		weightsCoeff = coefficients[2]
		
	value = piecesCoeff * (aPiecesCount - bPiecesCount) + weightsCoeff * (aWeights - bWeights) + posMovesCoeff * (aPossibleMoves - bPossibleMoves)
	return value
	