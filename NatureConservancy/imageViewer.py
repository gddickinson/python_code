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
from skimage import util
from skimage.color import rgb2gray
import copy
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb
from scipy.ndimage import interpolation

from PyQt4.QtCore import *
from PyQt4.QtGui import *


if sys.version_info[:2]<(2,5):
    def partial(func,arg):
        def callme():
            return func(arg)
        return callme
else:
    from functools import partial

#global variables

global roi_origin, roi_size, newimg, original_image


class Form(QDialog):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)


        #filter variables
        self.red_min = 115
        self.red_max = 210
        self.green_min = 40
        self.green_max = 110
        self.blue_min = 15
        self.blue_max = 75

        #ratio variables
        self.green_blue_ratio_min = 1.2
        self.green_blue_ratio_max = 3.0
        self.red_green_ratio_min = 1.4
        self.red_green_ratio_max = 2.8

        # self.filterBox=QComboBox()
        # self.filterBox.addItem("No Filter")

        self.SpinBox1=QDoubleSpinBox()
        self.SpinBox1.setRange(0,self.red_max)
        self.SpinBox1.setValue(self.red_min)

        self.SpinBox2=QDoubleSpinBox()
        self.SpinBox2.setRange(self.red_min,255)
        self.SpinBox2.setValue(self.red_max)

        self.SpinBox3=QDoubleSpinBox()
        self.SpinBox3.setRange(0,self.green_max)
        self.SpinBox3.setValue(self.green_min)

        self.SpinBox4=QDoubleSpinBox()
        self.SpinBox4.setRange(self.green_min,255)
        self.SpinBox4.setValue(self.green_max)

        self.SpinBox5=QDoubleSpinBox()
        self.SpinBox5.setRange(0,self.blue_max)
        self.SpinBox5.setValue(self.blue_min)

        self.SpinBox6=QDoubleSpinBox()
        self.SpinBox6.setRange(self.blue_min,255)
        self.SpinBox6.setValue(self.blue_max)

        self.SpinBox7=QDoubleSpinBox()
        self.SpinBox7.setRange(0,self.green_blue_ratio_max)
        self.SpinBox7.setValue(self.green_blue_ratio_min)

        self.SpinBox8=QDoubleSpinBox()
        self.SpinBox8.setRange(self.green_blue_ratio_min,255)
        self.SpinBox8.setValue(self.green_blue_ratio_max)

        self.SpinBox9=QDoubleSpinBox()
        self.SpinBox9.setRange(0,self.red_green_ratio_max)
        self.SpinBox9.setValue(self.red_green_ratio_min)

        self.SpinBox10=QDoubleSpinBox()
        self.SpinBox10.setRange(self.red_green_ratio_min,255)
        self.SpinBox10.setValue(self.red_green_ratio_max)


        # self.filterLabel=QLabel("No Filter")
        # self.filterFlag = 'No Filter'

        self.sld1 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld1.setRange(0,255)
        self.sld1.setTickPosition(QSlider.TicksBelow)
        self.sld1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld1.setValue(self.red_min)
        self.sld1.setGeometry(30, 40, 100, 30)

        self.sld2 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld2.setRange(0,255)
        self.sld2.setTickPosition(QSlider.TicksAbove)
        self.sld2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld2.setValue(self.red_max)
        self.sld2.setGeometry(30, 40, 100, 30)

        self.sld3 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld3.setRange(0,255)
        self.sld3.setTickPosition(QSlider.TicksBelow)
        self.sld3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld3.setValue(self.green_min)
        self.sld3.setGeometry(30, 40, 100, 30)

        self.sld4 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld4.setRange(0,255)
        self.sld4.setTickPosition(QSlider.TicksAbove)
        self.sld4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld4.setValue(self.green_max)
        self.sld4.setGeometry(30, 40, 100, 30)

        self.sld5 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld5.setRange(0,255)
        self.sld5.setTickPosition(QSlider.TicksBelow)
        self.sld5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld5.setValue(self.blue_min)
        self.sld5.setGeometry(30, 40, 100, 30)

        self.sld6 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld6.setRange(0,255)
        self.sld6.setTickPosition(QSlider.TicksAbove)
        self.sld6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld6.setValue(self.blue_max)
        self.sld6.setGeometry(30, 40, 100, 30)

        self.sld7 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld7.setRange(0,255)
        self.sld7.setTickPosition(QSlider.TicksBelow)
        self.sld7.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld7.setValue(self.green_blue_ratio_min)
        self.sld7.setGeometry(30, 40, 100, 30)

        self.sld8 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld8.setRange(0,255)
        self.sld8.setTickPosition(QSlider.TicksAbove)
        self.sld8.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld8.setValue(self.green_blue_ratio_max)
        self.sld8.setGeometry(30, 40, 100, 30)

        self.sld9 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld9.setRange(0,255)
        self.sld9.setTickPosition(QSlider.TicksBelow)
        self.sld9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld9.setValue(self.red_green_ratio_min)
        self.sld9.setGeometry(30, 40, 100, 30)

        self.sld10 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld10.setRange(0,255)
        self.sld10.setTickPosition(QSlider.TicksAbove)
        self.sld10.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld10.setValue(self.red_green_ratio_max)
        self.sld10.setGeometry(30, 40, 100, 30)


        self.button1 = QPushButton("Run")
        self.onFlag = False

        self.buttonRed = QPushButton("RED")
        self.buttonGreen = QPushButton("GREEN")
        self.buttonBlue = QPushButton("BLUE")

        self.buttonGreenBlueRatio = QPushButton("GREEN/BLUE")
        self.buttonRedGreenRatio = QPushButton("RED/GREEN")


        layout = QGridLayout()
        #layout.addWidget(self.dial, 0,0)
        #layout.addWidget(self.zerospinbox, 0,1)
        layout.addWidget(self.button1, 0, 0)
        layout.addWidget(self.buttonRed, 1, 0)
        layout.addWidget(self.sld1, 1, 1)
        layout.addWidget(self.sld2, 1, 2)
        layout.addWidget(self.SpinBox1, 1, 3)
        layout.addWidget(self.SpinBox2, 1, 4)
        layout.addWidget(self.buttonGreen, 2, 0)
        layout.addWidget(self.sld3, 2, 1)
        layout.addWidget(self.sld4, 2, 2)
        layout.addWidget(self.SpinBox3, 2, 3)
        layout.addWidget(self.SpinBox4, 2, 4)
        layout.addWidget(self.buttonBlue, 3, 0)
        layout.addWidget(self.sld5,3, 1)
        layout.addWidget(self.sld6, 3, 2)
        layout.addWidget(self.SpinBox5, 3, 3)
        layout.addWidget(self.SpinBox6, 3, 4)

        layout.addWidget(self.buttonGreenBlueRatio, 1, 5)
        layout.addWidget(self.sld7, 1, 6)
        layout.addWidget(self.sld8, 1, 7)
        layout.addWidget(self.SpinBox7, 1, 8)
        layout.addWidget(self.SpinBox8, 1, 9)

        layout.addWidget(self.buttonRedGreenRatio, 2, 5)
        layout.addWidget(self.sld9, 2, 6)
        layout.addWidget(self.sld10, 2, 7)
        layout.addWidget(self.SpinBox9, 2, 8)
        layout.addWidget(self.SpinBox10, 2, 9)

        self.setLayout(layout)

        self.connect(self.button1,SIGNAL("clicked()"),self.button_1)

        self.connect(self.buttonRed,SIGNAL("clicked()"),self.button_red)
        self.connect(self.buttonGreen,SIGNAL("clicked()"),self.button_green)
        self.connect(self.buttonBlue,SIGNAL("clicked()"),self.button_blue)

        self.connect(self.buttonGreenBlueRatio,SIGNAL("clicked()"),self.button_green_blue_ratio)
        self.connect(self.buttonRedGreenRatio,SIGNAL("clicked()"),self.button_red_green_ratio)


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

        self.connect(self.sld7,SIGNAL("valueChanged(int)"), self.slider_7)
        self.connect(self.sld7,SIGNAL("valueChanged(int)"),self.SpinBox7.setValue)

        self.connect(self.sld8,SIGNAL("valueChanged(int)"), self.slider_8)
        self.connect(self.sld8,SIGNAL("valueChanged(int)"),self.SpinBox8.setValue)

        self.connect(self.sld9,SIGNAL("valueChanged(int)"), self.slider_9)
        self.connect(self.sld9,SIGNAL("valueChanged(int)"),self.SpinBox9.setValue)

        self.connect(self.sld10,SIGNAL("valueChanged(int)"), self.slider_10)
        self.connect(self.sld10,SIGNAL("valueChanged(int)"),self.SpinBox10.setValue)



    def button_1(self):
        if self.onFlag == False:
            self.onFlag = True
            self.button1.setText("Run")
        else:
            self.onFlag = False
            self.button1.setText("Run")


    def button_red(self):
        self.red_min = 115
        self.red_max = 210
        self.sld2.setValue(self.red_max)
        self.sld1.setValue(self.red_min)
        self.SpinBox2.setValue(self.red_max)
        self.SpinBox2.setRange(self.red_min,255)
        self.SpinBox1.setValue(self.red_min)
        self.SpinBox1.setRange(0,self.red_max)


    def button_green(self):
        self.green_min = 40
        self.green_max = 110
        self.sld4.setValue(self.green_max)
        self.sld3.setValue(self.green_min)
        self.SpinBox4.setValue(self.green_max)
        self.SpinBox4.setRange(self.green_min,255)
        self.SpinBox3.setValue(self.green_min)
        self.SpinBox3.setRange(0,self.green_max)

    def button_blue(self):
        self.blue_min = 15
        self.blue_max = 75
        self.sld6.setValue(self.blue_max)
        self.sld5.setValue(self.blue_min)
        self.SpinBox6.setValue(self.blue_max)
        self.SpinBox6.setRange(self.blue_min,255)
        self.SpinBox5.setValue(self.blue_min)
        self.SpinBox5.setRange(0,self.blue_max)

    def button_green_blue_ratio(self):
        self.green_blue_ratio_min = 1.2
        self.green_blue_ratio_max = 3.0
        self.sld8.setValue(self.green_blue_ratio_max)
        self.sld7.setValue(self.green_blue_ratio_min)
        self.SpinBox8.setValue(self.green_blue_ratio_max)
        self.SpinBox8.setRange(self.green_blue_ratio_min,255)
        self.SpinBox7.setValue(self.green_blue_ratio_min)
        self.SpinBox7.setRange(0,self.green_blue_ratio_max)

    def button_red_green_ratio(self):
        self.red_green_ratio_min = 1.4
        self.red_green_ratio_max = 2.8
        self.sld10.setValue(self.red_green_ratio_max)
        self.sld9.setValue(self.red_green_ratio_min)
        self.SpinBox10.setValue(self.red_green_ratio_max)
        self.SpinBox10.setRange(self.red_green_ratio_min,255)
        self.SpinBox9.setValue(self.red_green_ratio_min)
        self.SpinBox9.setRange(0,self.red_green_ratio_max)


    def slider_1(self):
        if self.sld1.value() < self.red_max:
            self.red_min = self.sld1.value()
            self.SpinBox2.setRange(self.red_min,255)
        else:
            self.sld1.setValue(self.red_max)
            self.SpinBox1.setValue(self.red_max)

    def slider_2(self):
        if self.sld2.value() > self.red_min:
            self.red_max = self.sld2.value()
            self.SpinBox1.setRange(0,self.red_max)
        else:
            self.sld2.setValue(self.red_min)
            self.SpinBox2.setValue(self.red_min)

    def slider_3(self):
        if self.sld3.value() < self.green_max:
            self.green_min = self.sld3.value()
            self.SpinBox4.setRange(self.green_min,255)
        else:
            self.sld3.setValue(self.green_max)
            self.SpinBox3.setValue(self.green_max)

    def slider_4(self):
        if self.sld4.value() > self.green_min:
            self.green_max = self.sld4.value()
            self.SpinBox3.setRange(0,self.green_max)
        else:
            self.sld4.setValue(self.green_min)
            self.SpinBox4.setValue(self.green_min)

    def slider_5(self):
        if self.sld5.value() < self.blue_max:
            self.blue_min = self.sld5.value()
            self.SpinBox6.setRange(self.blue_min,255)
        else:
            self.sld5.setValue(self.blue_max)
            self.SpinBox5.setValue(self.blue_max)

    def slider_6(self):
        if self.sld6.value() > self.blue_min:
            self.blue_max = self.sld6.value()
            self.SpinBox5.setRange(0,self.blue_max)
        else:
            self.sld6.setValue(self.blue_min)
            self.SpinBox6.setValue(self.blue_min)

    def slider_7(self):
        if self.sld7.value() < self.green_blue_ratio_max:
            self.green_blue_ratio_min = self.sld7.value()
            self.SpinBox8.setRange(self.green_blue_ratio_min,255)
        else:
            self.sld7.setValue(self.green_blue_ratio_max)
            self.SpinBox7.setValue(self.green_blue_ratio_max)

    def slider_8(self):
        if self.sld8.value() > self.green_blue_ratio_min:
            self.green_blue_ratio_max = self.sld8.value()
            self.SpinBox7.setRange(0,self.green_blue_ratio_max)
        else:
            self.sld8.setValue(self.green_blue_ratio_min)
            self.SpinBox8.setValue(self.green_blue_ratio_min)

    def slider_9(self):
        if self.sld9.value() < self.red_green_ratio_max:
            self.red_green_ratio_min = self.sld9.value()
            self.SpinBox10.setRange(self.red_green_ratio_min,255)
        else:
            self.sld9.setValue(self.red_green_ratio_max)
            self.SpinBox9.setValue(self.red_green_ratio_max)

    def slider_10(self):
        if self.sld10.value() > self.red_green_ratio_min:
            self.red_green_ratio_max = self.sld10.value()
            self.SpinBox9.setRange(0,self.red_green_ratio_max)
        else:
            self.sld10.setValue(self.red_green_ratio_min)
            self.SpinBox10.setValue(self.red_green_ratio_min)

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
        rotateCounter.setShortcut('Ctrl+<')
        rotateCounter.setStatusTip('Rotate Counterclock')
        rotateCounter.triggered.connect(self.rotateImageCounter)

        rotateClock = QtGui.QAction(QtGui.QIcon('open.png'), 'Rotate Clock', self)
        rotateClock.setShortcut('Ctrl+>')
        rotateClock.setStatusTip('Rotate Clock')
        rotateClock.triggered.connect(self.rotateImageClock)

        rotateCounter_90 = QtGui.QAction(QtGui.QIcon('open.png'), 'Rotate Counterclock 90', self)
        rotateCounter_90.setShortcut('Ctrl+9')
        rotateCounter_90.setStatusTip('Rotate Counterclock 90')
        rotateCounter_90.triggered.connect(self.rotateImageCounter_90)

        rotateClock_90 = QtGui.QAction(QtGui.QIcon('open.png'), 'Rotate Clock 90', self)
        rotateClock_90.setShortcut('Ctrl+0')
        rotateClock_90.setStatusTip('Rotate Clock 90')
        rotateClock_90.triggered.connect(self.rotateImageClock_90)

        flipLR = QtGui.QAction(QtGui.QIcon('open.png'), 'Flip Vertical', self)
        flipLR.setShortcut('Ctrl+7')
        flipLR.setStatusTip('Flip vertical')
        flipLR.triggered.connect(self.flipImageLR)

        flipUD = QtGui.QAction(QtGui.QIcon('open.png'), 'Flip Horizontal', self)
        flipUD.setShortcut('Ctrl+8')
        flipUD.setStatusTip('Flip horizontal')
        flipUD.triggered.connect(self.flipImageUD)

        invert = QtGui.QAction(QtGui.QIcon('open.png'), 'Invert', self)
        invert.setShortcut('Ctrl+I')
        invert.setStatusTip('Invert')
        invert.triggered.connect(self.invert)

        rgbToGray = QtGui.QAction(QtGui.QIcon('open.png'), 'RGB to Grayscale', self)
        rgbToGray.setShortcut('Ctrl+G')
        rgbToGray.setStatusTip('RGB to Gray')
        rgbToGray.triggered.connect(self.rgb2grayscale)

        otsu_thresh = QtGui.QAction(QtGui.QIcon('open.png'), 'Otsu Threshold', self)
        otsu_thresh.setShortcut('Ctrl+T')
        otsu_thresh.setStatusTip('otsu_thresh')
        otsu_thresh.triggered.connect(self.otsu_thresh)

        getOriginal = QtGui.QAction(QtGui.QIcon('open.png'), 'Reset to Original', self)
        getOriginal.setShortcut('Ctrl+Z')
        getOriginal.setStatusTip('get_original')
        getOriginal.triggered.connect(self.get_original)

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
        fileMenu1.addAction(rotateCounter_90)
        fileMenu1.addAction(rotateClock_90)
        fileMenu1.addAction(rotateCounter)
        fileMenu1.addAction(rotateClock)
        fileMenu1.addAction(flipLR)
        fileMenu1.addAction(flipUD)
        fileMenu1.addAction(invert)
        fileMenu1.addAction(rgbToGray)
        fileMenu1.addAction(otsu_thresh)
        fileMenu1.addAction(getOriginal)

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
        global newimg, original_image
        newimg = io.imread(filename)
        original_image = copy.deepcopy(newimg)
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

    def rotateImageCounter_90(self):
        img = self.ImageView.getProcessedImage()
        global newimg
        newimg = np.rot90(img,k=3)
        self.ImageView.setImage(newimg)
        return

    def rotateImageClock_90(self):
        img = self.ImageView.getProcessedImage()
        global newimg
        newimg = np.rot90(img,k=1)
        self.ImageView.setImage(newimg)
        return

    def rotateImageCounter(self):
        img = self.ImageView.getProcessedImage()
        global newimg
        newimg = interpolation.rotate(img,-1)
        self.ImageView.setImage(newimg)
        return

    def rotateImageClock(self):
        img = self.ImageView.getProcessedImage()
        global newimg
        newimg = interpolation.rotate(img,1)
        self.ImageView.setImage(newimg)
        return

    def flipImageLR(self):
        img = self.ImageView.getProcessedImage()
        global newimg
        newimg = np.fliplr(img)
        self.ImageView.setImage(newimg)
        return

    def flipImageUD(self):
        img = self.ImageView.getProcessedImage()
        global newimg
        newimg = np.flipud(img)
        self.ImageView.setImage(newimg)
        return

    def invert(self):
        img = self.ImageView.getProcessedImage()
        global newimg
        newimg = np.invert(img)
        self.ImageView.setImage(newimg)
        return

    def rgb2grayscale(self):
        img = self.ImageView.getProcessedImage()
        global newimg
        newimg = rgb2gray(img)
        self.ImageView.setImage(newimg)
        return

    def otsu_thresh(self):
        img = self.ImageView.getProcessedImage()
        global newimg
        newimg = rgb2gray(img)
        newimg = threshold_otsu(img)
        self.ImageView.setImage(newimg)
        return

    def get_original(self):
        global newimg, original_image
        newimg = original_image
        newimg = np.rot90(newimg,k=1)
        newimg = np.flipud(newimg)
        self.ImageView.setImage(newimg)
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

        #area based on rectangular roi
        roi_area = int(roi_size[0])*int(roi_size[1])


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
        red_min = self.console.red_min
        red_max = self.console.red_max
        green_min = self.console.green_min
        green_max = self.console.green_max
        blue_min = self.console.blue_min
        blue_max = self.console.blue_max

        #ratio variables
        green_blue_ratio_min = self.console.green_blue_ratio_min
        green_blue_ratio_max = self.console.green_blue_ratio_max
        red_green_ratio_min = self.console.red_green_ratio_min
        red_green_ratio_max = self.console.red_green_ratio_max

        #loop through all pixels in image and set pixel to maximum channel value - count pixels in each channel
        for x in range (image_x_origin,image_x_end):
            for y in range (image_y_origin,image_y_end):
                #pixels with equivalent values
                if image[x,y][b] == image[x,y][g]:
                    image_other[x,y] = 0
                    image_board[x,y] = 255
                    other_pixel += 1

                #count board pixels
                elif ((image[x,y][r] > image[x,y][g])
                        and (image[x,y][r] > image[x,y][b])
                        and ((image[x,y][g]/image[x,y][b]) > green_blue_ratio_min)
                        and ((image[x,y][g]/image[x,y][b]) < green_blue_ratio_max)
                        and ((image[x,y][r]/image[x,y][g]) > red_green_ratio_min)
                        and ((image[x,y][r]/image[x,y][g]) < red_green_ratio_max)):

                    if (image[x,y][r] > red_min
                        and image[x,y][r] < red_max
                        and image[x,y][g] > green_min
                        and image[x,y][g] < green_max
                        and image[x,y][b] > blue_min
                        and image[x,y][b] < blue_max):

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
        print("ROI_pixels = ", roi_area)

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
