import sys
from PyQt4.QtGui import *


class OutputTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        QPlainTextEdit.__init__(self, parent)

    def write(self, txt):
        txt = txt.rstrip('\n')+'\n'
        sys.__stdout__.write(txt)
        # sys.__stdout__.flush()
        #self.appendPlainText(QString(string.rstrip(txt, '\n')))
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(txt)
        self.moveCursor(QTextCursor.End)
        self.ensureCursorVisible()

    def flush(self):
        sys.__stdout__.flush()
