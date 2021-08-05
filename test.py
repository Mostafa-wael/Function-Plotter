import random
import sys

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
                               QLineEdit, QMessageBox, QPushButton,
                               QVBoxLayout, QWidget)

################################################################
#Constants
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
        self.setGeometry(MAIN_WINDOW_LEFT, MAIN_WINDOW_TOP, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        
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
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.onClick)
    
    def createInputFunction(self):
        self.InputFunctionField = QLineEdit(self)   
        self.InputFunctionField.move(60,60)

        self.InputFunctionLabel = QLabel("f(x)")
        self.InputFunctionLabel.move(20,20)

    def createLayout(self):
        self.createCanvasWidget()
        self.createButton()
        self.createInputFunction()
        self.styleLayout()

    def styleLayout(self):
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.InputFunctionLabel)
        layout.addWidget(self.InputFunctionField)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self, x, y):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # instead of ax.hold(False)
        self.figure.clear()
        self.canvas.axes.cla()  # Clear the canvas.

        # create an axis
        self.canvas.axes = self.figure.add_subplot(111)

        # plot data
        self.canvas.axes.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()

    def onClick(self):
        self.plot(self.x, self.y)

def run():
    app = QApplication(sys.argv)

    main = Plotter()
    main.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    run()
