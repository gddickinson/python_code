# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 12:14:34 2015

@author: george
"""
from __future__ import (absolute_import, division,print_function, unicode_literals)
from future.builtins import (bytes, dict, int, list, object, range, str, ascii, chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
import time
tic=time.time()
import os, sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import tifffile
import json
import re

from skimage import io
from skimage.color import rgb2gray
import copy
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb

from PyQt4.QtCore import *
from PyQt4.QtGui import *


if sys.version_info[:2]<(2,5):
    def partial(func,arg):
        def callme():
            return func(arg)
        return callme
else:
    from functools import partial



class ZeroSpinBox(QSpinBox):

    zeros = 0

    def __init__(self, parent = None):
        super(ZeroSpinBox, self).__init__(parent)
        self.connect(self,SIGNAL("valueChanged(int)"),self.checkzero)

    def checkzero(self):
        if self.value() == 0:
            self.zeros +=1
            self.emit(SIGNAL("atzero"),self.zeros)


class Form(QDialog):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)

        self.filterBox=QComboBox()
        self.filterBox.addItem("No Filter")

        self.SpinBox1=QDoubleSpinBox()
        self.SpinBox1.setRange(0,255)
        self.SpinBox1.setValue(1)

        self.SpinBox2=QDoubleSpinBox()
        self.SpinBox2.setRange(0,255)
        self.SpinBox2.setValue(255)

        self.SpinBox3=QDoubleSpinBox()
        self.SpinBox3.setRange(0,255)
        self.SpinBox3.setValue(1)

        self.SpinBox4=QDoubleSpinBox()
        self.SpinBox4.setRange(0,255)
        self.SpinBox4.setValue(255)

        self.SpinBox5=QDoubleSpinBox()
        self.SpinBox5.setRange(0,255)
        self.SpinBox5.setValue(1)

        self.SpinBox6=QDoubleSpinBox()
        self.SpinBox6.setRange(0,255)
        self.SpinBox6.setValue(255)

        self.filterLabel=QLabel("No Filter")
        self.filterFlag = 'No Filter'

        self.dial = QDial()
        self.dial.setNotchesVisible(True)
        self.zerospinbox = ZeroSpinBox()

        self.sld1 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld1.setRange(0,255)
        self.sld1.setTickPosition(QSlider.TicksBelow)
        self.sld1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld1.setGeometry(30, 40, 100, 30)

        self.sld2 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld2.setRange(0,255)
        self.sld2.setTickPosition(QSlider.TicksBelow)
        self.sld2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld2.setValue(255)
        self.sld2.setGeometry(30, 40, 100, 30)

        self.sld3 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld3.setRange(0,255)
        self.sld3.setTickPosition(QSlider.TicksBelow)
        self.sld3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld3.setGeometry(30, 40, 100, 30)

        self.sld4 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld4.setRange(0,255)
        self.sld4.setTickPosition(QSlider.TicksBelow)
        self.sld4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld4.setValue(255)
        self.sld4.setGeometry(30, 40, 100, 30)

        self.sld5 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld5.setRange(0,255)
        self.sld5.setTickPosition(QSlider.TicksBelow)
        self.sld5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld5.setGeometry(30, 40, 100, 30)

        self.sld6 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld6.setRange(0,255)
        self.sld6.setTickPosition(QSlider.TicksBelow)
        self.sld6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld6.setValue(255)
        self.sld6.setGeometry(30, 40, 100, 30)

        self.button1 = QPushButton("ON")
        self.onFlag = False

        layout = QHBoxLayout()
        layout.addWidget(self.dial)
        layout.addWidget(self.zerospinbox)
        layout.addWidget(self.button1)
        layout.addWidget(self.sld1)
        layout.addWidget(self.sld2)
        layout.addWidget(self.SpinBox1)
        layout.addWidget(self.SpinBox2)
        layout.addWidget(self.sld3)
        layout.addWidget(self.sld4)
        layout.addWidget(self.SpinBox3)
        layout.addWidget(self.SpinBox4)
        layout.addWidget(self.sld5)
        layout.addWidget(self.sld6)
        layout.addWidget(self.SpinBox5)
        layout.addWidget(self.SpinBox6)

        self.setLayout(layout)

        self.connect(self.dial,SIGNAL("valueChanged(int)"), self.zerospinbox.setValue)
        self.connect(self.zerospinbox,SIGNAL("valueChanged(int)"),self.dial.setValue)
        self.connect(self.zerospinbox,SIGNAL("atzero"),self.announce)
        self.connect(self.button1,SIGNAL("clicked()"),self.button_1)

        self.connect(self.sld1,SIGNAL("valueChanged(int)"), self.slider_1)
        self.connect(self.sld1,SIGNAL("valueChanged(int)"),self.SpinBox1.setValue)

        self.connect(self.sld2,SIGNAL("valueChanged(int)"), self.slider_2)
        self.connect(self.sld2,SIGNAL("valueChanged(int)"),self.SpinBox2.setValue)

        self.connect(self.sld3,SIGNAL("valueChanged(int)"), self.slider_3)
        self.connect(self.sld3,SIGNAL("valueChanged(int)"),self.SpinBox3.setValue)

        self.connect(self.sld4,SIGNAL("valueChanged(int)"), self.slider_4)
        self.connect(self.sld4,SIGNAL("valueChanged(int)"),self.SpinBox4.setValue)

        self.connect(self.sld5,SIGNAL("valueChanged(int)"), self.slider_5)
        self.connect(self.sld5,SIGNAL("valueChanged(int)"),self.SpinBox5.setValue)

        self.connect(self.sld6,SIGNAL("valueChanged(int)"), self.slider_6)
        self.connect(self.sld6,SIGNAL("valueChanged(int)"),self.SpinBox6.setValue)




    def button_1(self):
        if self.onFlag == False:
            self.onFlag = True
            self.button1.setText("ON")
        else:
            self.onFlag = False
            self.button1.setText("OFF")


    def slider_1(self):
        print ("Not implemented")

    def slider_2(self):
        print ("Not implemented")

    def slider_3(self):
        print ("Not implemented")

    def slider_4(self):
        print ("Not implemented")

    def slider_5(self):
        print ("Not implemented")

    def slider_6(self):
        print ("Not implemented")

    def announce(self,zeros):
        print ("ZeroSpinBox has been at zero %d times" %zeros)

    def updateUi(self):
        self.filterType = unicode(self.filterBox.currentText())
        self.filterLabel.setText(self.filterType)
        self.filterFlag = str(self.filterType)


class Viewer(QtGui.QMainWindow):

    def __init__(self):
        super(Viewer, self).__init__()

        self.initUI()


    def initUI(self):

        self.ImageView = pg.ImageView(view=pg.PlotItem())
        self.resize(800,800)
        self.setCentralWidget(self.ImageView)
        self.statusBar()

        openImage = QtGui.QAction(QtGui.QIcon('open.png'), 'Open image', self)
        openImage.setShortcut('Ctrl+O')
        openImage.setStatusTip('Open new Image')
        openImage.triggered.connect(self.openDialog)

        saveFile = QtGui.QAction(QtGui.QIcon('save.png'), 'Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.saveDialog)

        rotateCounter = QtGui.QAction(QtGui.QIcon('open.png'), 'Rotate Counterclock', self)
        rotateCounter.setShortcut('Ctrl+9')
        rotateCounter.setStatusTip('Rotate Counterclock')
        rotateCounter.triggered.connect(self.rotateImageCounter)

        rotateClock = QtGui.QAction(QtGui.QIcon('open.png'), 'Rotate Clock', self)
        rotateClock.setShortcut('Ctrl+0')
        rotateClock.setStatusTip('Rotate Clock')
        rotateClock.triggered.connect(self.rotateImageClock)

        flipLR = QtGui.QAction(QtGui.QIcon('open.png'), 'Flip Vertical', self)
        flipLR.setShortcut('Ctrl+7')
        flipLR.setStatusTip('Flip vertical')
        flipLR.triggered.connect(self.flipImageLR)

        flipUD = QtGui.QAction(QtGui.QIcon('open.png'), 'Flip Horizontal', self)
        flipUD.setShortcut('Ctrl+8')
        flipUD.setStatusTip('Flip horizontal')
        flipUD.triggered.connect(self.flipImageUD)

        quitApp = QtGui.QAction(QtGui.QIcon('save.png'), 'Quit Now', self)
        quitApp.setShortcut('Ctrl+Q')
        quitApp.setStatusTip('Quit')
        quitApp.triggered.connect(self.quitDialog)

        activateExaminer = QtGui.QAction(QtGui.QIcon('save.png'), 'ROI Examiner', self)
        activateExaminer.setShortcut('Ctrl+E')
        activateExaminer.setStatusTip('Start Examiner')
        activateExaminer.triggered.connect(self.startROIExaminer)

        activateConsole = QtGui.QAction(QtGui.QIcon('save.png'), 'ROI Console', self)
        activateConsole.setShortcut('Ctrl+R')
        activateConsole.setStatusTip('Start Console')
        activateConsole.triggered.connect(self.initConsole)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openImage)
        fileMenu.addAction(saveFile)

        fileMenu1 = menubar.addMenu('&Transform Image')
        fileMenu1.addAction(rotateCounter)
        fileMenu1.addAction(rotateClock)
        fileMenu1.addAction(flipLR)
        fileMenu1.addAction(flipUD)

        fileMenu2 = menubar.addMenu("&Quit")
        fileMenu2.addAction(quitApp)

        fileMenu3 = menubar.addMenu('&ROI Examiner')
        fileMenu3.addAction(activateExaminer)
        fileMenu3.addAction(activateConsole)


#        fileMenu3 = menubar.addMenu('&Analysis')
#        fileMenu3.addAction(analysis1)

        #self.setGeometry(300, 300, 350, 300)

        self.setWindowTitle('ImageView')

        self.initROI()
        self.show()

    def initConsole(self):
        self.console = Form()
        #self.console.connect(self.console.button1,SIGNAL("clicked()"),self.testPrint)
        self.console.connect(self.console.button1,SIGNAL("clicked()"),self.detect_coverBoard)
        self.console.show()


    def testPrint(self):
        print("test passed")

    def initROI(self):

        def updateROI(roi):
            self.roiImg = self.ImageView.getProcessedImage()
            arr = np.array(self.roiImg)
            x = self.roi1.getArrayRegion(arr, self.ImageView.getImageItem())

            global roi_origin, roi_size
            roi_origin = self.roi1.pos()
            roi_size = self.roi1.size()

            self.roiImg = x


        def rectROI(self):
            self.roiImg = []
            self.roi1 = pg.RectROI([40, 40], [40, 40], pen=(0,9))
            self.roi1.addRotateHandle([1,0], [0.5, 0.5])
            self.roi1.sigRegionChanged.connect(updateROI)
            self.ImageView.addItem(self.roi1)
            return

        rectROI(self)


    def txt2dict(metadata):
        meta=dict()
        try:
            metadata=json.loads(metadata.decode('utf-8'))
            return metadata
        except ValueError: #if the metadata isn't in JSON
            pass
        for line in metadata.splitlines():
            line=re.split('[:=]',line)
            if len(line)==1:
                meta[line[0]]=''
            else:
                meta[line[0].lstrip().rstrip()]=line[1].lstrip().rstrip()
        return meta


    def open_image(self, filename):
        self.statusBar().showMessage('Loading {}'.format(os.path.basename(filename)))
        t=time.time()
        global newimg
        newimg = io.imread(filename)
        newimg = np.rot90(newimg,k=1)
        newimg = np.flipud(newimg)
        self.statusBar().showMessage('{} successfully loaded ({} s)'.format(os.path.basename(filename), time.time()-t))
        return newimg


    def openDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Image file',
                '/home')
        filename=str(filename)
        if filename=='':
            return False
        else:
            data = self.open_image(filename)
            print(len(data.shape))
            self.ImageView.setImage(data)


    def saveDialog(self):

        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file',
                '/home')

        f = open(fname, 'r')

        with f:
            data = f.read()
            print(data)

    def rotateImageCounter(self):
        img = self.ImageView.getProcessedImage()
        img = np.rot90(img,k=3)
        self.ImageView.setImage(img)
        return

    def rotateImageClock(self):
        img = self.ImageView.getProcessedImage()
        img = np.rot90(img,k=1)
        self.ImageView.setImage(img)
        return

    def flipImageLR(self):
        img = self.ImageView.getProcessedImage()
        img = np.fliplr(img)
        self.ImageView.setImage(img)
        return

    def flipImageUD(self):
        img = self.ImageView.getProcessedImage()
        img = np.flipud(img)
        self.ImageView.setImage(img)
        return

    def startROIExaminer(self):
        try:
            #imgROI = self.ImageView.getProcessedImage()
            self.imgROI = self.roiImg
        except:
            print('No image loaded')
            return

        ## create GUI
        self.app = QtGui.QPixmap()
        self.w = pg.GraphicsWindow(size=(500,400), border=True)
        self.w.setWindowTitle('ROI Examiner')
        self.w1 = self.w.addLayout(row=0, col=0)

        self.v1a = self.w1.addViewBox(row=0, col=0, lockAspect=True)
        self.img = pg.ImageItem(self.imgROI)
        self.v1a.addItem(self.img)

        while True:
            self.v1a.removeItem(self.img)
            self.imgROI = self.roiImg
            self.imgROI = np.fliplr(self.imgROI)
            self.img = pg.ImageItem(self.imgROI)

            self.v1a.addItem(self.img)

            if QtCore.QCoreApplication.instance() != None: #something is wrong here - change this
                app.closeAllWindows() # this is giving an error - but removing if statement causes ROIexaminer to fail!!
                break

        return

####################################################################################################
    def detect_coverBoard(self):
        print('start analysis')
        #set up arrays
        global newimg, roi_origin, roi_size
        image = newimg

        image_original = copy.deepcopy(image)
        image_board = copy.deepcopy(image)
        image_other = copy.deepcopy(image)

        #set image size variables
        image_x_origin = int(roi_origin[0])
        image_y_origin = int(roi_origin[1])

        #print("origin ",image_x_origin,image_y_origin)

        image_x_end = image_x_origin + int(roi_size[0])
        image_y_end = image_y_origin + int(roi_size[1])

        #print ("end ", image_x_end, image_y_end)

        center_x = int(roi_size[0]/2)
        center_y = int(roi_size[1]/2)

        #image array index
        r = 0
        g = 1
        b = 2

#        # colour settings
#        red = [255,0,0]
#        green = [0,255,0]
#        blue = [0,0,255]
#        black = [0,0,0]
#        white = [255,255,255]

        #pixel countvariables
        board_pixel = 0
        other_pixel = 0

        #filter variables
        red_min = 115
        red_max = 210
        green_min = 40
        green_max = 110
        blue_min = 15
        blue_max = 75


         #loop through all pixels in image and set pixel to maximum channel value - count pixels in each channel
        for x in range (image_x_origin,image_x_end):
            for y in range (image_y_origin,image_y_end):
                #pixels with equivalent values
                if image[x,y][b] == image[x,y][g]:
                    image_other[x,y] = 0
                    image_board[x,y] = 255
                    other_pixel += 1

                #count board pixels
                elif image[x,y][r] > image[x,y][g] and image[x,y][r] > image[x,y][b] and image[x,y][g]/image[x,y][b] > 1.2 and image[x,y][g]/image[x,y][b] < 3 and image[x,y][r]/image[x,y][g] > 1.4 and image[x,y][r]/image[x,y][g] < 2.8:

                    if image[x,y][r] > red_min and image[x,y][r] < red_max and image[x,y][g] > green_min and image[x,y][g] < green_max and image[x,y][b] > blue_min and image[x,y][b] < blue_max:

                        image_board[x,y] = 0
                        image_other[x,y] = 255
                        board_pixel += 1


                    else:
                        image_board[x,y] = 255
                        image_other[x,y] = 0
                        other_pixel += 1

                #count green pixels
                elif image[x,y][g] > image[x,y][r] and image[x,y][g] > image[x,y][b]:
                    image_other[x,y] = 0
                    image_board[x,y] = 255
                    other_pixel += 1

                #count blue pixels
                elif image[x,y][b] > image[x,y][r] and image[x,y][b] > image[x,y][g]:
                    image_board[x,y] = 255
                    image_other[x,y] = 0
                    other_pixel += 1

                else:
                    image_other[x,y] = 0
                    image_board[x,y] = 255
                    other_pixel += 1


        print("board_pixels = ", board_pixel)
        print("other_pixels = ", other_pixel)

        #plot result
        image_board = np.rot90(image_board, k=1)
        image_board = np.flipud(image_board)
        plt.imshow(image_board)
        plt.show()

####################################################################################################

    def quitDialog(self):
        self.ImageView.close()
        self.console.close()
        plt.close()
        if QtCore.QCoreApplication.instance() != None:
            app = QtCore.QCoreApplication.instance()
        else:
            app = QtGui.QApplication(sys.argv)
        sys.exit(app.exec_())
        return



    def closeEvent(self, event):
         #==============================================================================
         #       If we close a QtGui.QWidget, a QtGui.QCloseEvent is generated.
         #       To modify the widget behaviour we need to reimplement the closeEvent() event handler.
         #==============================================================================
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you wish to quit?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
            self.console.close()
            plt.close()

        else:
            event.ignore()


def main():
    if QtCore.QCoreApplication.instance() != None:
        app = QtCore.QCoreApplication.instance()
    else:
        app = QtGui.QApplication(sys.argv)
    ex = Viewer()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
