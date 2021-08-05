# Imports
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QMainWindow

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, 
QLineEdit, QInputDialog)
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QMainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QInputDialog
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
################################################################
# Constants
NUMBER_OF_SAMPLES = 50
MAIN_WINDOW_TITLE = "Plotter"
MAIN_WINDOW_LEFT = 80
MAIN_WINDOW_TOP = 80
MAIN_WINDOW_WIDTH = 1000
MAIN_WINDOW_HEIGHT = 900
# attributes
################################################################
class mainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(MAIN_WINDOW_TITLE)
        self.setGeometry(MAIN_WINDOW_LEFT, MAIN_WINDOW_TOP, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)

        #create widgets
        self.__createLayout()
        self.__setLayout()

    def __createCanvasWidget(self):
        # a figure instance to plot on
        self.figure = plt.figure()
        
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # create an axis
        ax = self.figure.add_subplot(111)
        self.canvas.axes = ax

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
        
    def __createTextBox(self):
        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,40)
        self.textbox.setText("e**X")

    def __createButton(self):
        # Create a button in the window
        self.button = QPushButton('Plot', self)
        self.button.move(20,80)
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)

    def __createLayout(self):
        self.__createCanvasWidget()
        self.__createTextBox()
        self.__createButton()

    def __setLayout(self):
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.textbox)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def __checkInputs(self):
        inputFunc = self.textbox.text().lower()
        inputFunc = inputFunc.replace(" ", "")
        inputFunc = inputFunc.replace("^", "**")
        # inputFunc = inputFunc.replace("sqrt", "np.sqrt")
        inputFunc = inputFunc.replace("e**", "np.exp")
        inputFunc = inputFunc.replace("log", "np.log")
        inputFunc = inputFunc.replace("sin", "np.sin")
        inputFunc = inputFunc.replace("cos", "np.cos")
        inputFunc = inputFunc.replace("tan", "np.tan")
        return inputFunc

    @pyqtSlot()
    def on_click(self):
        inputFunc = self.__checkInputs()
        x = []
        y = []
        try:
            x = np.linspace(0, 100, NUMBER_OF_SAMPLES)
            y = eval(inputFunc)
        except:
            QMessageBox.question(self, 'Error', "You typed: " + inputFunc + " which is wrong!", QMessageBox.Ok, QMessageBox.Ok)
        # try:
        #     len(y)
        # except:
        #     y = np.full(len(x), y)

        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(x, y, 'r')
        # refresh canvas
        self.canvas.draw()

        
            
    @pyqtSlot()
    def plot(self):  
        pass
  
###############################################################
def run():
    app = QApplication(sys.argv)

    main = mainWindow()
    main.show()

    sys.exit(main.exec_())

if __name__ == '__main__':
    run()