import random
import sys
import numpy as np
import matplotlib.pyplot as plt
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
    QMessageBox,
)

################################################################
# Constants
NUMBER_OF_SAMPLES = 50
MAIN_WINDOW_TITLE = "Plotter"
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

        # attributes
        self.x = list(range(NUMBER_OF_SAMPLES))
        self.y = list(range(NUMBER_OF_SAMPLES))

        # create
        self.createLayout()

    def createCanvasWidget(self):
        # a figure instance to plot on
        self.figure = plt.figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # create an axis
        self.canvas.axes = self.figure.add_subplot(111)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

    def createButton(self):
        # Just some button connected to `plot` method
        self.button = QPushButton("Plot")
        self.button.clicked.connect(self.onClick)

    def createInputFunction(self):
        self.InputFunctionLabel = QLabel("f(x)")
        # self.InputFunctionLabel.move(20,20)
        # self.InputFunctionLabel.resize(280,40)

        self.InputFunctionField = QLineEdit(self)
        self.InputFunctionField.setText("‌5*x^3‌ ‌+‌ ‌2*x")
        # self.InputFunctionField.move(60,60)

    def createLimits(self):
        self.lowerXLabel = QLabel("lowerX")
        self.lowerXField = QLineEdit(self)
        self.lowerXField.setText("-10")

        self.upperXLabel = QLabel("upperX")
        self.upperXField = QLineEdit(self)
        self.upperXField.setText("10")

    def createLayout(self):
        self.createCanvasWidget()
        self.createButton()
        self.createInputFunction()
        self.createLimits()
        self.styleLayout()

    def styleLayout(self):
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        layout.addWidget(self.lowerXLabel)
        layout.addWidget(self.lowerXField)
        layout.addWidget(self.upperXLabel)
        layout.addWidget(self.upperXField)

        layout.addWidget(self.InputFunctionLabel)
        layout.addWidget(self.InputFunctionField)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def showErrorMessage(self, str):
        QMessageBox.question(self, "Error", str, QMessageBox.Ok, QMessageBox.Ok)

    def validateInput(self, fx, ux, lx):
        # validate the input fields
        if fx == "" or ux == "" or lx == "":
           self.showErrorMessage("Please, complete all the fields")
        
        # validate the limits
        self.lowerX = lx
        self.upperX = ux
        # check for numbers
        try: 
            self.upperX = float(self.upperX)
            self.lowerX = float(self.lowerX)
        except:
            self.showErrorMessage("Limits Must be Numbers Only")
        # check for inquality
        if self.lowerX >  self.upperX:
            self.showErrorMessage("Upper limits must be greater than lower limit, we have exchaned them for you!")
            self.upperXField.setText(str(self.lowerX))
            self.lowerXField.setText(str(self.upperX))
            self.lowerX, self.upperX = self.upperX, self.lowerX
        ##################################
        # validate and processthe input function
        self.inputFunction = fx
        try:
            self.inputFunction = self.inputFunction.replace(" ", "*")
            self.inputFunction = self.inputFunction.replace("^", "**")
            self.inputFunction = self.inputFunction.replace("sqrt", "np.sqrt")
            self.inputFunction = self.inputFunction.replace("e**", "np.exp")  # e**(x)
            self.inputFunction = self.inputFunction.replace("log", "np.log")  # log(x)
            self.inputFunction = self.inputFunction.replace("sin", "np.sin")
            self.inputFunction = self.inputFunction.replace("cos", "np.cos")
            self.inputFunction = self.inputFunction.replace("tan", "np.tan")
        except:
            QMessageBox.question(
                self, "Error", "Please, enter a valid function,", QMessageBox.Ok, QMessageBox.Ok
            )        

    def plot(self, x, y):
        # clear
        self.figure.clear()
        self.canvas.axes.cla()
        # create an axis
        self.canvas.axes = self.figure.add_subplot(111)
        # plot data
        self.canvas.axes.plot(x, y, "r")
        # refresh canvas
        self.canvas.draw()

    def onClick(self):
        self.validateInput(self.InputFunctionField.text().lower(),  self.upperXField.text(), self.lowerXField.text())
        try:
            x = np.linspace(self.lowerX, self.upperX, NUMBER_OF_SAMPLES)
            y = eval(self.inputFunction)
            self.plot(x, y)
        except:
            QMessageBox.question(
                self, "Error", "Please, enter a valid function", QMessageBox.Ok, QMessageBox.Ok
            )


def run():
    app = QApplication(sys.argv)

    main = Plotter()
    main.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
