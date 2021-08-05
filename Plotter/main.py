# imports
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import  NavigationToolbar2QT as NavigationToolbar
from PySide2.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout

################################################################
# Constants
MAIN_WINDOW_TITLE = "Function‌ ‌Plotter‌"
MAIN_WINDOW_LEFT = 80
MAIN_WINDOW_TOP = 80
MAIN_WINDOW_WIDTH = 600
MAIN_WINDOW_HEIGHT = 600
MAIN_WINDOW_PRIMARY_COLOR = "#0f9fbf"
MAIN_WINDOW_SECONDARY_COLOR = "black"

################################################################
class Plotter(QDialog):
    """ The main window of the Plotter
    """
    def __init__(self, parent=None):
        super().__init__()
        # main window parameters
        self.setWindowTitle(MAIN_WINDOW_TITLE)
        self.setGeometry(MAIN_WINDOW_LEFT, MAIN_WINDOW_TOP, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        self.setStyleSheet("background-color:" + MAIN_WINDOW_SECONDARY_COLOR + ";");
        plt.style.use('dark_background')
        self.autoFillBackground = True

        # attributes
        self.primaryColor =  MAIN_WINDOW_PRIMARY_COLOR

        # error messages and testing
        self.testingMode = False
        self.msgBox = QMessageBox() 
        self.errorMessage = None
        self.errorMessageMissingFields = "Please, complete all the fields"
        self.errorMessageLimitsNotNumeric = "Limits Must be Numbers Only"
        self.errorMessageLimitsNotOrdered = "Upper limits must be greater than lower limit, we have exchanged them for you!"
        self.errorMessageNonValidFunction = "Non-valid function"
        
        # create
        self.__createLayout()

    def __createCanvas(self):
        """ create a new Canvas to show the plot of the function
        """
        # create a canvas and pass a figure to it
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # create an axis
        self.canvas.axes = self.figure.add_subplot(111)
        self.canvas.axes.set_title("Plot")

        # create Navigation widget and pass a Canvas widget and the parent
        self.toolbar = NavigationToolbar(self.canvas, self)

    def __createButton(self):
        """create the plot button
        """
        self.button = QPushButton("Plot") # text diplayed on the button
        self.button.setShortcut("Ctrl+P") # adding a shortcut 
        self.button.clicked.connect(self.__onClick) # connect it to the __onClick function

    def __createInputFunction(self):
        """create the text iput filed for the function and a label to it
        """
        self.InputFunctionLabel = QLabel("f(x)")

        self.InputFunctionField = QLineEdit(self)
        self.InputFunctionField.setPlaceholderText("5*x^3 + 2*x")

    def __createLimits(self):
        """ create the label and the text input field for the limits of (X)
        """
        self.lowerXLabel = QLabel("lower limits of (x)")
        self.lowerXField = QLineEdit(self)
        self.lowerXField.setPlaceholderText("-10")

        self.upperXLabel = QLabel("upper limits of (x)")
        self.upperXField = QLineEdit(self)
        self.upperXField.setPlaceholderText("10")

    def __createLayout(self): 
        """Create the widgets for the main window
        """
        self.__createCanvas()
        self.__createButton()
        self.__createInputFunction()
        self.__createLimits()
        self.__styleLayout()

    def __styleLayout(self): 
        """ style the layout and set them in the proper order
        """
        style = "font-family:Times; font: bold; color:" + self.primaryColor + "; font-size: 15px"
        # set the layout
        layout = QVBoxLayout()

        # canvas 
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.toolbar.setStyleSheet("background-color:" + self.primaryColor + ";")

        # lower limits of X
        layout.addWidget(self.lowerXLabel)
        layout.addWidget(self.lowerXField)
        self.lowerXLabel.setStyleSheet(style)
        self.lowerXField.setStyleSheet("background-color:" + self.primaryColor + ";")

        # upper limits of X
        layout.addWidget(self.upperXLabel)
        layout.addWidget(self.upperXField)
        self.upperXLabel.setStyleSheet(style)
        self.upperXField.setStyleSheet("background-color:" + self.primaryColor + ";")

        # the input function
        layout.addWidget(self.InputFunctionLabel)
        layout.addWidget(self.InputFunctionField)
        self.InputFunctionLabel.setStyleSheet(style)
        self.InputFunctionField.setStyleSheet("background-color:" + self.primaryColor + ";")

        # the plot button
        layout.addWidget(self.button)
        self.button.setStyleSheet(style)

        self.setLayout(layout)

    def __showErrorMessage(self):
        """responsible for showing the error messages
        """
        # show messages if not in the test mode and there is an errorMessage
        if self.testingMode == False and self.errorMessage != None:    
            self.setStyleSheet("QMessageBox{background:  self.primaryColor; }"); # change the color theme in case of an error
            self.msgBox.warning(self, "Error", self.errorMessage, QMessageBox.Ok, QMessageBox.Ok)
            self.setStyleSheet("background-color:" + MAIN_WINDOW_SECONDARY_COLOR + ";"); # return the color theme to its original
            self.errorMessage = None
    def __validateInput(self, fx: str, ux:str, lx:str) -> bool:
        """ used to validate the input fields

        Args:
            fx (str): the input function
            ux (str): upper limits of X
            lx (str): lower limits of X

        Returns:
            bool: whether it is valid or not
        """
        # validate the input fields
        if fx == "" or ux == "" or lx == "":
            self.errorMessage = self.errorMessageMissingFields
            self.__showErrorMessage()
            return False

        # validate the limits
        self.lowerX = lx
        self.upperX = ux
        # check if numeric
        try:
            self.upperX = float(self.upperX)
            self.lowerX = float(self.lowerX)
        except:
            self.errorMessage =  self.errorMessageLimitsNotNumeric
            self.__showErrorMessage()
            return False
        
        # check for inquality
        if self.lowerX > self.upperX:
            self.errorMessage = self.errorMessageLimitsNotOrdered
            self.upperXField.setText(str(self.lowerX))
            self.lowerXField.setText(str(self.upperX))
            self.lowerX, self.upperX = self.upperX, self.lowerX
        ##################################
        # validate and process the input function
        self.inputFunction = fx
        try:
            self.inputFunction = self.inputFunction.replace(" ", "").replace("^", "**").replace("sqrt", "np.sqrt")
            self.inputFunction = self.inputFunction.replace("e**", "np.exp").replace("log", "np.log")  
            self.inputFunction = self.inputFunction.replace("sin", "np.sin").replace("cos", "np.cos").replace("tan", "np.tan")

        except:
            self.errorMessage = self.errorMessageNonValidFunction
        self.__showErrorMessage()
        return True
    
    def plot(self, x: list, y:list):
        """ used to plot a function on the canvas

        Args:
            x (list): the input 
            y (list): the output
        """
        # clear the figure
        self.figure.clear()
        # create an axis
        self.canvas.axes = self.figure.add_subplot(111)
        # plot data
        self.canvas.axes.plot(x, y,  self.primaryColor, label=self.inputFunction)
        # refresh canvas
        self.canvas.draw()

    def __onClick(self):
        """take any needded action after clicking the button
        """
        # check if all inputs are valid
        if self.__validateInput(
            self.InputFunctionField.text().lower(),
            self.upperXField.text(),
            self.lowerXField.text(),
        ) == True:
            try:
                x = np.linspace(self.lowerX, self.upperX) # create the data on the x-axis
                y = eval(self.inputFunction) # evalute the function
                self.plot(x, y) 
            except Exception as e:
                self.errorMessage = self.errorMessageNonValidFunction + ", " + str(e)
                self.__showErrorMessage()

################################################################
def run():
    """ execute the program
    """
    app = QApplication(sys.argv) # create the application

    main = Plotter() # create object of the Plotter -main window-
    main.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
