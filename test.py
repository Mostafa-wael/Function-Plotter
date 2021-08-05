from PySide2 import QtCore
from main import Plotter
import pytest


@pytest.fixture
def app(qtbot):
    tester = Plotter()
    tester.testingMode = True
    qtbot.addWidget(tester)
    return tester

def test1_EMPTY_INPUTS(app, qtbot): # should start with the word "test"
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)
    assert app.errorMessage == app.errorMessageMissingFields

    app.InputFunctionField.setText("5*X^2+3*X")
    app.lowerXField.setText("-10")
    app.upperXField.setText("")
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)
    assert app.errorMessage == app.errorMessageMissingFields

    app.InputFunctionField.setText("5*X^2+3*X")
    app.lowerXField.setText("")
    app.upperXField.setText("10")
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)
    assert app.errorMessage == app.errorMessageMissingFields

    app.InputFunctionField.setText("")
    app.lowerXField.setText("-10")
    app.upperXField.setText("10")
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)
    assert app.errorMessage == app.errorMessageMissingFields

def test2_NON_NUMERIC_LIMITS(app, qtbot):
    app.lowerXField.setText("xx")
    app.upperXField.setText("xx")
    app.InputFunctionField.setText("5*X^2+3*X")
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)
    assert app.errorMessage == app.errorMessageLimitsNotNumeric

    app.lowerXField.setText("-10")
    app.upperXField.setText("10x")
    app.InputFunctionField.setText("5*X^2+3*X")
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)
    assert app.errorMessage == app.errorMessageLimitsNotNumeric

    app.lowerXField.setText("-10x")
    app.upperXField.setText("10")
    app.InputFunctionField.setText("5*X^2+3*X")
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)
    assert app.errorMessage == app.errorMessageLimitsNotNumeric

def test3_NON_ORDERED_LIMITS(app, qtbot):
    app.lowerXField.setText("100")
    app.upperXField.setText("0")
    app.InputFunctionField.setText("5*X^2+3*X")
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)
    assert app.errorMessage == app.errorMessageLimitsNotOrdered

def test4_NON_VALID_FUNCTION(app, qtbot):
    app.lowerXField.setText("-10")
    app.upperXField.setText("10")
    app.InputFunctionField.setText("np.sqrt(x)")
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)
    assert app.errorMessage == app.errorMessageNonValidFunction

def test5_VALID_FUNCTION(app, qtbot): #normal function
    app.lowerXField.setText("-10")
    app.upperXField.setText("10")
    app.InputFunctionField.setText("5*X^2+3*X")
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)
    assert app.errorMessage == None

def test6_VALID_FUNCTION(app, qtbot): # log with -ve values and exp
    app.lowerXField.setText("-10")
    app.upperXField.setText("10")
    # results in a warning for the log function due to the negative values
    app.InputFunctionField.setText("log(x) + e**(x) + 5*x + log(2*x + 30) + e^(5*x)")
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)
    assert app.errorMessage == None

def test7_VALID_FUNCTION(app, qtbot): # trignometric
    app.lowerXField.setText("-10")
    app.upperXField.setText("10")
    app.InputFunctionField.setText("sin(x) + 3 * cos(x + 270) + tan(x + 180)")
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)
    assert app.errorMessage == None

def test8_VALID_FUNCTION(app, qtbot): #normal function with differnet limits
    app.lowerXField.setText("-1e-5")
    app.upperXField.setText("0.5")
    app.InputFunctionField.setText("5*X^2+3*X")
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)
    assert app.errorMessage == None

def test8_VALID_FUNCTION(app, qtbot): #normal function with differnet limits
    app.lowerXField.setText("-1e5")
    app.upperXField.setText("1e5")
    app.InputFunctionField.setText("5*X^2+3*X")
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)
    assert app.errorMessage == None

def test9_VALID_FUNCTION(app, qtbot): # extreme function
    app.lowerXField.setText("-1e-5")
    app.upperXField.setText("0.5")
    app.InputFunctionField.setText("sqrt(sin(e^(x^2)) + 180) / 5*cos(log(X + 5) - 270)")
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)
    assert app.errorMessage == None