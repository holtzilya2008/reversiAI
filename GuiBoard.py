
from graphics import *
from Button import *
from ReversiPiece import *

# ---- GUI Board (that can also process moves and stuff) ---- 
class Board:

    def __init__(self, win, coords, length, playerTeam, compTeam):
        self.win = win
        self.xCo, self.yCo = coords[0], coords[1]
        self.l = length
        self.drawBoard(self.l)
        self.highlights = [] # List of active square highlights on board
        self.playerTeam = playerTeam
        self.compTeam = compTeam

        # Initializes the board data. Two-dimensional array that stores
        # the Piece objects (or None) associated with each space.
        self.boardData = []
        self.boardData.append([])
        for i in range(1,13):
            row = []
            row.append([])
            for j in range(1,13):
                row.append(None)
            self.boardData.append(row)
            
        # Creates the first four pieces on the board and saves
        # them in board data
        self.boardData[6][6] = Piece(win, [6,6], 'black')
        self.boardData[7][7] = Piece(win, [7,7], 'black')
        self.boardData[6][7] = Piece(win, [6,7], 'white')
        self.boardData[7][6] = Piece(win, [7,6], 'white')

    def drawBoard(self, length):
        gridX, gridY = self.xCo, self.yCo
        r = Rectangle(Point(self.xCo, self.yCo), Point(self.xCo+length,self.yCo+length))
        r.setFill('white')
        r.draw(self.win)
        lSpace = length/12
        for i in range(13):
            Line(Point(gridX+i*lSpace, gridY), Point(gridX+i*lSpace, gridY+12*lSpace)).draw(self.win)
            Line(Point(gridX, gridY+i*lSpace), Point(gridX+12*lSpace, gridY+i*lSpace)).draw(self.win)

    def drawHighlight(self, coords):
        x = self.xCo+(coords[0]-1)*self.l/12
        y = self.yCo+self.l-(coords[1])*self.l/12
        mod = self.l/12
        rect = Rectangle(Point(x,y),Point(x+mod,y+mod))
        rect.setWidth(12)
        rect.draw(self.win)
        self.highlights.append(rect)

    def resetHighlights(self):
        if len(self.highlights) > 0:
            for h in self.highlights:
                h.undraw()

    # Returns the [x,y] coords of a click on the board
    def calcClick(self, p):
        xMin, xMax = self.xCo, self.xCo+self.l
        yMin, yMax = self.yCo, self.yCo+self.l

        if p.getX()>xMax or p.getX()<xMin or p.getY()>yMax or p.getY()<yMin:
            return []

        x = int((p.getX() - xMin) / (self.l/12) // 1 + 1)
        y = int(12 - (p.getY() - yMin) / (self.l/12) // 1)

        return [x,y]
    
    def getTile(self, coords):
        return self.boardData[coords[0]][coords[1]]

    # Creates a piece, stores it in data, flips all sammiched
    # enemy squares, and returns piece.
    def processMove(self, co, teamColor, enemyColor):
        if co == None:
            return None
        print(co)
        piece = Piece(self.win, co, teamColor)
        self.boardData[co[0]][co[1]] = piece

        for enemyCo in self.getSwappSquares(co, teamColor, enemyColor):
            enemyPiece = self.getTile(enemyCo)
            enemyPiece.flip()                 

        return piece

    def getBoardData(self):
        return self.boardData
    

    # Returns a list of team scores (# of acquired squares/tiles)
    def pieceCount(self):
        wSco = 0
        bSco = 0
        for x in range(1,13):
            for y in range(1,13):
                pc = self.boardData[x][y]
                if pc != None:
                    if pc.getTeam() == "white":
                        wSco += 1
                    else:
                        bSco += 1
        return [wSco,bSco]

    # Returns a list of valid moves
    def getPossMoves(self, teamColor, enemyColor):
        moves = []
        for x in range(1,13):
            for y in range(1,13):
                if self.isValidMove([x,y], teamColor, enemyColor):
                    moves.append([x,y])
        if moves == []:
            return "No moves"
        return moves
 
    # Returns True if the move is an empty square and has more than 1 swap-tiles
    def isValidMove(self, co, tColor, eColor):
        return not (self.boardData[co[0]][co[1]] != None or self.getSwappSquares(co,tColor,eColor) == [])

    # Creates 8 branches of moves around the square, processes each strand,
    # and appends each 'swappable' square coord from each strand. Ultimately
    # returns a list of all enemy square coords that will be flipped.
    def getSwappSquares(self,coords,tColor,eColor):
        
        x,y = coords[0],coords[1]
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
            bMod = self.getOneBranchSwaps(b,tColor,eColor)
            for sq in bMod:
                allSwaps.append(sq)

        return allSwaps  

    # Returns the number of empty tiles on board
    def getNumEmptyTiles(self):
        t = []
        for x in range(1,13):
            for y in range(1,13):
                b = self.boardData[x][y]
                if b == None:
                    t.append([x,y])
        return len(t)

    # Returns all flippable tiles from a certain branch in a list.
    # All square/tile coords must be sandwiched by two team colors.
    def getOneBranchSwaps(self,branchSquares,tColor,eColor):
        swaps = []
        for sq in branchSquares:
            occ = self.getTile(sq)

            try: 
                t = occ.getTeam()
            except: 
                t = ""

            if t == tColor:
                # Successful sandwich
                swaps.append("Roger")
                break
            elif t == "":
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
