#Imports
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

from PySide6.QtWidgets import QWidget, QLineEdit, QLabel, QGridLayout, QMessageBox

################################################################
#Constants
NUMBER_OF_SAMPLES = 50
################################################################
class Window(QDialog):
    def __init__(self, parent=None):
        #inhertiance
        super(Window, self).__init__(parent)

        # setting title
        self.setWindowTitle("Plotter ")

        #attributes
        self.xdata = list(range(NUMBER_OF_SAMPLES))
        self.ydata =  list(range(NUMBER_OF_SAMPLES))

         # create QtWidgets
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

    def __createButtonWidget(self):
        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

    
    def __createLayout(self):
        # create QtWidgets
        self.__createCanvasWidget()
        self.__createButtonWidget()
         # creating a QLineEdit object
        # self.line_edit = QLineEdit()
  
        

    def __setLayout(self):
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        # layout.addWidget(self.line_edit)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self):        
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.xdata, self.ydata, 'r')
        # refresh canvas
        self.canvas.draw()

###############################################################
def run():
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    run()
