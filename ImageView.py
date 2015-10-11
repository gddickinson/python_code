# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 12:14:34 2015

@author: robot
"""

import sys
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg


class Viewer(QtGui.QMainWindow):
    
    def __init__(self):
        super(Viewer, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        self.ImageView = pg.ImageView()
        self.resize(800,800)
        self.setCentralWidget(self.ImageView)
        self.statusBar()

        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.openDialog)

        saveFile = QtGui.QAction(QtGui.QIcon('save.png'), 'Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.saveDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        
        #self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('ImageView')
        self.show()
        
    def openDialog(self):

        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                '/home')
        
        f = open(fname, 'r')
        
        with f:        
            data = f.read()
            print(data) 
                                

    def saveDialog(self):
        
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file', 
                '/home')
        
        f = open(fname, 'r')
        
        with f:        
            data = f.read()
            print(data) 

        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Viewer()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()