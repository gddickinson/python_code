# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 12:14:34 2015

@author: george
"""
############# Import packages ################################################
#from __future__ import (absolute_import, division,
                        #print_function, unicode_literals)
#from future.builtins import (bytes, dict, int, list, object, range, str,
                             #ascii, chr, hex, input, next, oct, open,
                             #pow, round, super, filter, map, zip)

import time
tic=time.time()
import os, sys

os.environ["QT_API"] = "pyside" #for python2.7 - otherwise error: API 'QString' has already been set to version 1 --- due to PyQt4 conflict


import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtCore import *
from qtpy.QtGui import *
#from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
#import tifffile
import json
import re

from skimage import io
from skimage import util
from skimage.color import rgb2gray
from skimage.restoration import denoise_bilateral
from skimage.transform import resize
import copy
from skimage.filters import threshold_otsu
try:
    from skimage.filters import gaussian
except:
    from skimage.filters import gaussian_filter as gaussian
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb
from scipy.ndimage import interpolation
from skimage import img_as_ubyte

#from PyQt4.QtCore import *
#from PyQt4.QtGui import *


if sys.version_info[:2]<(2,5):
    def partial(func,arg):
        def callme():
            return func(arg)
        return callme
else:
    from functools import partial

########### define global variables ##########################################

global ROI_flag, roi_origin, roi_size, newimg, original_image, sky_array, canopy_array, sky_mean, sky_n, sky_sd, canopy_mean, canopy_n, canopy_sd, roi_mean_red, roi_mean_green, roi_mean_blue, roi_mean_intensity

##############################################################################
########### define classes for GUI ###########################################
##############################################################################

class Console_Analysis(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(Console_Analysis, self).__init__(parent)
        
        global newimg
        
        self.image = newimg
        self.randomPoints = []
        self.numberPoints = 50
        self.activePoint = 0
        self.currentX = None
        self.currentY = None
        self.x, self.y = self.image.shape[0:2]
        self.randomPlot = False
        self.randomPlotWithPoints = copy.deepcopy(self.image)
        
        self.randomPlot = pg.ImageView(view = pg.PlotItem())
        self.randomPlot.setImage(self.randomPlotWithPoints)
        self.randomPlot.show()
        self.randomPlot.view.setTitle(title = 'Random Point Analysis')
        
        self.displayPoints = True
        self.displayPointsEdge = False
        
        self.edgeSize = 1
        
        self.analysisTypes = ['coverboard', 'sky-canopy']
        
        self.coverboard_selection = ['board', 'not-board', 'unknown']
        self.skyCanopy_selection = ['sky', 'canopy', 'unknown']

        self.current_selection_types = self.coverboard_selection
        self.current_selection_flag = self.analysisTypes[0]
        
        self.currentPixelType = None
        self.assignedPixelTypes = []
        for i in range (self.numberPoints):
            self.assignedPixelTypes.append('None')
        
        
        ########## set up widgets ####################################
        
        self.button1 = QtWidgets.QPushButton("Generate Points")
        self.button2 = QtWidgets.QPushButton("Hide Points")
        self.button3 = QtWidgets.QPushButton("Show Edge")
        self.button4 = QtWidgets.QPushButton("Show current point")
        self.button5 = QtWidgets.QPushButton("Go forward a point")
        self.button6 = QtWidgets.QPushButton("Go back a point")
        self.button9 = QtWidgets.QPushButton("Center on current point")
        
        self.SpinBox1=QtWidgets.QSpinBox()
        self.SpinBox1.setRange(0,10000)
        self.SpinBox1.setValue(self.numberPoints)
                
        self.number_points = QtWidgets.QLabel()
        self.number_points.setText("Number of Points = %d" % len(self.randomPoints)) 
        
        self.active_point = QtWidgets.QLabel()
        self.active_point.setText("Current Point = %d" % self.activePoint) 
        
        self.active_x = QtWidgets.QLabel()
        self.active_x.setText("X = %d" % self.activePoint)    
        
        self.active_y = QtWidgets.QLabel()
        self.active_y.setText("Y = %d" % self.activePoint)   
        
        self.edge_size = QtWidgets.QLabel()
        self.edge_size.setText("Edge Size = %d" % self.edgeSize)
        
        self.SpinBox2=QtWidgets.QSpinBox()
        self.SpinBox2.setRange(0,self.numberPoints)
        self.SpinBox2.setValue(self.activePoint)
        
        self.SpinBox3=QtWidgets.QSpinBox()
        self.SpinBox3.setRange(1,100)
        self.SpinBox3.setValue(self.edgeSize)     
        
        self.ComboBox1 = QtWidgets.QComboBox()
        self.ComboBox1.addItems(self.analysisTypes)
        
        self.analysis_text = QtWidgets.QLabel()
        self.analysis_text.setText("Current pixel = %s" % self.currentPixelType)
        
        self.button7 = QtWidgets.QPushButton(self.coverboard_selection[0])
        self.button8 = QtWidgets.QPushButton(self.coverboard_selection[1])
        
                    
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.button1, 0, 0)
        layout.addWidget(self.button2, 0, 1)
        layout.addWidget(self.button3, 0, 2)
        
        layout.addWidget(self.number_points, 1, 0)
        layout.addWidget(self.SpinBox1, 1, 1)
        
        layout.addWidget(self.active_point, 2, 0)
        layout.addWidget(self.SpinBox2, 2, 1)
        layout.addWidget(self.active_x, 2, 2)
        layout.addWidget(self.active_y, 2, 3)
        
        layout.addWidget(self.edge_size, 3, 0)
        layout.addWidget(self.SpinBox3, 3, 1)
        
        layout.addWidget(self.button4, 4, 0)
        layout.addWidget(self.button5, 4, 1)
        layout.addWidget(self.button6, 4, 2)
        layout.addWidget(self.button9, 4, 3)        
        
        layout.addWidget(self.ComboBox1, 5,0)
        
        layout.addWidget(self.analysis_text, 6,0)
        layout.addWidget(self.button7, 6, 1)
        layout.addWidget(self.button8, 6, 2)        

        self.setLayout(layout)

        self.connect(self.button1,SIGNAL("clicked()"),self.button_1)                
        self.connect(self.button2,SIGNAL("clicked()"),self.button_2)
        self.connect(self.button3,SIGNAL("clicked()"),self.button_3)
        self.connect(self.button4,SIGNAL("clicked()"),self.button_4)
        self.connect(self.button5,SIGNAL("clicked()"),self.button_5)
        self.connect(self.button6,SIGNAL("clicked()"),self.button_6)
        
        self.connect(self.button7,SIGNAL("clicked()"),self.button_7)       
        self.connect(self.button8,SIGNAL("clicked()"),self.button_8)        
        
        self.connect(self.button9,SIGNAL("clicked()"),self.button_9)       
        
        self.connect(self.SpinBox1,SIGNAL("valueChanged(int)"),self.spinBox1_update)
        self.connect(self.SpinBox2,SIGNAL("valueChanged(int)"),self.spinBox2_update)
        self.connect(self.SpinBox3,SIGNAL("valueChanged(int)"),self.spinBox3_update)
        
        self.connect(self.ComboBox1,SIGNAL("currentIndexChanged(QString)"),self.comboBox1_update)


    #### Helper functions #######
    def addEdge(self,img, x_val, y_val, listOfPositions, size = 1, edgeColour = 255, centerColour = 0):
        
        s = set(listOfPositions)
                                        
        for x in range(x_val-size,x_val+size+1):
            for y in range(y_val-size,y_val+size+1):
                           
                try:
                    if (x,y) in s:
                        pass
                    else:
                        img[x,y] = edgeColour
                except:
                    pass

   
        img[x_val,y_val] = centerColour
           
        return img


        
    ################# define functions called by widgets #####################
    def button_1(self):
        self.randomPoints = []
        self.randomPlotWithPoints = copy.deepcopy(self.image)
        self.randomPlotWithPointsAndEdge = copy.deepcopy(self.image)
        
        for i in range(0,self.numberPoints):
            new_x = np.random.randint(0,high = self.x)
            new_y = np.random.randint(0,high = self.y)
            self.randomPoints.append((new_x,new_y))
            self.randomPlotWithPoints[new_x,new_y] = 0                                     
            self.randomPlotWithPointsAndEdge = self.addEdge(self.randomPlotWithPointsAndEdge, new_x, new_y, self.randomPoints, size = self.edgeSize)                         
                          
                
                
        self.number_points.setText("Number of Points = %d" % len(self.randomPoints)) 
        self.activePoint = 0
        self.active_point.setText("Current Point = %d" % self.activePoint) 
        self.currentX, self.currentY = self.randomPoints[self.activePoint] 
        self.active_x.setText("X = %d" % self.currentX)
        self.active_y.setText("Y = %d" % self.currentY) 

        self.randomPlot.setImage(self.randomPlotWithPoints)
        print(self.randomPlot.axes)
        
    def button_2(self):
        if self.displayPoints == True:
            self.randomPlot.setImage(self.image, autoRange = False)
            self.displayPoints = False
            self.button2.setText("Show Points")
            self.displayPointsEdge = False
            self.button3.setText("Show Edge")
        else:    
            self.randomPlot.setImage(self.randomPlotWithPoints, autoRange = False)
            self.displayPoints = True
            self.button2.setText("Hide Points")
            

    def button_3(self):
        if self.displayPointsEdge == True:
            self.randomPlot.setImage(self.randomPlotWithPoints, autoRange = False)
            self.displayPointsEdge = False
            self.button3.setText("Show Edge")
        else:    
            self.randomPlot.setImage(self.randomPlotWithPointsAndEdge, autoRange = False)
            self.displayPointsEdge = True
            self.button3.setText("Hide Edge")
            
    def button_4(self):
        self.randomPlotCurrentPointWithEdge = copy.deepcopy(self.image) 
        self.randomPlotCurrentPointWithEdge = self.addEdge(self.randomPlotCurrentPointWithEdge, self.currentX, self.currentY, self.randomPoints, size = self.edgeSize)
        self.randomPlot.setImage(self.randomPlotCurrentPointWithEdge, autoRange = False)
        


    def button_5(self):
        if self.activePoint +1 <= self.numberPoints:
            self.activePoint += 1
            self.active_point.setText("Current Point = %d" % self.activePoint) 
            self.currentX, self.currentY = self.randomPoints[self.activePoint] 
            self.active_x.setText("X = %d" % self.currentX)
            self.active_y.setText("Y = %d" % self.currentY)
            self.SpinBox2.setValue(self.activePoint)            
            self.randomPlotCurrentPointWithEdge = copy.deepcopy(self.image) 
            self.randomPlotCurrentPointWithEdge = self.addEdge(self.randomPlotCurrentPointWithEdge, self.currentX, self.currentY, self.randomPoints, size = self.edgeSize)
            self.randomPlot.setImage(self.randomPlotCurrentPointWithEdge, autoRange = False)
        
    def button_6(self):
        if self.activePoint -1 >= 0:
            self.activePoint -= 1
            self.active_point.setText("Current Point = %d" % self.activePoint) 
            self.currentX, self.currentY = self.randomPoints[self.activePoint] 
            self.active_x.setText("X = %d" % self.currentX)
            self.active_y.setText("Y = %d" % self.currentY)
            self.SpinBox2.setValue(self.activePoint)
            self.randomPlotCurrentPointWithEdge = copy.deepcopy(self.image) 
            self.randomPlotCurrentPointWithEdge = self.addEdge(self.randomPlotCurrentPointWithEdge, self.currentX, self.currentY, self.randomPoints, size = self.edgeSize)
            self.randomPlot.setImage(self.randomPlotCurrentPointWithEdge, autoRange = False)      


    def button_7(self):
        self.currentPixelType = self.current_selection_types[0]
        self.analysis_text.setText("Current pixel = %s" % self.currentPixelType)
        self.assignedPixelTypes[self.activePoint] = self.currentPixelType

    def button_8(self):
        self.currentPixelType = self.current_selection_types[1]
        self.analysis_text.setText("Current pixel = %s" % self.currentPixelType)
        self.assignedPixelTypes[self.activePoint] = self.currentPixelType

    def button_9(self):
        self.randomPlot.view.setXRange(self.currentX, self.currentX)
        self.randomPlot.view.setYRange(self.currentY, self.currentY)

    
    def spinBox1_update (self):
        self.numberPoints = self.SpinBox1.value()

    def spinBox2_update (self):
        if self.randomPoints != []:
            self.activePoint = self.SpinBox2.value()
            self.active_point.setText("Current Point = %d" % self.activePoint) 
            self.currentX, self.currentY = self.randomPoints[self.activePoint] 
            self.active_x.setText("X = %d" % self.currentX)
            self.active_y.setText("Y = %d" % self.currentY)
        else:
            self.SpinBox2.setValue(self.activePoint)

    def spinBox3_update (self):
        self.edgeSize = self.SpinBox3.value()
        self.edge_size.setText("Edge Size = %d" % self.edgeSize)
        self.randomPlotWithPointsAndEdge = copy.deepcopy(self.image) 
        
        for i in range(0,self.numberPoints):
            new_x = self.randomPoints[i][0]
            new_y = self.randomPoints[i][1]                                    
            self.randomPlotWithPointsAndEdge = self.addEdge(self.randomPlotWithPointsAndEdge, new_x, new_y, self.randomPoints, size = self.edgeSize)

        self.randomPlot.setImage(self.randomPlotWithPointsAndEdge, autoRange = False)


    def comboBox1_update(self):
        self.current_selection_flag = self.ComboBox1.currentText()
        
        self.currentPixelType = None
        self.assignedPixelTypes = []
        for i in range (self.numberPoints):
            self.assignedPixelTypes.append('None')
 
        if self.current_selection_flag == 'coverboard':
            self.current_selection_types = self.coverboard_selection
        
        elif self.current_selection_flag == 'sky-canopy':
            self.current_selection_types = self.skyCanopy_selection
        
        self.button7.setText(self.current_selection_types[0])
        self.button8.setText(self.current_selection_types[1])
        
##############################################################################

class Console_Cal(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(Console_Cal, self).__init__(parent)
        
        global roi_origin, roi_size, sky_mean, sky_n, sky_sd, canopy_mean, canopy_n, canopy_sd, roi_mean_red, roi_mean_green, roi_mean_blue, roi_mean_intensity
        
        ########## set up widgets ####################################
        
        self.button1 = QtWidgets.QPushButton("Get Sky")
        self.button2 = QtWidgets.QPushButton("Get Canopy")
        self.button3 = QtWidgets.QPushButton("Undo last")
        self.button4 = QtWidgets.QPushButton("Done")        
        self.buttonReset = QtWidgets.QPushButton("Reset All")
        
        self.buttonSkyReset = QtWidgets.QPushButton("Sky Reset")        
        self.buttonCanopyReset = QtWidgets.QPushButton("Canopy Reset")
                
        self.sky_mean_label = QtWidgets.QLabel()
        self.sky_n_label = QtWidgets.QLabel()
        self.sky_sd_label = QtWidgets.QLabel()
        self.canopy_mean_label = QtWidgets.QLabel()
        self.canopy_n_label = QtWidgets.QLabel()
        self.canopy_sd_label = QtWidgets.QLabel()

        self.sky_mean_label.setText("Sky Mean = %d" % sky_mean) 
        self.sky_n_label.setText("Sky Number = %d" % sky_n) 
        self.sky_sd_label.setText("Sky SD = %d" % sky_sd)
        self.canopy_mean_label.setText("Canopy Mean = %d" % canopy_mean) 
        self.canopy_n_label.setText("Canopy n = %d" % canopy_n) 
        self.canopy_sd_label.setText("Canopy SD = %d" % canopy_sd) 
        
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.button1, 0, 0)
        layout.addWidget(self.button2, 0, 1)
        layout.addWidget(self.button3, 0, 2)
        layout.addWidget(self.button4, 0, 3)
        layout.addWidget(self.buttonReset, 0, 4)
        
        layout.addWidget(self.buttonSkyReset, 1, 0)
        layout.addWidget(self.buttonCanopyReset, 1, 3)

        layout.addWidget(self.sky_mean_label, 2, 0)
        layout.addWidget(self.sky_n_label, 2, 1)
        layout.addWidget(self.sky_sd_label, 2, 2)
        layout.addWidget(self.canopy_mean_label, 3, 0)
        layout.addWidget(self.canopy_n_label, 3, 1)
        layout.addWidget(self.canopy_sd_label, 3, 2)

        self.setLayout(layout)

        self.connect(self.button1,SIGNAL("clicked()"),self.button_1)
        self.connect(self.button2,SIGNAL("clicked()"),self.button_2)
        self.connect(self.button3,SIGNAL("clicked()"),self.button_3)
        self.connect(self.button4,SIGNAL("clicked()"),self.button_4)
        self.connect(self.buttonReset,SIGNAL("clicked()"),self.button_reset)
        self.connect(self.buttonSkyReset,SIGNAL("clicked()"),self.button_sky_reset)
        self.connect(self.buttonCanopyReset,SIGNAL("clicked()"),self.button_canopy_reset)
        
    ################# define functions called by widgets #####################
    def button_1(self):
        global sky_array, roi_mean_intensity
   
        sky_array.append(roi_mean_intensity)
        self.updateStats()
        
    def button_2(self):
        global canopy_array, roi_mean_intensity
            
        canopy_array.append(roi_mean_intensity)
        self.updateStats()

    def button_3(self):
        print('not implemented')

    def button_4(self):
        print('not implemented')
            
    def button_reset(self):       
        global sky_array, canopy_array, sky_mean, sky_n, sky_sd, canopy_mean, canopy_n, canopy_sd
        
        sky_array = []
        canopy_array = []
        sky_n = len(sky_array)
        canopy_n = len(canopy_array)
        sky_mean = 0
        canopy_mean = 0
        sky_sd = 0
        canopy_sd = 0
        
        self.sky_mean_label.setText("Sky Mean = %d" % sky_mean) 
        self.sky_n_label.setText("Sky Number = %d" % sky_n) 
        self.sky_sd_label.setText("Sky SD = %d" % sky_sd)
        self.canopy_mean_label.setText("Canopy Mean = %d" % canopy_mean) 
        self.canopy_n_label.setText("Canopy n = %d" % canopy_n) 
        self.canopy_sd_label.setText("Canopy SD = %d" % canopy_sd) 
        
    def button_sky_reset(self):       
        global sky_array, canopy_array, sky_mean, sky_n, sky_sd, canopy_mean, canopy_n, canopy_sd
        
        sky_array = []
        sky_n = len(sky_array)
        sky_mean = 0
        sky_sd = 0
        
        self.sky_mean_label.setText("Sky Mean = %d" % sky_mean) 
        self.sky_n_label.setText("Sky Number = %d" % sky_n) 
        self.sky_sd_label.setText("Sky SD = %d" % sky_sd)

    def button_canopy_reset(self):       
        global sky_array, canopy_array, sky_mean, sky_n, sky_sd, canopy_mean, canopy_n, canopy_sd
        
        canopy_array = []
        canopy_n = len(canopy_array)
        canopy_mean = 0
        canopy_sd = 0
        
        self.canopy_mean_label.setText("Canopy Mean = %d" % canopy_mean) 
        self.canopy_n_label.setText("Canopy n = %d" % canopy_n) 
        self.canopy_sd_label.setText("Canopy SD = %d" % canopy_sd) 
            
    def updateStats(self):
        global sky_array, canopy_array, sky_mean, sky_n, sky_sd, canopy_mean, canopy_n, canopy_sd
        
        sky_n = len(sky_array)
        canopy_n = len(canopy_array)
        
        if sky_n > 0:
            sky_mean = np.mean(sky_array)        
            sky_sd = np.std(sky_array)

        if canopy_n > 0:
            canopy_mean = np.mean(canopy_array)        
            canopy_sd = np.std(canopy_array)
            
        self.sky_mean_label.setText("Sky Mean = %d" % sky_mean) 
        self.sky_n_label.setText("Sky Number = %d" % sky_n) 
        self.sky_sd_label.setText("Sky SD = %d" % sky_sd)
        self.canopy_mean_label.setText("Canopy Mean = %d" % canopy_mean) 
        self.canopy_n_label.setText("Canopy n = %d" % canopy_n) 
        self.canopy_sd_label.setText("Canopy SD = %d" % canopy_sd) 


class Console_Canopy(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(Console_Canopy, self).__init__(parent)
        
        global sky_array, canopy_array, sky_mean, sky_n, sky_sd, canopy_mean, canopy_n, canopy_sd

        #initial filter variables - values chosen based on canopy images from Bob
        self.intensity_min = 115
        self.intensity_max = 210
        
        #calibration variables - get from calibration console
        sky_array = []
        canopy_array = []
        sky_n = len(sky_array)
        canopy_n = len(canopy_array)
        sky_mean = 0
        canopy_mean = 0
        sky_sd = 0
        canopy_sd = 0
        
        ########### set up widgets #########################

        self.SpinBox1=QtWidgets.QDoubleSpinBox()
        self.SpinBox1.setRange(0,self.intensity_max)
        self.SpinBox1.setValue(self.intensity_min)

        self.SpinBox2=QtWidgets.QDoubleSpinBox()
        self.SpinBox2.setRange(self.intensity_min,255)
        self.SpinBox2.setValue(self.intensity_max)

   
        self.sld1 = QtWidgets.QSlider(QtCore.Qt.Vertical, self)
        self.sld1.setRange(0,255)
        self.sld1.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld1.setValue(self.intensity_min)
        self.sld1.setGeometry(30, 40, 100, 30)

        self.sld2 = QtWidgets.QSlider(QtCore.Qt.Vertical, self)
        self.sld2.setRange(0,255)
        self.sld2.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sld2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld2.setValue(self.intensity_max)
        self.sld2.setGeometry(30, 40, 100, 30)

        self.path_label = QtWidgets.QLabel()
        self.pathname = "***None set***"
        self.path_label.setText("Batch folder = %s" % (self.pathname)) 
        
        self.button1 = QtWidgets.QPushButton("Run")
        self.onFlag = False

        self.button2 = QtWidgets.QPushButton("Set Calibration")
        self.calDataFlag = False

        self.button3 = QtWidgets.QPushButton("Calibrate")
        self.calFlag = False

        self.button4 = QtWidgets.QPushButton("Get Batch Folder")
        self.batchFlag = False

        self.button5 = QtWidgets.QPushButton("Batch Run")
        
        self.buttonReset = QtWidgets.QPushButton("Reset")


        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.button1, 0, 0)
        layout.addWidget(self.button2, 0, 3)
        layout.addWidget(self.button3, 0, 4)
        layout.addWidget(self.buttonReset, 1, 0)
        layout.addWidget(self.sld1, 1, 1)
        layout.addWidget(self.sld2, 1, 2)
        layout.addWidget(self.SpinBox1, 1, 3)
        layout.addWidget(self.SpinBox2, 1, 4)
        layout.addWidget(self.button4, 2, 0)
        layout.addWidget(self.button5, 2, 3)   
        layout.addWidget(self.path_label, 3,0)


        self.setLayout(layout)

        self.connect(self.button1,SIGNAL("clicked()"),self.button_1)
        self.connect(self.button2,SIGNAL("clicked()"),self.button_2)
        self.connect(self.button2,SIGNAL("clicked()"),self.initCalConsole)        
        self.connect(self.button3,SIGNAL("clicked()"),self.button_3)
        self.connect(self.button4,SIGNAL("clicked()"),self.button_4)        
        #self.connect(self.button5,SIGNAL("clicked()"),self.button_5)
        self.connect(self.buttonReset,SIGNAL("clicked()"),self.button_reset)

        self.connect(self.sld1,SIGNAL("valueChanged(int)"), self.slider_1)
        self.connect(self.sld1,SIGNAL("valueChanged(int)"),self.SpinBox1.setValue)

        self.connect(self.sld2,SIGNAL("valueChanged(int)"), self.slider_2)
        self.connect(self.sld2,SIGNAL("valueChanged(int)"),self.SpinBox2.setValue)

    ################# define functions called by widgets #####################
    def button_1(self):
        if self.onFlag == False:
            self.onFlag = True
            self.button1.setText("Run")
        else:
            self.onFlag = False
            self.button1.setText("Run")

    def button_2(self):
        if self.calDataFlag == False:
            self.calDataFlag = True
            self.button2.setText("Set Calibration")
            
        else:
            self.calDataFlag = False
            self.button2.setText("Set Calibration")

    def button_3(self):
        global sky_array, canopy_array, sky_mean, sky_n, sky_sd, canopy_mean, canopy_n, canopy_sd
        
        if self.calFlag == False:
            self.calFlag = True
            self.button3.setText("Calibrate")
        else:
            self.calFlag = False
            self.button3.setText("Calibrate")
        
        ## Need to think about how calibration parameters calculated!! ###
        ## For the moment using mean intensity +/- 1stdev #######
        self.intensity_min = canopy_mean+canopy_sd
        self.intensity_max = sky_mean-sky_sd
        self.sld2.setValue(self.intensity_max)
        self.sld1.setValue(self.intensity_min)
        self.SpinBox2.setValue(self.intensity_max)
        self.SpinBox2.setRange(self.intensity_min,255)
        self.SpinBox1.setValue(self.intensity_min)
        self.SpinBox1.setRange(0,self.intensity_max)            
            
        
    def button_4(self):
        pathname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a folder',
                os.path.expanduser("~"), QtWidgets.QFileDialog.ShowDirsOnly)
        
        self.pathname = str(pathname)
        #print(pathname)
#        if pathname == '':
#            return False
#        else:
#            self.runBatch(pathname)
#            return
        self.path_label.setText("Batch folder = %s" % (self.pathname)) 
 

    def button_5(self):
        self.runBatch()

    def runBatch(self):
        print("Folder = ", self.pathname)
        return


    def slider_1(self):
        if self.sld1.value() < self.intensity_max:
            self.intensity_min = self.sld1.value()
            self.SpinBox2.setRange(self.intensity_min,255)
        else:
            self.sld1.setValue(self.intensity_max)
            self.SpinBox1.setValue(self.intensity_max)

    def slider_2(self):
        if self.sld2.value() > self.intensity_min:
            self.intensity_max = self.sld2.value()
            self.SpinBox1.setRange(0,self.intensity_max)
        else:
            self.sld2.setValue(self.intensity_min)
            self.SpinBox2.setValue(self.intensity_min)

    def button_reset(self):
        self.intensity_min = 115
        self.intensity_max = 210
        self.sld2.setValue(self.intensity_max)
        self.sld1.setValue(self.intensity_min)
        self.SpinBox2.setValue(self.intensity_max)
        self.SpinBox2.setRange(self.intensity_min,255)
        self.SpinBox1.setValue(self.intensity_min)
        self.SpinBox1.setRange(0,self.intensity_max)


    def updateUi(self):
        self.filterType = unicode(self.filterBox.currentText())
        self.filterLabel.setText(self.filterType)
        self.filterFlag = str(self.filterType)


    def initCalConsole(self):
        self.consoleCalibrate = Console_Cal()
        #self.consoleCalibrate.connect(self.consoleCalibrate.button1,SIGNAL("clicked()"),self.testPrint)
        self.consoleCalibrate.show()

##############################################################################

class Console_Coverboard(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(Console_Coverboard, self).__init__(parent)

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

        # self.filterBox=QtGui.QComboBox()
        # self.filterBox.addItem("No Filter")


        ########### Set uo widgets ####################################
        self.SpinBox1=QtWidgets.QDoubleSpinBox()
        self.SpinBox1.setRange(0,self.red_max)
        self.SpinBox1.setValue(self.red_min)

        self.SpinBox2=QtWidgets.QDoubleSpinBox()
        self.SpinBox2.setRange(self.red_min,255)
        self.SpinBox2.setValue(self.red_max)

        self.SpinBox3=QtWidgets.QDoubleSpinBox()
        self.SpinBox3.setRange(0,self.green_max)
        self.SpinBox3.setValue(self.green_min)

        self.SpinBox4=QtWidgets.QDoubleSpinBox()
        self.SpinBox4.setRange(self.green_min,255)
        self.SpinBox4.setValue(self.green_max)

        self.SpinBox5=QtWidgets.QDoubleSpinBox()
        self.SpinBox5.setRange(0,self.blue_max)
        self.SpinBox5.setValue(self.blue_min)

        self.SpinBox6=QtWidgets.QDoubleSpinBox()
        self.SpinBox6.setRange(self.blue_min,255)
        self.SpinBox6.setValue(self.blue_max)

        self.SpinBox7=QtWidgets.QDoubleSpinBox()
        self.SpinBox7.setRange(0,self.green_blue_ratio_max)
        self.SpinBox7.setValue(self.green_blue_ratio_min)

        self.SpinBox8=QtWidgets.QDoubleSpinBox()
        self.SpinBox8.setRange(self.green_blue_ratio_min,255)
        self.SpinBox8.setValue(self.green_blue_ratio_max)

        self.SpinBox9=QtWidgets.QDoubleSpinBox()
        self.SpinBox9.setRange(0,self.red_green_ratio_max)
        self.SpinBox9.setValue(self.red_green_ratio_min)

        self.SpinBox10=QtWidgets.QDoubleSpinBox()
        self.SpinBox10.setRange(self.red_green_ratio_min,255)
        self.SpinBox10.setValue(self.red_green_ratio_max)

        # self.filterLabel=QtGui.QLabel("No Filter")
        # self.filterFlag = 'No Filter'

        self.sld1 = QtWidgets.QSlider(QtCore.Qt.Vertical, self)
        self.sld1.setRange(0,255)
        self.sld1.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld1.setValue(self.red_min)
        self.sld1.setGeometry(30, 40, 100, 30)

        self.sld2 = QtWidgets.QSlider(QtCore.Qt.Vertical, self)
        self.sld2.setRange(0,255)
        self.sld2.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sld2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld2.setValue(self.red_max)
        self.sld2.setGeometry(30, 40, 100, 30)

        self.sld3 = QtWidgets.QSlider(QtCore.Qt.Vertical, self)
        self.sld3.setRange(0,255)
        self.sld3.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld3.setValue(self.green_min)
        self.sld3.setGeometry(30, 40, 100, 30)

        self.sld4 = QtWidgets.QSlider(QtCore.Qt.Vertical, self)
        self.sld4.setRange(0,255)
        self.sld4.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sld4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld4.setValue(self.green_max)
        self.sld4.setGeometry(30, 40, 100, 30)

        self.sld5 = QtWidgets.QSlider(QtCore.Qt.Vertical, self)
        self.sld5.setRange(0,255)
        self.sld5.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld5.setValue(self.blue_min)
        self.sld5.setGeometry(30, 40, 100, 30)

        self.sld6 = QtWidgets.QSlider(QtCore.Qt.Vertical, self)
        self.sld6.setRange(0,255)
        self.sld6.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sld6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld6.setValue(self.blue_max)
        self.sld6.setGeometry(30, 40, 100, 30)

        self.sld7 = QtWidgets.QSlider(QtCore.Qt.Vertical, self)
        self.sld7.setRange(0,255)
        self.sld7.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld7.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld7.setValue(self.green_blue_ratio_min)
        self.sld7.setGeometry(30, 40, 100, 30)

        self.sld8 = QtWidgets.QSlider(QtCore.Qt.Vertical, self)
        self.sld8.setRange(0,255)
        self.sld8.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sld8.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld8.setValue(self.green_blue_ratio_max)
        self.sld8.setGeometry(30, 40, 100, 30)

        self.sld9 = QtWidgets.QSlider(QtCore.Qt.Vertical, self)
        self.sld9.setRange(0,255)
        self.sld9.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld9.setValue(self.red_green_ratio_min)
        self.sld9.setGeometry(30, 40, 100, 30)

        self.sld10 = QtWidgets.QSlider(QtCore.Qt.Vertical, self)
        self.sld10.setRange(0,255)
        self.sld10.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sld10.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld10.setValue(self.red_green_ratio_max)
        self.sld10.setGeometry(30, 40, 100, 30)

        self.button1 = QtWidgets.QPushButton("Run")
        self.onFlag = False
        
        self.button2 = QtWidgets.QPushButton("Cluster")
        self.clusterFlag = False

        self.buttonRed = QtWidgets.QPushButton("RED")
        self.buttonGreen = QtWidgets.QPushButton("GREEN")
        self.buttonBlue = QtWidgets.QPushButton("BLUE")

        self.buttonGreenBlueRatio = QtWidgets.QPushButton("GREEN/BLUE")
        self.buttonRedGreenRatio = QtWidgets.QPushButton("RED/GREEN")

        layout = QtWidgets.QGridLayout()
        #layout.addWidget(self.dial, 0,0)
        #layout.addWidget(self.zerospinbox, 0,1)
        layout.addWidget(self.button1, 0, 0)
        layout.addWidget(self.button2, 0, 2)
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
        self.connect(self.button2,SIGNAL("clicked()"),self.button_2)

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

    def button_2(self):
        if self.clusterFlag == False:
            self.clusterFlag = True
            self.button2.setText("Cluster")
        else:
            self.clusterFlag = False
            self.button2.setText("Cluster")

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


############ Main Viewing Window ##############################################
class Viewer(QtWidgets.QMainWindow):

    def __init__(self):
        super(Viewer, self).__init__()

        self.initUI()
        global ROI_flag
        ROI_flag = False
#    def mousePressEvent(self, QtGui.QMouseEvent):
#        print (QMouseEvent.pos())
#
#    def mouseReleaseEvent(self, QtGui.QMouseEvent):
#        cursor =QtGui.QCursor()
#        print (cursor.pos())  

    def initUI(self):

        self.ImageView = pg.ImageView(view=pg.PlotItem())
        self.resize(800,800)
        self.setCentralWidget(self.ImageView)
        self.statusBar()
        self.setMouseTracking(True)

        #self.cursor =QtGui.QCursor()

        openImage = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Open image', self)
        openImage.setShortcut('Ctrl+O')
        openImage.setStatusTip('Open new Image')
        openImage.triggered.connect(self.openDialog)

        saveFile = QtWidgets.QAction(QtGui.QIcon('save.png'), 'Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.saveDialog)

        rotateCounter = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Rotate Counterclock', self)
        rotateCounter.setShortcut('Ctrl+<')
        rotateCounter.setStatusTip('Rotate Counterclock')
        rotateCounter.triggered.connect(self.rotateImageCounter)

        rotateClock = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Rotate Clock', self)
        rotateClock.setShortcut('Ctrl+>')
        rotateClock.setStatusTip('Rotate Clock')
        rotateClock.triggered.connect(self.rotateImageClock)

        rotateCounter_90 = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Rotate Counterclock 90', self)
        rotateCounter_90.setShortcut('Ctrl+9')
        rotateCounter_90.setStatusTip('Rotate Counterclock 90')
        rotateCounter_90.triggered.connect(self.rotateImageCounter_90)

        rotateClock_90 = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Rotate Clock 90', self)
        rotateClock_90.setShortcut('Ctrl+0')
        rotateClock_90.setStatusTip('Rotate Clock 90')
        rotateClock_90.triggered.connect(self.rotateImageClock_90)

        flipLR = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Flip Vertical', self)
        flipLR.setShortcut('Ctrl+7')
        flipLR.setStatusTip('Flip vertical')
        flipLR.triggered.connect(self.flipImageLR)

        flipUD = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Flip Horizontal', self)
        flipUD.setShortcut('Ctrl+8')
        flipUD.setStatusTip('Flip horizontal')
        flipUD.triggered.connect(self.flipImageUD)

        invert = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Invert', self)
        invert.setShortcut('Ctrl+I')
        invert.setStatusTip('Invert')
        invert.triggered.connect(self.invert)

        rgbToGray = QtWidgets.QAction(QtGui.QIcon('open.png'), 'RGB to Grayscale', self)
        rgbToGray.setShortcut('Ctrl+G')
        rgbToGray.setStatusTip('RGB to Gray')
        rgbToGray.triggered.connect(self.rgb2grayscale)

        getRedChannel = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Get Red Channel', self)
        getRedChannel.setShortcut('Ctrl+R')
        getRedChannel.setStatusTip('Get Red')
        getRedChannel.triggered.connect(self.get_red)

        getGreenChannel = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Get Green Channel', self)
        getGreenChannel.setShortcut('Ctrl+G')
        getGreenChannel.setStatusTip('Get Green')
        getGreenChannel.triggered.connect(self.get_green)

        getBlueChannel = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Get Blue Channel', self)
        getBlueChannel.setShortcut('Ctrl+B')
        getBlueChannel.setStatusTip('Get Blue')
        getBlueChannel.triggered.connect(self.get_blue)

        denoiseBilateral = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Denoise Bilateral', self)
        denoiseBilateral.setShortcut('Ctrl+D')
        denoiseBilateral.setStatusTip('denoise_bilateral')
        denoiseBilateral.triggered.connect(self.denoise_bilateral_filter)

        gaussFilter = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Gaussian Filter', self)
        gaussFilter.setShortcut('Ctrl+T')
        gaussFilter.setStatusTip('Gaussian Filter')
        gaussFilter.triggered.connect(self.gaussianFilter)
        
        cropImg = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Crop', self)
        cropImg.setShortcut('Ctrl+X')
        cropImg.setStatusTip('Crop')
        cropImg.triggered.connect(self.cropImage)       

        binImg = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Re-size ', self)
        binImg.setShortcut('Ctrl+L')
        binImg.setStatusTip('Bin')
        binImg.triggered.connect(self.binImage)  
        
        otsuThresh = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Otsu Threshold', self)
        otsuThresh.setShortcut('Ctrl+W')
        otsuThresh.setStatusTip('OtsuThresh')
        otsuThresh.triggered.connect(self.otsuThreshold)
               
        getOriginal = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Reset to Original', self)
        getOriginal.setShortcut('Ctrl+Z')
        getOriginal.setStatusTip('get_original')
        getOriginal.triggered.connect(self.get_original)

        quitApp = QtWidgets.QAction(QtGui.QIcon('save.png'), 'Quit Now', self)
        quitApp.setShortcut('Ctrl+Q')
        quitApp.setStatusTip('Quit')
        quitApp.triggered.connect(self.quitDialog)

        activateExaminer = QtWidgets.QAction(QtGui.QIcon('save.png'), 'ROI Examiner', self)
        activateExaminer.setShortcut('Ctrl+E')
        activateExaminer.setStatusTip('Start Examiner')
        activateExaminer.triggered.connect(self.startROIExaminer)

        activateConsole = QtWidgets.QAction(QtGui.QIcon('save.png'), 'ROI Console', self)
        activateConsole.setShortcut('Ctrl+R')
        activateConsole.setStatusTip('Start Console')
        activateConsole.triggered.connect(self.initConsole_CoverBoard)
        
        activateConsoleCanopy = QtWidgets.QAction(QtGui.QIcon('save.png'), 'Canopy Console', self)
        activateConsoleCanopy.setShortcut('Ctrl+N')
        activateConsoleCanopy.setStatusTip('Start Console')
        activateConsoleCanopy.triggered.connect(self.initConsole_Canopy)
        activateConsoleCanopy.triggered.connect(self.startROIExaminer)
        
        activateAnalysisConsole = QtWidgets.QAction(QtGui.QIcon('save.png'), 'Analysis Console', self)
        activateAnalysisConsole.setShortcut('Ctrl+A')
        activateAnalysisConsole.setStatusTip('Start Analysis')
        activateAnalysisConsole.triggered.connect(self.initConsole_Analysis)
        
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
        fileMenu1.addAction(getRedChannel)
        fileMenu1.addAction(getGreenChannel)
        fileMenu1.addAction(getBlueChannel)
        fileMenu1.addAction(denoiseBilateral)
        fileMenu1.addAction(gaussFilter)
        #fileMenu1.addAction(otsuThresh)
        fileMenu1.addAction(binImg)      
        fileMenu1.addAction(cropImg)
        fileMenu1.addAction(getOriginal)

        fileMenu2 = menubar.addMenu("&Quit")
        fileMenu2.addAction(quitApp)

        fileMenu3 = menubar.addMenu('&ROI Examiner')
        fileMenu3.addAction(activateExaminer)
        fileMenu3.addAction(activateConsole)
        
        fileMenu4 = menubar.addMenu('&Canopy Detection')       
        fileMenu4.addAction(activateConsoleCanopy)
        
        fileMenu5 = menubar.addMenu('&Random Point Analysis')       
        fileMenu5.addAction(activateAnalysisConsole)        

#        fileMenu3 = menubar.addMenu('&Analysis')
#        fileMenu3.addAction(analysis1)

        #self.setGeometry(300, 300, 350, 300)

        self.setWindowTitle('ImageView')

        #self.initROI()
        self.show()

    def initConsole_CoverBoard(self):
        self.console = Console_Coverboard()
        #self.console.connect(self.console.button1,SIGNAL("clicked()"),self.testPrint)
        self.console.connect(self.console.button1,SIGNAL("clicked()"),self.detect_coverBoard)
        self.console.connect(self.console.button2,SIGNAL("clicked()"),self.cluster_coverBoard)
        self.console.show()

    def initConsole_Canopy(self):
        self.consoleCanopy = Console_Canopy()
        #self.consoleCanopy.connect(self.consoleCanopy.button1,SIGNAL("clicked()"),self.testPrint)
        self.consoleCanopy.connect(self.consoleCanopy.button1,SIGNAL("clicked()"),self.detect_canopy)
        self.consoleCanopy.connect(self.consoleCanopy.button5,SIGNAL("clicked()"),self.batch_canopy)
        self.consoleCanopy.show()


    def initConsole_Analysis(self):
        self.AnalysisCanopy = Console_Analysis()
        #self.consoleCanopy.connect(self.consoleCanopy.button1,SIGNAL("clicked()"),self.testPrint)
        self.AnalysisCanopy.show()


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
            #no rotation needed yet
            #self.roi1.addRotateHandle([1,0], [0.5, 0.5])
            self.roi1.sigRegionChanged.connect(updateROI)
            self.roi1.sigRegionChanged.connect(self.updateWin)
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
        global newimg, original_image, ROI_flag
        newimg = io.imread(filename)
        original_image = copy.deepcopy(newimg)
        newimg = np.rot90(newimg,k=1)
        newimg = np.flipud(newimg)
        self.statusBar().showMessage('{} successfully loaded ({} s)'.format(os.path.basename(filename), time.time()-t))
        
        if ROI_flag == False:
            self.initROI()
            ROI_flag = True
        
        return newimg


    def openDialog(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image file',
                '/home', 'Images (*.png *.xpm *.jpg *.tif *.tiff *.pdf *.ps *.eps *.raw)')
        filename=str(filename[0])
        if filename=='':
            return False
        else:
            data = self.open_image(filename)
            print(len(data.shape))
            self.ImageView.setImage(data)


    def saveDialog(self):
        fname = (QtWidgets.QFileDialog.getSaveFileName
                 (self, 'Save file', None,
                  "RAW (*.raw);;EPS (*.eps);;PS (*.ps);;PNG (*.png);;TIFF (*.tiff);;JPEG (*.jpg);;PDF (*.pdf);;All Files (*)"))
        
        t=time.time()
        self.statusBar().showMessage('Saving {}'.format(os.path.basename(fname)))
        
        img = self.ImageView.getProcessedImage()
        img = np.rot90(img,k=1)
        img = np.flipud(img)
        plt.imsave(fname, img)
        self.statusBar().showMessage('{} successfully saved ({} s)'.format(os.path.basename(fname), time.time()-t))
        return
        

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
        img = rgb2gray(img)
        #reset datatype to unit8 for RGB 0-255
        newimg = img_as_ubyte(img)
        self.ImageView.setImage(newimg)
        return

    def get_red(self):
        #convert by mean channel value
        self.statusBar().showMessage('Working...')
        try:
            img = self.ImageView.getProcessedImage()
            global newimg     
            newimg = img[:, :, 0]
            self.ImageView.setImage(newimg)
            self.statusBar().showMessage('Finished Extracting Red Channel')
        except:
            self.statusBar().showMessage('No Red Channel Detected')
        return

    def get_green(self):
        #convert by mean channel value
        self.statusBar().showMessage('Working...')
        try:
            img = self.ImageView.getProcessedImage()
            global newimg     
            newimg = img[:, :, 1]
            self.ImageView.setImage(newimg)
            self.statusBar().showMessage('Finished Extracting Green Channel')
        except:
            self.statusBar().showMessage('No Green Channel Detected')
        return

    def get_blue(self):
        #convert by mean channel value
        self.statusBar().showMessage('Working...')
        try:
            img = self.ImageView.getProcessedImage()
            global newimg     
            newimg = img[:, :, 2]
            self.ImageView.setImage(newimg)
            self.statusBar().showMessage('Finished Extracting Blue Channel')
        except:
            self.statusBar().showMessage('No Blue Channel Detected')
        return

    def denoise_bilateral_filter(self):
        self.statusBar().showMessage('Working...')
        img = self.ImageView.getProcessedImage()
        global newimg
        img = denoise_bilateral(img, multichannel = True)
        #reset datatype to unit8 for RGB 0-255
        newimg = img_as_ubyte(img)
        self.ImageView.setImage(newimg)
        self.statusBar().showMessage('Finished Bilateral Filter')
        return

    def gaussianFilter(self):
        self.statusBar().showMessage('Working...')
        img = self.ImageView.getProcessedImage()
        global newimg
        newimg = gaussian(img, sigma = 1)
        newimg = img_as_ubyte(newimg)
        self.ImageView.setImage(newimg)
        self.statusBar().showMessage('Finished Gaussian Filter')
        return

    def cropImage(self):
        self.statusBar().showMessage('Working...')
        
        global newimg, roi_origin, roi_size
        img = newimg

        #set image size variables
        image_x_origin = int(roi_origin[0])
        image_y_origin = int(roi_origin[1])
        image_x_end = image_x_origin + int(roi_size[0])
        image_y_end = image_y_origin + int(roi_size[1])

        crop = img[image_x_origin:image_x_end, image_y_origin:image_y_end]
        newimg = crop
        self.ImageView.setImage(newimg)
        self.statusBar().showMessage('Finished Cropping')
        return

    def binImage(self):
        self.statusBar().showMessage('Working...')
        img = self.ImageView.getProcessedImage()
        global newimg
        x,y = img.shape[0:2]
        newimg = resize(img,(int(x/2),int(y/2)),preserve_range=False)
        newimg = img_as_ubyte(newimg)
        self.ImageView.setImage(newimg)
        self.statusBar().showMessage('Finished Binning')
        return

    def otsuThreshold(self):
        self.statusBar().showMessage('Working...')
        img = self.ImageView.getProcessedImage()
        global newimg
        #threshold 
        img = rgb2gray(img)
        img = img.astype(np.uint8)
        #img = np.invert(img)       
        # apply threshold
        thresh = threshold_otsu(img)
        newimg = img >= thresh
        self.ImageView.setImage(newimg)
        self.statusBar().showMessage('Finished Otsu Threshold')
        return

    def get_original(self):
        global newimg, original_image
        newimg = original_image
        newimg = np.rot90(newimg,k=1)
        newimg = np.flipud(newimg)
        self.ImageView.setImage(newimg)
        return

    def updateWin(self):
            
        global roi_mean_red, roi_mean_green, roi_mean_blue, roi_mean_intensity
       
        try:
            self.v1a.removeItem(self.img)
        except:
            print('no examiner created yet')
        self.imgROI = self.roiImg
        self.imgROI = np.fliplr(self.imgROI)
        self.img = pg.ImageItem(self.imgROI)

        try:
            self.v1a.addItem(self.img)
        except:
            pass

        roi_mean_red = np.mean(self.imgROI[:, :, 0])
        roi_mean_green = np.mean(self.imgROI[:, :, 1])
        roi_mean_blue = np.mean(self.imgROI[:, :, 2])
        roi_mean_intensity = np.mean(self.imgROI[:, :, :,])
        self.roi_numberPixels = np.size(self.imgROI[:, :, 0])
        
        self.statusBar().showMessage("Mean Red: %d, Mean Green: %d, Mean Blue: %d, Mean Intensity: %d, Number of pixels: %d" % (roi_mean_red, roi_mean_green, roi_mean_blue, roi_mean_intensity, self.roi_numberPixels))
        #print("Mean Red: %d, Mean Green: %d, Mean Blue: %d" % (self.roi_mean_red, self.roi_mean_green, self.roi_mean_blue))
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
        self.statusBar()
        self.w = pg.GraphicsWindow(size=(500,400), border=True)
        self.w.setWindowTitle('ROI Examiner')
        self.w1 = self.w.addLayout(row=0, col=0)

        self.v1a = self.w1.addViewBox(row=0, col=0, lockAspect=True)
        self.imgROI = np.fliplr(self.imgROI)
        self.img = pg.ImageItem(self.imgROI)
        self.v1a.addItem(self.img)
        
        self.w.setMouseTracking(True)

        #link change in roi signal to update
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
        print("----------------------------------------------")
        print("Area of ROI detected as board = ", round((board_pixel/roi_area)*100, 1), " %")
        print("Area of ROI detected as other = ", round((other_pixel/roi_area)*100, 1), " %")

        #plot result
        image_board = np.rot90(image_board, k=1)
        image_board = np.flipud(image_board)
        self.imageBoard = copy.deepcopy(image_board)

#        #using matplotlib
#        plt.imshow(image_board)
#        plt.show()

#        ###using skimage - it searches for suitable backend package###
#        io.imshow(image_board)
#        io.show()

        #using pyqtgraph.image
        image_board = np.rot90(image_board, k=1)
        image_board = np.flipud(image_board)        
        resultCoverBoard = pg.image(image_board)

    def cluster_coverBoard(self):
                
        #threshold and find clusters
        image = rgb2gray(self.imageBoard)
        image = image.astype(np.uint8)
        image = np.invert(image)
        
        # apply threshold
        thresh = threshold_otsu(image)
        # close holes
        bw = closing(image > thresh, square(3))
        
        # remove artifacts connected to image border
        cleared = clear_border(bw)
        
        # label image regions
        label_image = label(cleared, background=0)
        image_label_overlay = label2rgb(label_image, image=image)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(image_label_overlay)
        
        total_area = 0
        centeroid = (0,0)
        largest_region_area = 0
        
        for region in regionprops(label_image):
            # take regions with large enough areas
            if region.area >= 50:
                area = region.area
                if area > largest_region_area:
                    centeroid = region.centroid
                    largest_region_area = area
                    
                # draw rectangle around segmented areas
                minr, minc, maxr, maxc = region.bbox
                rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                          fill=False, edgecolor='red', linewidth=1)
                
                ax.add_patch(rect)
                total_area += area
            area = 0
        
        rect2 = mpatches.Circle((centeroid[1],centeroid[0]))
        ax.add_patch(rect2)
        
        
        ax.set_axis_off()
        plt.tight_layout()
        plt.show()
                
        print ("total # of pixels detected in board = ", total_area)
     
################################################################################################
    def detect_canopy(self):
        print('start analysis')
        #set up arrays
        global newimg, roi_origin, roi_size
        image = newimg
       
        #set limits for thresholding by brightness
        dark_threshold = self.consoleCanopy.intensity_min
        light_threshold = self.consoleCanopy.intensity_max
        
        #set up arrays
        image_bright_adjusted = copy.deepcopy(image)
        image_sky = copy.deepcopy(image)
        image_canopy = copy.deepcopy(image)
        image_equivalent = copy.deepcopy(image)

        #set image size variables
        image_x, image_y = image.shape[0:2]
        
        #image array index
        r = 0
        g = 1
        b = 2
        
        # colour settings   
        red = [255,0,0]
        green = [0,255,0]
        blue = [0,0,255]
        black = [0,0,0]
        white = [255,255,255]    
        
        #pixel count variables  
        sky_pixel = 0
        canopy_pixel = 0
        equivalent_pixel = 0
        
        #progress counters
        first_loop = 0
        second_loop = 0
        total_pixels = image_x*image_y
               
        #loop through all pixels in image and assign brightest pixels to sky and darkest pixels to canopy (by setting colour)
        for x in range (image_x):
            print("1st loop % complete = ", round((first_loop/image_x)*100,1))
            first_loop +=1
            for y in range (image_y):
                #remove pixels from sky and add to canopy if below darkness threshold
                if np.mean(image[x,y]) < dark_threshold:
                    image_bright_adjusted[x,y] = green
                #make white pixels blue to ensure they are counted
                if np.mean(image[x,y]) > light_threshold:
                    image_bright_adjusted[x,y] = blue
        
        
        #loop through all pixels in image and set pixel to sky or canopy based on colour - count pixels   
        for x in range (image_x):
            print("2nd loop % complete = ", round((second_loop/image_x)*100,1))
            second_loop +=1
            for y in range (image_y):
                #pixels with equivalent values
                if (image_bright_adjusted[x,y][b] == image_bright_adjusted[x,y][g]):
                    image_sky[x,y] = 255
                    image_canopy[x,y] = 255
                    image_equivalent[x,y] = 0
                    equivalent_pixel += 1
        
                #count red canopy pixels
                elif (image_bright_adjusted[x,y][r] > image_bright_adjusted[x,y][g] 
                        and image_bright_adjusted[x,y][r] > image_bright_adjusted[x,y][b]):
                    image_canopy[x,y] = 0
                    image_sky[x,y] = 255
                    image_equivalent[x,y] = 255
                    canopy_pixel += 1
                    
                #count green canopy pixels   
                elif (image_bright_adjusted[x,y][g] > image_bright_adjusted[x,y][r] 
                        and image_bright_adjusted[x,y][g] > image_bright_adjusted[x,y][b]):
                    image_sky[x,y] = 255
                    image_canopy[x,y] = 0
                    image_equivalent[x,y] = 255
                    canopy_pixel += 1
        
                #count blue sky pixels 
                elif (image_bright_adjusted[x,y][b] > image_bright_adjusted[x,y][r]
                        and image_bright_adjusted[x,y][b] > image_bright_adjusted[x,y][g]):
                    image_canopy[x,y] = 255
                    image_equivalent[x,y] = 255
                    image_sky[x,y] = 0
                    sky_pixel += 1
                
                else:
                    image_sky[x,y] = 255
                    image_canopy[x,y] = 255
                    image_equivalent[x,y] = 0
                    equivalent_pixel += 1
                            
       
        print ("sky: %.2f" % (sky_pixel/(total_pixels)*100), "%")
        print ("canopy: %.2f" % (canopy_pixel/(total_pixels)*100), "%")
        print ("unassigned: %.2f" % (equivalent_pixel/(total_pixels)*100), "%")
        print ("total pixels counted = ", sky_pixel + canopy_pixel + equivalent_pixel)

        #plot result
    

#        #matplotlib
#        image_sky = np.rot90(image_sky, k=1)
#        image_sky = np.flipud(image_sky)
#        
#        image_canopy = np.rot90(image_canopy, k=1)
#        image_canopy = np.flipud(image_canopy)       
#        plt.imshow(image_sky)
#        plt.show()

        #using pyqtgraph.image       
        resultSky = pg.image(image_sky)

        return

    def batch_canopy(self):
        path = self.consoleCanopy.pathname
        files = os.listdir(path)
        dark_threshold = self.consoleCanopy.intensity_min
        light_threshold = self.consoleCanopy.intensity_max
        
        result = []

        def detection(imgData, dark_threshold, light_threshold):
            image = imgData
                       
            #set up arrays
            image_bright_adjusted = copy.deepcopy(image)
            image_sky = copy.deepcopy(image)
            image_canopy = copy.deepcopy(image)
            image_equivalent = copy.deepcopy(image)
    
            #set image size variables
            image_x, image_y = image.shape[0:2]
            
            #image array index
            r = 0
            g = 1
            b = 2
            
            # colour settings   
            red = [255,0,0]
            green = [0,255,0]
            blue = [0,0,255]
            black = [0,0,0]
            white = [255,255,255]    
            
            #pixel count variables  
            sky_pixel = 0
            canopy_pixel = 0
            equivalent_pixel = 0
            
            #progress counters
            #first_loop = 0
            #second_loop = 0
            total_pixels = image_x*image_y

            print("loop 1 start")         
            #loop through all pixels in image and assign brightest pixels to sky and darkest pixels to canopy (by setting colour)
            for x in range (image_x):
                #print("1st loop % complete = ", round((first_loop/image_x)*100,1))
                #first_loop +=1
                for y in range (image_y):
                    #remove pixels from sky and add to canopy if below darkness threshold
                    if np.mean(image[x,y]) < dark_threshold:
                        image_bright_adjusted[x,y] = green
                    #make white pixels blue to ensure they are counted
                    if np.mean(image[x,y]) > light_threshold:
                        image_bright_adjusted[x,y] = blue

            print("loop 1 done")
            print("loop 2 start")            

            #loop through all pixels in image and set pixel to sky or canopy based on colour - count pixels   
            for x in range (image_x):
                #print("2nd loop % complete = ", round((second_loop/image_x)*100,1))
                #second_loop +=1
                for y in range (image_y):
                    #pixels with equivalent values
                    if (image_bright_adjusted[x,y][b] == image_bright_adjusted[x,y][g]):
                        image_sky[x,y] = 255
                        image_canopy[x,y] = 255
                        image_equivalent[x,y] = 0
                        equivalent_pixel += 1
            
                    #count red canopy pixels
                    elif (image_bright_adjusted[x,y][r] > image_bright_adjusted[x,y][g] 
                            and image_bright_adjusted[x,y][r] > image_bright_adjusted[x,y][b]):
                        image_canopy[x,y] = 0
                        image_sky[x,y] = 255
                        image_equivalent[x,y] = 255
                        canopy_pixel += 1
                        
                    #count green canopy pixels   
                    elif (image_bright_adjusted[x,y][g] > image_bright_adjusted[x,y][r] 
                            and image_bright_adjusted[x,y][g] > image_bright_adjusted[x,y][b]):
                        image_sky[x,y] = 255
                        image_canopy[x,y] = 0
                        image_equivalent[x,y] = 255
                        canopy_pixel += 1
            
                    #count blue sky pixels 
                    elif (image_bright_adjusted[x,y][b] > image_bright_adjusted[x,y][r]
                            and image_bright_adjusted[x,y][b] > image_bright_adjusted[x,y][g]):
                        image_canopy[x,y] = 255
                        image_equivalent[x,y] = 255
                        image_sky[x,y] = 0
                        sky_pixel += 1
                    
                    else:
                        image_sky[x,y] = 255
                        image_canopy[x,y] = 255
                        image_equivalent[x,y] = 0
                        equivalent_pixel += 1

            print("loop 2 done")

            return image_sky, image_canopy, sky_pixel, canopy_pixel, equivalent_pixel, total_pixels            

        
        for filename in files:
            openName = path + "/" + filename
            saveName = path + "/result_" + filename
            print("Working on... " + openName)
            try:
                imageFile = io.imread(openName)
                image_sky, image_canopy, sky_pixel, canopy_pixel, equivalent_pixel, total_pixels  = detection(imageFile, dark_threshold, light_threshold)
    #            print ("sky: %.2f" % (sky_pixel/(total_pixels)*100), "%")
    #            print ("canopy: %.2f" % (canopy_pixel/(total_pixels)*100), "%")
    #            print ("unassigned: %.2f" % (equivalent_pixel/(total_pixels)*100), "%")
    #            print ("total pixels counted = ", sky_pixel + canopy_pixel + equivalent_pixel)
                plt.imsave(saveName, image_sky)
                result.append([str(openName),str(sky_pixel),str(canopy_pixel),str(equivalent_pixel), str(total_pixels)])
                print("Finshed with... " + openName)
            except:
                print("Non-image file detected")
        
        print("Batch run complete!")
#        result = np.array(result)
        print(result)
#        resultSummaryName = path + "/results.txt"
#        np.savetxt(resultSummaryName, result, delimiter=" ", fmt="%s")
#        print("Result File Saved")
        
        return


###############################################################################

    def quitDialog(self):
        self.ImageView.close()
        try:
            self.console.close()
            self.consoleCanopy.close()
            self.AnalysisCanopy.close()
        except:
            print("console close error_1")
        
        plt.close()
        if QtCore.QCoreApplication.instance() != None:
            app = QtCore.QCoreApplication.instance()
        else:
            app = QtWidgets.QApplication(sys.argv)
        sys.exit(app.exec_())
        return


    def closeEvent(self, event):
         #==============================================================================
         #       If we close a QtGui.QWidget, a QtGui.QCloseEvent is generated.
         #       To modify the widget behaviour we need to reimplement the closeEvent() event handler.
         #==============================================================================
        reply = QtWidgets.QMessageBox.question(self, 'Message',
            "Are you sure you wish to quit?", QtWidgets.QMessageBox.Yes |
            QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            try:
                self.console.close()
                self.consoleCanopy.close()
                self.AnalysisCanopy.close()
                
            except:
                print("console close error_2")
            
            plt.close()

        else:
            event.ignore()


            
##############################################################################
############ create main run loop for GUI ####################################
##############################################################################
def main():
    if QtCore.QCoreApplication.instance() != None:
        app = QtCore.QCoreApplication.instance()
    else:
        app = QtWidgets.QApplication(sys.argv)
    ex = Viewer()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
