# importing libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from keras.preprocessing.image import load_img
from PyQt5.QtGui import QPixmap
import os.path
import cv2


# window class
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Math expression recogniser")
        # sets main window
        self.setGeometry(100, 100, 1500, 500)
        # creates image object
        self.image = QImage(self.size(), QImage.Format_RGB32)
        # making image color to white
        self.image.fill(Qt.white)

        # drawing flag
        self.drawing = False
        # default color
        self.brushColor = Qt.black
        self.brushSize = 7

        # QPoint object to track the point
        self.lastPoint = QPoint()

        # creates menu bar
        mainMenu = self.menuBar()

        # creating file menu for save
        fileMenu = mainMenu.addMenu("File")

        # creating save action
        saveAction = QAction("Save", self)
        # adding save to the file menu
        fileMenu.addAction(saveAction)
        # adding action to the save
        saveAction.triggered.connect(self.save)

        # creating save action
        deleteAction = QAction("Delete", self)
        # adding save to the file menu
        fileMenu.addAction(deleteAction)
        # adding action to the save
        deleteAction.triggered.connect(self.delete)

        # creating clear action
        clearAction = QAction("Clear", self)
        # adding clear to the file menu
        fileMenu.addAction(clearAction)
        # adding action to the clear
        clearAction.triggered.connect(self.clear)

        self.labelPredResult = QLabel("", self)
        self.labelPredResult.move(70, 36)
        self.labelPredResult.setStyleSheet("background-color: gray")
        self.labelPredResult.setFixedHeight(18)
        self.labelPredLabel = QLabel("Solution", self)
        self.labelPredLabel.move(0,36)
        self.labelExprLabel = QLabel("Expression",self)
        self.labelExprLabel.move(0,56)
        self.labelExpr = QLabel("", self)
        self.labelExpr.move(70, 56)
        self.labelExpr.setStyleSheet("background-color: yellow")
        self.labelExpr.setFixedHeight(18)
        self.labelPredLabel.setStyleSheet("background-color: orange")
        self.labelExprLabel.setStyleSheet("background-color: orange")
        self.labelExprLabel.setFixedWidth(70)
        self.labelPredLabel.setFixedWidth(70)
        self.labelExprLabel.setFixedHeight(18)
        self.labelPredLabel.setFixedHeight(18)
        self.labelExpr.setFixedWidth(200)
        self.labelPredResult.setFixedWidth(200)

        predict = QAction('Predict', self)
        # adding clear to the file menu
        fileMenu.addAction(predict)
        # adding action to the clear
        predict.triggered.connect(self.predict)

        # creating clear action
        eraserAction = QAction("Eraser", self)
        # adding clear to the file menu
        fileMenu.addAction(eraserAction)
        # adding action to the clear
        eraserAction.triggered.connect(self.clear)

        # creating clear action
        penAction = QAction("Pen", self)
        # adding clear to the file menu
        fileMenu.addAction(penAction)
        # adding action to the clear
        penAction.triggered.connect(self.clear)

        self.check1 = QRadioButton(self)
        self.check1.toggled.connect(self.blackColor)
        self.check1.setText("Black pen")
        self.check2 = QRadioButton(self)
        self.check2.toggled.connect(self.whiteColor)
        self.check2.setText("Eraser")
        self.check1.move(0, 0)
        self.check2.move(85, 0)
        self.check5 = QPushButton(self)
        self.check5.pressed.connect(self.usingVariables)
        self.check5.setText("Variables")
        self.check5.move(320, 0)

        self.xBoxL = QLabel(self)
        self.xBox = QLineEdit(self)
        self.xBoxL.setText("Value of x:")
        self.xBox.textChanged.connect(self.textchangedX)
        self.yBoxL = QLabel(self)
        self.yBox = QLineEdit(self)
        self.yBoxL.setText("Value of y:")
        self.yBox.textChanged.connect(self.textchangedY)

        self.check5Clicked = False
        self.xBoxL.hide()
        self.yBoxL.hide()
        self.xBox.hide()
        self.yBox.hide()

        self.comboBox = QComboBox(self)
        self.comboBox.setFixedSize(200,200)
        self.comboBox.setIconSize(QSize(200,200))
        self.comboBox.move(1150, -40)
        self.comboBox.setVisible(True)
        self.notebook = QLabel(self)
        self.notebook.setText("Notebook")
        self.notebook.move(1200, 0)
        self.notebook.setVisible(True)
        self.ifPresent()


    def delete(self):
        import os
        f = open("current_image.txt")
        r = f.read()
        os.remove("./MathExpressions/exp" + r + ".png")
        self.update()
        index = self.comboBox.findText(r)  # find the index of text
        self.comboBox.removeItem(index)
        self.clear()

    # if using variables - a place to assign a value to them appears
    def usingVariables(self):
        if (self.check5Clicked == True):
            self.xBoxL.hide()
            self.yBoxL.hide()
            self.xBox.hide()
            self.yBox.hide()
            self.check5Clicked = False
        else:
            self.yBoxL.move(900, 0)
            self.yBox.move(1000, 0)
            self.xBox.move(750, 0)
            self.xBoxL.move(650, 0)
            self.xBoxL.show()
            self.yBoxL.show()
            self.xBox.show()
            self.yBox.show()
            self.check5Clicked = True

    # changing value of x variable
    def textchangedX(self):
        return self.xBox.text()

    # changing value of y variable
    def textchangedY(self):
        return self.yBox.text()

    def blackColor(self):
        self.brushColor = Qt.black
        self.brushSize = 7

    def whiteColor(self):
        self.brushColor = Qt.white
        self.brushSize = 20
        # method for checking mouse cicks

    # mouse events
    def mousePressEvent(self, event):

        # if left mouse button is pressed
        if event.button() == Qt.LeftButton:
            # make drawing flag true
            self.drawing = True
            # make last point to the point of cursor
            self.lastPoint = event.pos()

    # method for tracking mouse activity

    def mouseMoveEvent(self, event):

        # checking if left button is pressed and drawing flag is true
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            # creating painter object
            painter = QPainter(self.image)

            # set the pen of the painter
            painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

            # draw line from the last point of cursor to the current point
            # this will draw only one step
            painter.drawLine(self.lastPoint, event.pos())

            # change the last point
            self.lastPoint = event.pos()
            # update
            self.update()

    # method for mouse left button release
    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            # make drawing flag false
            self.drawing = False

    # paint event to paint on the white board
    def paintEvent(self, event):
        # create a canvas
        canvasPainter = QPainter(self)

        # draw rectangle on the canvas
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    # display the image picked from the list of images
    def displayPrevious(self, i):
        self.image.load("./MathExpressions/exp" + str(i) + ".png")
        self.update()
        f = open("current_image.txt", "w")
        f.write(str(i))
        f.close()
        self.labelExpr.setText("")
        self.labelPredResult.setText("")

    # adding a new image
    def newButton(self, i):
        icon = QIcon("./MathExpressions/exp" + str(i) + ".png")
        self.comboBox.addItem(icon, str(i))
        # self.comboBox.activated.connect(self.displayPrevious(i))

    # adding to canvas the items in the MathExpressions folder
    def ifPresent(self):
        p = os.path.getsize("./MathExpressions/")
        for i in range(int(p)):
            if(os.path.exists("./MathExpressions/exp" + str(i) + ".png")):
                icon = QIcon("./MathExpressions/exp" + str(i) + ".png")
                self.comboBox.addItem(icon, str(i))
                # adding icon to the given index
                #self.comboBox.addItem(str(i))
                self.comboBox.activated[str].connect(self.displayPrevious)
        f = open("current_image.txt", "w")
        f.write(str(-1))
        f.close()

    # saving the current image
    def save(self):
        import os.path
        i = 0
        found = False
        while (found == False):
            if (os.path.isfile("./MathExpressions/exp" + str(i) + ".png")):
                i = i + 1
            else:
                self.image.save("./MathExpressions/exp" + str(i) + ".png")
                self.displayPrevious(i)
                f = open("current_image.txt", 'w')
                f.write(str(i))
                f.close()
                self.newButton(str(i))
                found = True

    # clear the white board
    def clear(self):
        # make the whole canvas white
        self.image.fill(Qt.white)
        # update
        self.update()

    # predict the expression
    def predict(self):
        import os
        f = open("current_image.txt", 'r')
        n = f.read()
        f.close()
        if (os.path.exists("./MathExpressions/exp" + n + ".png") == False):
            self.labelPredResult.setText("There is no valid maths expression.")
        else:
            from subprocess import call
            call(["python", "Character_Boxing.py"])
            import os
            os.system('python Character_Prediction.py')
            f = open("the_result.txt", "r")
            n = f.read()
            if('x' in n or 'y' in n):
                if('>' not in n):
                    n = self.addAVariable(n)
            try:
                res = eval(n)
                self.labelPredResult.setText(str(res))
            except:
                self.labelPredResult.setText("Not a valid expression.")
            self.labelExpr.setText(n)

    def addAVariable(self,n):
        newString = ""
        if (('y' in n) and ('x' in n)):
            valueX = self.textchangedX()
            valueY = self.textchangedY()
            if(valueX == "" and valueY == ""):
                return n
            for el in n:
                if (el == 'y'):
                    newString = newString + valueY
                    continue
                if (el == 'x'):
                    newString = newString + valueX
                else:
                    newString = newString + el
        elif('x' in n):
            value = self.textchangedX()
            if(value == ""):
                return n
            for el in n:
                if(el == 'x'):
                    newString = newString + value
                else:
                    newString = newString + el
        elif ('y' in n):
            value = self.textchangedY()
            if (value == ""):
                return n
            for el in n:
                if (el == 'y'):
                    newString = newString + value
                else:
                    newString = newString + el
        return newString


App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# showing the window
window.show()

# start the app
sys.exit(App.exec())

app.exec()
