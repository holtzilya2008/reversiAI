
from graphics import *
from Button import *
from ReversiBoard import *
from GuiBoard import *
from ReversiPiece import *
from ReversiAI import *
from asyncio.tasks import wait


# This is the main game code
def main():

    # Temporary window to choose player color.
    winTemp = GraphWin("Welcome to Reversi!", 400, 200)
    title = Text(Point(200, 50), "Choose a game mode:")
    title.setSize(24)
    title.setFace('courier')
    title.draw(winTemp)
    b1 = Button(winTemp, Point(80,120), 100, 50, "player vs. AI", 'white')
    b2 = Button(winTemp, Point(200,120), 100, 50, "player vs. player", 'white')
    b3 = Button(winTemp, Point(320,120), 100, 50, "AI vs AI", 'white')
    b1.activate()
    b2.activate()
    b3.activate()
    p = winTemp.getMouse()
    while not (b1.clicked(p) or b2.clicked(p) or b3.clicked(p)):
        p = winTemp.getMouse()
        
    if b1.clicked(p):
        mode = "PVE"
    elif b2.clicked(p):
        mode = "PVP"
    elif b3.clicked(p):
        mode = "EVE"
        
    winTemp.close()
    
    
        #title = Text(Point(200, 50), "Choose a color:")
    winTemp = GraphWin("Welcome to Reversi!", 400, 200)
    if mode == "PVP" or mode == "PVE":
        title.setText("PlayerA: Choose your color:")
        title.setSize(20)
        title.setFace('courier')
        title.draw(winTemp)
        b1 = Button(winTemp, Point(120,120), 130, 50, "", 'white')
        b2 = Button(winTemp, Point(280,120), 130, 50, "", 'black')
        b1.activate()
        b2.activate()
        
        p = winTemp.getMouse()
        while not (b1.clicked(p) or b2.clicked(p)):
            p = winTemp.getMouse()
        
        if b1.clicked(p):
            playerAcolor = 'white'
            playerBcolor = 'black'
        else:
            playerAcolor = 'black'
            playerBcolor = 'white'
    elif mode == "EVE":
        playerAcolor = 'white'
        playerBcolor = 'black'
        title.setText("Choose a strategy for white AI:")
        title.setSize(16)
        title.setFace('courier')
        title.draw(winTemp)
        minimaxB = Button(winTemp, Point(120,120), 100, 50, "Minimax", 'white')
        alphabetaB = Button(winTemp, Point(250,120), 100, 50, "Alpha-Beta", 'white')
        minimaxB.activate()
        alphabetaB.activate()
        
        p = winTemp.getMouse()
        while not (minimaxB.clicked(p) or alphabetaB.clicked(p)):
            p = winTemp.getMouse()
        
        if minimaxB.clicked(p):
            wAIstrategy = "minimax"
        elif alphabetaB.clicked(p):
            wAIstrategy = "alphabeta"
        
        title.setText("Choose a strategy for black AI:")
        title.setSize(16)
        title.setFace('courier')
        #title.draw(winTemp)
        minimaxB = Button(winTemp, Point(120,120), 100, 50, "Minimax", 'white')
        alphabetaB = Button(winTemp, Point(250,120), 100, 50, "Alpha-Beta", 'white')
        minimaxB.activate()
        alphabetaB.activate()
        
        p = winTemp.getMouse()
        while not (minimaxB.clicked(p) or alphabetaB.clicked(p)):
            p = winTemp.getMouse()
        
        if minimaxB.clicked(p):
            bAIstrategy = "minimax"
        elif alphabetaB.clicked(p):
            bAIstrategy = "alphabeta"
    

    winTemp.close()

    # Creates Game object and plays the game
    if mode == "EVE":
        g = Game("white", "black", "EVE", wAIstrategy, bAIstrategy)
    else:    
        g = Game(playerAcolor, playerBcolor, mode)
    
    g.play()

    

class Game:

	def __init__(self, playerAcolor, playerBcolor, mode, wAI="minimax", bAI="minimax"):
		self.playerAcolor = playerAcolor
		self.playerBcolor = playerBcolor
		self.mode = mode
		self.wAIstrategy = wAI
		self.bAIstrategy = bAI
		# Keeps track of the previously played piece (for highlights)
		self.lastPlayedPiece = None

		self.winX = 700
		self.win = GraphWin("Reversi", self.winX, self.winX)
		self.win.setBackground('lightblue')
		self.drawText()
		self.board = Board(self.win, [100,100], 500, self.playerAcolor, self.playerBcolor)

		# References board-data from the board object
		self.bData = self.board.getBoardData()

		# Keeps track of the number of turns
		self.turn = 1

    # Main play function
	def play(self):
		while not self.isGameover():

            # Cycles turns
			if self.turn%2 == 0: 
				color = 'black'
				eColor = 'white'
			else: 
				color = 'white'
				eColor = 'black'

			possMoves = self.board.getPossMoves(color,eColor)

			if possMoves != "No moves":

				self.updateInstruc2(color)
                
                # Payer A move:
				if color == self.playerAcolor:
                    # Highlights all possible moves for player A
                    # and processes the click. 
					if self.mode == "EVE": # AI move
						if self.wAIstrategy == "minimax":
							move, result = getBestMinimaxMove(color,eColor,self.board, 1)
							# print("Mini Max 1 " + str(move) + " " + str(result))
						elif self.wAIstrategy == "alphabeta":
							move, result = getBestAlphaBetaMove(color,eColor,self.board, 1, -1000, 1000)
							# print("Alpha Beta 1 " + str(move) + " " + str(result))
					else: # human move
						for m in possMoves:
							self.board.drawHighlight(m)
						p = self.win.getMouse()
						move = self.processClick(p, possMoves)
					if move == "EXIT PROGRAM":
						break
				else: # Player B move:
					if self.mode == "EVE": # AI move
						if self.bAIstrategy == "minimax":
							move, result = getBestMinimaxMove(color,eColor,self.board, 1)
							# print("Mini Max 2" + str(move) + " " + str(result))
						elif self.bAIstrategy == "alphabeta":
							move, result = getBestAlphaBetaMove(color,eColor,self.board, 1, -1000, 1000)
							# print("Alpha Beta 2 " + str(move) + " " + str(result))
                                
					if self.mode == "PVE": # AI move, but let the user choose the tactics for this move
						winTemp = GraphWin("Select tactic", 400, 150)
						winTemp.anchor('center')
						#winTemp.master.geometry('%dx%d+%d+%d' % (200, 200, 500, 100))
						title = Text(Point(200, 25), "AI's turn: select tactics:")
						title.setSize(18)
						title.setFace('courier')
						title.draw(winTemp)
						minimaxB = Button(winTemp, Point(120,120), 100, 50, "Minimax", 'white')
						alphabetaB = Button(winTemp, Point(250,120), 100, 50, "Alpha-Beta", 'white')
						minimaxB.activate()
						alphabetaB.activate()
						p = winTemp.getMouse()
						while not (minimaxB.clicked(p) or alphabetaB.clicked(p)):
							p = winTemp.getMouse()

						if minimaxB.clicked(p):
							move, result = getBestMinimaxMove(color,eColor,self.board, 1)
							# print("Mini Max 3 " + str(move) + " " + str(result))
						elif alphabetaB.clicked(p):
							move, result = getBestAlphaBetaMove(color,eColor,self.board, 1, -1000, 1000)
							# print("Alpha Beta 3 " + str(move) + " " + str(result))

						winTemp.close()    # close the "Choose tactics" window
                            
                        
					elif self.mode == "PVP": # human move
						for m in possMoves:
							self.board.drawHighlight(m)
						p = self.win.getMouse()
						move = self.processClick(p, possMoves)
						if move == "EXIT PROGRAM":
							break

                # Unhighlights last played piece
				if self.lastPlayedPiece != None:
					self.lastPlayedPiece.unhighlight()
                    
                # Processes the move and then highlights the recently-
                # played piece.
				pc = self.board.processMove(move,color,eColor)
				if pc != None:
					self.lastPlayedPiece = pc
					self.lastPlayedPiece.highlight()
			else:
				message = color.capitalize() + " has no moves!"
				self.updateInstruc2(message, 1)
             

            # Unhighlights squares, updates score and turn.
			self.board.resetHighlights()
			self.updateScore()
			self.turn += 1

		if move == "EXIT PROGRAM":
			pass
		else:
			w = self.determineWinner()
			self.updateInstruc2(w.capitalize() + " wins!", 1)
			p = self.win.getMouse()
			self.win.close()

    # Returns True if there are no open tiles or if no players can move.
	def isGameover(self):
		if self.board.getNumEmptyTiles() == 0:
			return True
		elif not self.hasMoves("white", "black") and not self.hasMoves("black", "white"):
			return True
		return False

	def determineWinner(self):
		sco = self.board.pieceCount()
		if sco[0] > sco[1]:
			return "white"
		return "black"

    # Creates main text and button objects
	def drawText(self):
		self.title = Text(Point(self.winX/2,50), "Reversi")
		self.title.setSize(36)
		self.title.setFace('courier')
		self.title.draw(self.win)
		 
		t = "White : 0, Black: 0"
		self.instruc = Text(Point(self.winX/2, 80), t)
		self.instruc.setSize(15)
		self.instruc.setFace('courier')
		self.instruc.draw(self.win)

		self.quitBtn = Button(self.win, Point(50,50), 40, 30, "Quit", 'red')
		self.quitBtn.activate()

		self.instruc2 = Text(Point(self.winX/2,630), "It is White's turn - please click a valid open square.")
		self.instruc2.setSize(20)
		self.instruc2.setFace('courier')
		self.instruc2.draw(self.win)

	def updateInstruc2(self,color,thing=0):
		if thing == 0:
			message = "It is " + color.capitalize() + "'s turn - please click a valid open square."
			self.instruc2.setText(message)
		else:
			self.instruc2.setText(color)

    # Updates score to text object
	def updateScore(self):
		sco = self.board.pieceCount()
		message = "White: " + str(sco[0]) + ", Black: " + str(sco[1])
		self.instruc.setText(message)

    # Determines if the player has a move
	def hasMoves(self,color,eColor):
		moves = self.board.getPossMoves(color,eColor)
		if moves == "No moves":
			return False
		return len(moves) > 0

    # Handles clicking in the play function
	def processClick(self,p, possMoves):
		finished = False
		winClose = False
		while not finished:
			try:
				if self.quitBtn.clicked(p):
					self.win.close()
					winClose = True
					break
				co = self.board.calcClick(p)
				# Induces error if click is not in possible square
				if co not in possMoves:
					self.updateInstruc2("Square chosen is not valid! Choose again.", 1)
					error = 0 + "0"
				if co != []:
					finished = True
					break
				p = self.win.getMouse()
			except:
				p = self.win.getMouse()
		if winClose:
			return "EXIT PROGRAM"
		return co


        
        
main()
