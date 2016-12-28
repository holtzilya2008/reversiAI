
from graphics import *

class Piece:

    def __init__(self, win, coords, teamColor):
        self.win = win
        self.l = 500
        self.xCo, self.yCo = 100, 100
        self.teamColor = teamColor
        self.coords = coords
        self.drawCircle(coords)

        if self.teamColor == "white":
            self.enemyColor = "black"
        else:
            self.enemyColor = "white"

    def getEnemyTeam(self):
        return self.enemyColor

        # Draws the main circle graphics object of the piece
    def drawCircle(self, coords):
        self.circ = Circle(Point(self.xCo+coords[0]*self.l/12-self.l/24, self.yCo+self.l-coords[1]*self.l/12+self.l/24), 15)
        self.circ.setFill(self.teamColor)
        self.circ.setWidth(2)
        self.circ.draw(self.win)

    def getTeam(self):
        return self.teamColor

    def setTeam(self, team):
        self.teamColor = team
        
    def getCoords(self):
        return self.coords

        # First changes the pieces stored team and enemy colors,
        # and then changes the fill of the piece to the new color.
    def flip(self):
        if self.teamColor == "white":
            self.teamColor = "black"
            self.enemyColor = "white"
        else:
            self.teamColor = "white"
            self.enemyColor = "black"
        self.circ.setFill(self.teamColor)

        # Highlights for recently-played pieces
    def highlight(self):
        self.circ.setOutline('red')
        self.highlighted = True

    def unhighlight(self):
        self.circ.setOutline('black')
        self.highlighted = False

    def isHighlighted(self):
        return self.highlighted