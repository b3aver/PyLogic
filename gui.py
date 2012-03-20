#!/usr/bin/python


#from PyQt4 import *
#from PyQt4 import QtGui

#from form import *
import sys
# for file checks
import os.path


from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import *


from PyQt4.QtCore import QString

from MainWindow import Ui_MainWindow
from AboutBox import Ui_Dialog


from propositional.parser import parser as propositional_parser



"""
class Window(QWidget, Ui_MainWindow):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
"""

class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def getInputString(self):
        return str(self.ui.textEditInput.toPlainText())


    def appendOutput(self, string=""):
        outputBox = self.ui.textEditOutput
        outputBox.appendPlainText(QString(string))
        outputBox.moveCursor(QTextCursor.End)
        outputBox.ensureCursorVisible()


    def showAboutBox(self):
        aboutBox = MyAboutBox()
        aboutBox.setModal(False)
        aboutBox.exec_()
        """
        #QMessageBox.about(self, "PyLogic", "Hello World")
        messageBox = QMessageBox(QMessageBox.NoIcon, "PyLogic", "Hello World", QMessageBox.Ok) #, Icon icon, int button0, int button1, int button2, QWidget parent = None, Qt.WindowFlags flags = Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint)
        messageBox.setModal(True)
        #messageBox.exec_()
        messageBox.show()
        """

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
        """
        choice = QMessageBox.Yes
        if os.path.isfile(filename):
            choice=QMessageBox.question(self,
                                        QString("Overwrite"),
                                        QString("The file "
                                                +filename
                                                +" exists.\n\nOverwrite it?"),
                                        QMessageBox.Yes,
                                        QMessageBox.No)
        if choice == QMessageBox.Yes:
        """
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
        #output = formula.cnf()
        output = "CNF not yet implemented."
        self.appendOutput(output.__str__())



class MyAboutBox(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)



class OutputTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        QPlainTextEdit.__init__(self, parent)

"""
class CentralWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

    def showAboutBox(self):
        QMessageBox.about(self, "PyLogic", "Hello World")


class CustomMenu(QMenuBar):
    def __init__(self, parent=None):
        QMenu.__init__(self, parent)

   
""" 

        
        
if __name__ == "__main__":
    #app = QApplication(sys.argv)
    #app = QtGui.QApplication(sys.argv)

    """
    window = Ui_MainWindow()
    #window.show()
    app.setMainWidget(window)
    app.exec_loop()
    """

    app = QApplication(sys.argv)
    window = MyMainWindow() #Window()
    window.show()
    sys.exit(app.exec_())



    """
    w = QtGui.QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()
    
    sys.exit(app.exec_())
    """
