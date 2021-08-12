from PySide2 import QtCore
from main import Plotter
import pytest

# pytest test.py
@pytest.fixture # A decorator for a function that must be executed before running the test functions
def appTester(qtbot):
    tester = Plotter()
    tester.testingMode = True
    qtbot.addWidget(tester)
    return tester

def test1_EMPTY_INPUTS(appTester, qtbot): # should start with the word "test"
    qtbot.mouseClick(appTester.button, QtCore.Qt.LeftButton)
    assert appTester.errorMessage == appTester.errorMessageMissingFields

    appTester.InputFunctionField.setText("5*X^2+3*X")
    appTester.lowerXField.setText("-10")
    appTester.upperXField.setText("")
    qtbot.mouseClick(appTester.button, QtCore.Qt.LeftButton)
    assert appTester.errorMessage == appTester.errorMessageMissingFields

    appTester.InputFunctionField.setText("5*X^2+3*X")
    appTester.lowerXField.setText("")
    appTester.upperXField.setText("10")
    qtbot.mouseClick(appTester.button, QtCore.Qt.LeftButton)
    assert appTester.errorMessage == appTester.errorMessageMissingFields

    appTester.InputFunctionField.setText("")
    appTester.lowerXField.setText("-10")
    appTester.upperXField.setText("10")
    qtbot.mouseClick(appTester.button, QtCore.Qt.LeftButton)
    assert appTester.errorMessage == appTester.errorMessageMissingFields

def test2_NON_NUMERIC_LIMITS(appTester, qtbot):
    appTester.lowerXField.setText("xx")
    appTester.upperXField.setText("xx")
    appTester.InputFunctionField.setText("5*X^2+3*X")
    qtbot.mouseClick(appTester.button, QtCore.Qt.LeftButton)
    assert appTester.errorMessage == appTester.errorMessageLimitsNotNumeric

    appTester.lowerXField.setText("-10")
    appTester.upperXField.setText("10x")
    appTester.InputFunctionField.setText("5*X^2+3*X")
    qtbot.mouseClick(appTester.button, QtCore.Qt.LeftButton)
    assert appTester.errorMessage == appTester.errorMessageLimitsNotNumeric

    appTester.lowerXField.setText("-10x")
    appTester.upperXField.setText("10")
    appTester.InputFunctionField.setText("5*X^2+3*X")
    qtbot.mouseClick(appTester.button, QtCore.Qt.LeftButton)
    assert appTester.errorMessage == appTester.errorMessageLimitsNotNumeric

def test3_NON_ORDERED_LIMITS(appTester, qtbot):
    appTester.lowerXField.setText("100")
    appTester.upperXField.setText("0")
    appTester.InputFunctionField.setText("5*X^2+3*X")
    qtbot.mouseClick(appTester.button, QtCore.Qt.LeftButton)
    assert appTester.errorMessage == appTester.errorMessageLimitsNotOrdered

def test4_NON_VALID_FUNCTION(appTester, qtbot):
    appTester.lowerXField.setText("-10")
    appTester.upperXField.setText("10")
    appTester.InputFunctionField.setText("np.sqrt(x)")
    qtbot.mouseClick(appTester.button, QtCore.Qt.LeftButton)
    assert appTester.errorMessageNonValidFunction in appTester.errorMessage  # as the message contains the error description

def test5_VALID_FUNCTION(appTester, qtbot): # normal function
    appTester.lowerXField.setText("-10")
    appTester.upperXField.setText("10")
    appTester.InputFunctionField.setText("5*X^2+3*X")
    qtbot.mouseClick(appTester.button, QtCore.Qt.LeftButton)
    assert appTester.errorMessage == None

def test6_VALID_FUNCTION(appTester, qtbot): # log with -ve values and exp
    appTester.lowerXField.setText("-10")
    appTester.upperXField.setText("10")
    # results in a warning for the log function due to the negative values
    appTester.InputFunctionField.setText("log(x) + e**(x) + 5*x + log(2*x + 30) + e^(5*x)")
    qtbot.mouseClick(appTester.button, QtCore.Qt.LeftButton)
    assert appTester.errorMessage == None

def test7_VALID_FUNCTION(appTester, qtbot): # trignometric
    appTester.lowerXField.setText("-10")
    appTester.upperXField.setText("10")
    appTester.InputFunctionField.setText("sin(x) + 3 * cos(x + 270) + tan(x + 180)")
    qtbot.mouseClick(appTester.button, QtCore.Qt.LeftButton)
    assert appTester.errorMessage == None

def test8_VALID_FUNCTION(appTester, qtbot): # normal function with differnet limits
    appTester.lowerXField.setText("-1e-5")
    appTester.upperXField.setText("0.5")
    appTester.InputFunctionField.setText("5*X^2+3*X")
    qtbot.mouseClick(appTester.button, QtCore.Qt.LeftButton)
    assert appTester.errorMessage == None

def test9_VALID_FUNCTION(appTester, qtbot): # normal function with differnet limits
    appTester.lowerXField.setText("-1e5")
    appTester.upperXField.setText("1e5")
    appTester.InputFunctionField.setText("5*X^2+3*X/3*4-6")
    qtbot.mouseClick(appTester.button, QtCore.Qt.LeftButton)
    assert appTester.errorMessage == None

def test10_VALID_FUNCTION(appTester, qtbot): # extreme function
    appTester.lowerXField.setText("-1e-5")
    appTester.upperXField.setText("0.5")
    appTester.InputFunctionField.setText("sqrt(sin(e^(x^2)) + 180) / 5*cos(log(X + 5) - 270)")
    qtbot.mouseClick(appTester.button, QtCore.Qt.LeftButton)
    assert appTester.errorMessage == None