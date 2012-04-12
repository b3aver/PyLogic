#!/usr/bin/python


#from PyQt4 import *
#from PyQt4 import QtGui

#from form import *
import sys
import string
# for file checks
import os.path


from PyQt4.QtCore import Qt, SIGNAL, QString
from PyQt4.QtGui import *


from MainWindow import Ui_MainWindow
from AboutBox import Ui_Dialog


from propositional.parser import parser as propositional_parser
from first_order.parser import parser as firstOrder_parser


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


    def getInputString(self):
        return str(self.ui.textEditInput.toPlainText())


    def appendOutput(self, string=""):
        outputBox = self.ui.textEditOutput
        outputBox.write(string)
        # outputBox.appendPlainText(QString(string))
        # outputBox.moveCursor(QTextCursor.End)
        # outputBox.ensureCursorVisible()


    def showAboutBox(self):
        aboutBox = MyAboutBox()
        aboutBox.setModal(False)
        aboutBox.exec_()


    def openFile(self):
        filename = QFileDialog.getOpenFileName()
        if filename != "":
            if os.path.isfile(filename):
                print "open file"
                f = open(filename, "r")
                self.ui.textEditInput.setPlainText(QString(f.read()))
            else:
                QMessageBox.warning(self,
                                    "File not found!",
                                    "The selected file: "
                                    +filename
                                    +"\n doesn't exists!")


    def saveFile(self):
        filename = QFileDialog.getSaveFileName()
        if filename != "":
            print "save to file"
            f = open(filename, "w")
            f.write(self.getInputString())


    def propositionalCheck(self):
        """Check the sintax of the formula in input"""
        output = propositional_parser.parse(self.getInputString())
        self.appendOutput(output.__str__())

    def propositionalNNF(self):
        """Transform the current formula in input in NNF"""
        formula = propositional_parser.parse(self.getInputString())
        output = formula.nnf() #"NNF not yet implemented."
        self.appendOutput(output.__str__())

    def propositionalCNF(self):
        """Transform the current formula in input in CNF"""
        formula = propositional_parser.parse(self.getInputString())
        output = formula.cnf() #"CNF not yet implemented."
        self.appendOutput(output.__str__())


    def firstOrderCheck(self):
        """Check the sintax of the formula in input"""
        output = firstOrder_parser.parse(self.getInputString())
        self.appendOutput(output.__str__())

        
    def getOutputBox(self):
        return self.ui.textEditOutput

        

class MyAboutBox(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)



class OutputTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        QPlainTextEdit.__init__(self, parent)

    def write(self, txt):
        sys.__stdout__.write(txt+'\n')
        sys.__stdout__.flush()
        #self.appendPlainText(QString(string.rstrip(txt, '\n')))
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(QString(string.rstrip(txt, '\n')+'\n'))
        self.moveCursor(QTextCursor.End)
        self.ensureCursorVisible()

        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow() #Window()
    app.setWindowIcon(QIcon('img/logo.svg'))
    window.show()
    sys.stdout = window.getOutputBox()
    sys.exit(app.exec_())


