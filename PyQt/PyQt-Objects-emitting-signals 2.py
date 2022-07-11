#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

In this example, we show how to emit a
signal. 

#==============================================================================
# We create a new signal called closeApp.
# This signal is emitted during a mouse press event.
# The signal is connected to the close() slot of the QtGui.QMainWindow.
# 
# class Communicate(QtCore.QObject):
#     
#     closeApp = QtCore.pyqtSignal()     
# 
# A signal is created with the QtCore.pyqtSignal() as a class attribute of the external Communicate class.
# 
# self.c.closeApp.connect(self.close) 
# The custom closeApp signal is connected to the close() slot of the QtGui.QMainWindow.
# 
# def mousePressEvent(self, event):
#     
#     self.c.closeApp.emit()
# 
# When we click on the window with a mouse pointer, the closeApp signal is emitted.
# The application terminates.
#==============================================================================

author: Jan Bodnar
website: zetcode.com 
last edited: January 2015
"""

import sys
from PyQt4 import QtGui, QtCore


class Communicate(QtCore.QObject):
    
    closeApp = QtCore.pyqtSignal() 
    

class Example(QtGui.QMainWindow):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
        
    def initUI(self):      

        self.c = Communicate()
        self.c.closeApp.connect(self.close)       
        
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Emit signal')
        self.show()
        
        
    def mousePressEvent(self, event):
        
        self.c.closeApp.emit()
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()