

from graphics import *

class Button:

    # Initializes the button constructor, creates the rectangle outline,
    # creates the label, and initializes the button as deactivated.
    def __init__(self, win, center, width, height, label, color):
        self.xMin = center.getX() - width / 2
        self.xMax = center.getX() + width / 2
        self.yMin = center.getY() - height / 2
        self.yMax = center.getY() + height / 2
        rectP1 = Point(self.xMin, self.yMin)
        rectP2 = Point(self.xMax, self.yMax)
        self.rectangle = Rectangle(rectP1, rectP2)
        self.rectColor = color
        self.rectangle.setFill(self.rectColor)
        self.rectangle.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()
        
    def activate(self):
        self.labelColor = 'black'
        self.label.setFill(self.labelColor)
        self.rectangle.setFill(self.rectColor)
        self.rectangle.setWidth(2)
        # Indicates that the button is now active
        self.activeInd = True

    def deactivate(self):
        self.labelColor = 'darkgrey'
        self.label.setFill(self.labelColor)
        self.rectangle.setFill('lightgray')
        self.rectangle.setWidth(1)
        # Indicates that the button is now deactivated
        self.activeInd = False

    # Determines if the button was clicked from an inputted point.
    def clicked(self, pt):
        wasClicked = False
        if (self.xMin <= pt.getX() and self.xMax >= pt.getX()):
            if (self.yMin <= pt.getY() and self.yMax >= pt.getY()):
                if (self.activeInd):
                    wasClicked = True
        return wasClicked

    # Sets the color of the button's rectangle
    def setRectColor(self, color):
        self.rectColor = color
        self.rectangle.setFill(self.rectColor)

    def setLabelColor(self, color):
        self.labelColor = color
        self.label.setFill(self.labelColor)

    # Returns if the button is active or not
    def isActive(self):
        return self.activeInd

    def setLabelSize(self, size):
        self.label.setSize(size)
