import random
import sys

import matplotlib.pyplot as plt
plt.style.use('dark_background')
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QApplication,
    QDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

################################################################
# Constants
NUMBER_OF_SAMPLES = 50
MAIN_WINDOW_TITLE = "Function‌ ‌Plotter‌"
MAIN_WINDOW_LEFT = 80
MAIN_WINDOW_TOP = 80
MAIN_WINDOW_WIDTH = 600
MAIN_WINDOW_HEIGHT = 600
################################################################


class Plotter(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        # main window
        self.setWindowTitle(MAIN_WINDOW_TITLE)
        self.setGeometry(
            MAIN_WINDOW_LEFT, MAIN_WINDOW_TOP, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT
        )
        self.setStyleSheet("background-color:black;");
        self.autoFillBackground = True

        # attributes
        self.errorMessage = ""
        self.primaryColor =  "#0f9fbf"

        # create
        self.createLayout()

    def createCanvas(self):
        # a figure instance to plot on
        self.figure = plt.figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # create an axis
        self.canvas.axes = self.figure.add_subplot(111)
        self.canvas.axes.set_title("Plot")
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

    def createButton(self):
        # Just some button connected to `plot` method
        self.button = QPushButton("Plot")
        self.button.setShortcut("Ctrl+P")
        self.button.clicked.connect(self.onClick)

    def createInputFunction(self):
        self.InputFunctionLabel = QLabel("f(x)")

        self.InputFunctionField = QLineEdit(self)
        self.InputFunctionField.setPlaceholderText("5*x^3 + 2*x")  # 5 * x ^ 3 + 2 * x

    def createLimits(self):
        self.lowerXLabel = QLabel("lowerX")
        self.lowerXField = QLineEdit(self)
        self.lowerXField.setPlaceholderText("-10")

        self.upperXLabel = QLabel("upperX")
        self.upperXField = QLineEdit(self)
        self.upperXField.setPlaceholderText("10")

    def createLayout(self):
        self.createCanvas()
        self.createButton()
        self.createInputFunction()
        self.createLimits()
        self.styleLayout()

    def styleLayout(self):
        fonts = "font-family:Times; font: bold; color:" + self.primaryColor + "; font-size: 15px"
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.toolbar.setStyleSheet("background-color:" + self.primaryColor + ";")

        layout.addWidget(self.lowerXLabel)
        layout.addWidget(self.lowerXField)
        self.lowerXLabel.setStyleSheet(fonts)
        self.lowerXField.setStyleSheet("background-color:" + self.primaryColor + ";")

        layout.addWidget(self.upperXLabel)
        layout.addWidget(self.upperXField)
        self.upperXLabel.setStyleSheet(fonts)
        self.upperXField.setStyleSheet("background-color:" + self.primaryColor + ";")


        layout.addWidget(self.InputFunctionLabel)
        layout.addWidget(self.InputFunctionField)
        self.InputFunctionLabel.setStyleSheet(fonts)
        self.InputFunctionField.setStyleSheet("background-color:" + self.primaryColor + ";")


        layout.addWidget(self.button)
        self.button.setStyleSheet(fonts)

        self.setLayout(layout)

    def showErrorMessage(self):
        if self.errorMessage != "":     
            QMessageBox.warning(self, "Error!", self.errorMessage, QMessageBox.Ok, QMessageBox.Ok)
            self.errorMessage = ""

    def validateInput(self, fx, ux, lx):
        # validate the input fields
        if fx == "" or ux == "" or lx == "":
            self.errorMessage = "Please, complete all the fields"
            self.showErrorMessage()
            return False

        # validate the limits
        self.lowerX = lx
        self.upperX = ux
        # check for numbers
        try:
            self.upperX = float(self.upperX)
            self.lowerX = float(self.lowerX)
        except:
            self.errorMessage = "Limits Must be Numbers Only"
            self.showErrorMessage()
            return False
        
        # check for inquality
        if self.lowerX > self.upperX:
            self.errorMessage = "Upper limits must be greater than lower limit, we have exchaned them for you!"
            self.upperXField.setText(str(self.lowerX))
            self.lowerXField.setText(str(self.upperX))
            self.lowerX, self.upperX = self.upperX, self.lowerX
        ##################################
        # validate and processthe input function
        self.inputFunction = fx
        try:
            self.inputFunction = self.inputFunction.replace(" ", "")
            self.inputFunction = self.inputFunction.replace("^", "**")
            self.inputFunction = self.inputFunction.replace("sqrt", "np.sqrt")
            self.inputFunction = self.inputFunction.replace("e**", "np.exp")  # e**(x)
            self.inputFunction = self.inputFunction.replace("log", "np.log")  # log(x)
            self.inputFunction = self.inputFunction.replace("sin", "np.sin")
            self.inputFunction = self.inputFunction.replace("cos", "np.cos")
            self.inputFunction = self.inputFunction.replace("tan", "np.tan")
        except:
            self.errorMessage = "Please, enter a valid function, NOT VALID"
        self.showErrorMessage()
        return True
    
    def plot(self, x, y):
        # clear
        self.figure.clear()
        # create an axis
        self.canvas.axes = self.figure.add_subplot(111)
        # plot data
        self.canvas.axes.plot(x, y,  self.primaryColor, label=self.inputFunction)
        # refresh canvas
        self.canvas.draw()

    def onClick(self):
        if self.validateInput(
            self.InputFunctionField.text().lower(),
            self.upperXField.text(),
            self.lowerXField.text(),
        ) == True:
            try:
                x = np.linspace(self.lowerX, self.upperX, NUMBER_OF_SAMPLES)
                y = eval(self.inputFunction)  # divide according to the + then, sum them

                self.plot(x, y)
            except:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Please, enter a valid function",
                    QMessageBox.Ok,
                    QMessageBox.Ok,
                )


def run():
    app = QApplication(sys.argv)

    main = Plotter()
    main.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
