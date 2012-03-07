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

    def output(self, string=""):
        outputBox = self.ui.textEditOutput
        outputBox.insertPlainText(QString(string+"\n"))
        outputBox.ensureCursorVisible()

    def workout(self):
        self.output(self.getInputString())

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
