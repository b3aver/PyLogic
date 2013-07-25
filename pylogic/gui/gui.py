import sys
import string
import os.path  # for file checks

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import *
from PyQt4 import uic

from ..propositional.parser import propositional_parser, propositional_lexer
from ..propositional import resolution as propositional_resolution
from ..first_order.parser import first_order_parser, first_order_lexer



class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = uic.loadUi("pylogic/gui/mainwindow.ui", self)


    def getInputString(self):
        return str(self.ui.textEditInput.toPlainText())


    def appendOutput(self, string=""):
        outputBox = self.ui.textEditOutput
        outputBox.write(string)


    def showAboutBox(self):
        aboutBox = MyAboutBox()
        aboutBox.setModal(False)
        aboutBox.exec_()


    def openFile(self):
        filename = QFileDialog.getOpenFileName()
        if filename != "":
            if os.path.isfile(filename):
                print("open file")
                f = open(filename, "r")
                self.ui.textEditInput.setPlainText(f.read())
            else:
                QMessageBox.warning(self,
                                    "File not found!",
                                    "The selected file: "
                                    +filename
                                    +"\n doesn't exists!")


    def saveFile(self):
        filename = QFileDialog.getSaveFileName()
        if filename != "":
            print("save to file")
            f = open(filename, "w")
            f.write(self.getInputString())


    def propositionalCheck(self):
        """Check the sintax of the formula in input"""
        output = propositional_parser.parse(self.getInputString(),
                                            lexer = propositional_lexer)
        self.appendOutput(output.__str__())

    def propositionalNNF(self):
        """Transform the current formula in input in NNF"""
        formula = propositional_parser.parse(self.getInputString(),
                                             lexer = propositional_lexer)
        output = formula.nnf()
        self.appendOutput(output.__str__())

    def propositionalCNF(self):
        """Transform the current formula in input in CNF"""
        formula = propositional_parser.parse(self.getInputString(),
                                             lexer = propositional_lexer)
        output = formula.cnf()
        self.appendOutput(output.__str__())

    def propositionalResolution(self):
        """Test if the current formula is a tautology, using the resolution
        method"""
        formula = propositional_parser.parse(self.getInputString(),
                                             lexer = propositional_lexer)
        output = propositional_resolution.is_tautology(formula)
        self.appendOutput("%s: %s" % (str(formula), output.__str__()) )


    def firstOrderCheck(self):
        """Check the sintax of the formula in input"""
        output = first_order_parser.parse(self.getInputString(),
                                          lexer = first_order_lexer)
        self.appendOutput(output.__str__())


    def getOutputBox(self):
        return self.ui.textEditOutput



class MyAboutBox(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = uic.loadUi("pylogic/gui/aboutBox.ui", self)



def start():
    app = QApplication(sys.argv)
    window = MyMainWindow() #Window()
    app.setWindowIcon(QIcon('img/logo.svg'))
    window.show()
    sys.stdout = window.getOutputBox()
    sys.exit(app.exec_())
