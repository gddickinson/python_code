# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 12:14:34 2015

@author: george
"""
############# Import packages ################################################
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
#from future.builtins import (bytes, dict, int, list, object, range, str,
#                             ascii, chr, hex, input, next, oct, open,
#                             pow, round, super, filter, map, zip)

import time
tic=time.time()
import os, sys
import platform

if platform.system() != "Darwin":
    if (sys.version_info < (3, 0)):
        # Python 3 code in this block
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
from skimage.color import rgb2gray, rgb2hsv, rgb2lab, hsv2rgb, lab2rgb
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
from skimage.color import label2rgb, rgb2lab
from scipy.ndimage import interpolation
from skimage import img_as_ubyte

import cv2
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *


import serial
import io
from skimage.io import imread
import serial.tools.list_ports

if sys.version_info[:2]<(2,5):
    def partial(func,arg):
        def callme():
            return func(arg)
        return callme
else:
    from functools import partial



########### define global variables ##########################################

global roi_mean_hue, roi_mean_sat, roi_mean_val, roi_min_hue, roi_min_sat, \
        roi_min_val, roi_max_hue, roi_max_sat, roi_max_val, colourSpace, filename, \
        ROI_flag, roi_origin, roi_size, newimg, original_image, sky_array, canopy_array, \
        sky_mean, sky_n, sky_sd, canopy_mean, canopy_n, canopy_sd, roi_mean_red, roi_mean_green, \
        roi_mean_blue, roi_mean_intensity, roi_min_intensity, roi_max_intensity, roi_min_red, \
        roi_max_red, roi_min_green, roi_max_green, roi_min_blue, roi_max_blue, board_min_red, \
        board_max_red, board_mean_red, board_min_green, board_max_green, board_mean_green, \
        board_min_blue, board_max_blue, board_mean_blue, board_min_intensity, board_max_intensity, \
        board_mean_intensity, board_mean_hue, board_mean_sat, board_mean_val, board_min_hue, \
        board_min_sat, board_min_val, board_max_hue, board_max_sat, board_max_val, picker_RGB, \
        picker_HSV, picker_HSL 


########### helper functions ##################################################
def RGB_2_HSV(RGB):
    ''' Converts an integer RGB tuple (value range from 0 to 255) to an HSV tuple '''

    # Unpack the tuple for readability
    R, G, B = RGB

    # Compute the H value by finding the maximum of the RGB values
    RGB_Max = max(RGB)
    RGB_Min = min(RGB)

    # Compute the value
    V = RGB_Max;
    if V == 0:
        H = S = 0
        return (H,S,V)


    # Compute the saturation value
    S = 255 * (RGB_Max - RGB_Min) // V

    if S == 0:
        H = 0
        return (H, S, V)

    # Compute the Hue
    if RGB_Max == R:
        H = 0 + 43*(G - B)//(RGB_Max - RGB_Min)
    elif RGB_Max == G:
        H = 85 + 43*(B - R)//(RGB_Max - RGB_Min)
    else: # RGB_MAX == B
        H = 171 + 43*(R - G)//(RGB_Max - RGB_Min)

    return (H, S, V)

def HSV_2_RGB(HSV):
    ''' Converts an integer HSV tuple (value range from 0 to 255) to an RGB tuple '''

    # Unpack the HSV tuple for readability
    H, S, V = HSV

    # Check if the color is Grayscale
    if S == 0:
        R = V
        G = V
        B = V
        return (R, G, B)

    # Make hue 0-5
    region = H // 43;

    # Find remainder part, make it from 0-255
    remainder = (H - (region * 43)) * 6; 

    # Calculate temp vars, doing integer multiplication
    P = (V * (255 - S)) >> 8;
    Q = (V * (255 - ((S * remainder) >> 8))) >> 8;
    T = (V * (255 - ((S * (255 - remainder)) >> 8))) >> 8;


    # Assign temp vars based on color cone region
    if region == 0:
        R = V
        G = T
        B = P

    elif region == 1:
        R = Q; 
        G = V; 
        B = P;

    elif region == 2:
        R = P; 
        G = V; 
        B = T;

    elif region == 3:
        R = P; 
        G = Q; 
        B = V;

    elif region == 4:
        R = T; 
        G = P; 
        B = V;

    else: 
        R = V; 
        G = P; 
        B = Q;


    return (R, G, B)


class Arduino():   
    def __init__(self,Port='COM3',Boud=115200,connState=0): 
        self.parent=self
        self.port=Port
        self.boud=Boud
        self.connState=connState
        self.timeout=0.001
        self.ser=None
        self.connect()


    def connect(self): 
        try:
            self.ser=serial.Serial(self.port,self.boud,timeout=self.timeout)
            self.connState=1
            print('connected')
            return [1,'connect']
        except:
            self.connState=0
            print('no hardware found')
            return [0,'no hardware found']


    def loadData(self):     
        self.buffer=self.ser.read(1)        
        if (self.buffer!=''):
            try:
                print (self.buffer)
            except Exception:
                pass

    def getSonar(self):    
        a=0
        b=0
        c=0
        read =self.ser.read(30)
        try:
            newData = str(read)
            if "A" in newData:
                a = (int(newData.split('A')[1].split(")")[0]))
            if "B" in newData:
                b = (int(newData.split('B')[1].split(")")[0]))
            if "C" in newData:
                c = (int(newData.split('C')[1].split(")")[0]))
            self.data = newData
            return  [a,b,c]
        
        except Exception:
            print("no data")

        
    def getData(self):
        return self.data

    def close(self):
        self.ser.close()


class Arduino_Motor():   
    def __init__(self,Port='COM4',Boud=19200,connState=0): 
        self.parent=self
        self.port=Port
        self.boud=Boud
        self.connState=connState
        self.timeout= 0.001
        self.ser=None
        self.connect()


    def connect(self): 
        try:
            self.ser=serial.Serial(self.port,self.boud,timeout=self.timeout)
            self.connState=1
            print('motor board connected')
            return [1,'connect']
        except:
            self.connState=0
            print('no motor board found')
            return [0,'no hardware found']


    def loadData(self):     
        self.buffer=self.ser.read(1)        
        if (self.buffer!=''):
            try:
                print (self.buffer)
            except Exception:
                pass

    def forward(self, move_time = 0.3, power = 150):
        startTime = time.time()
        newTime = startTime
        self.ser.write(b'$F150Z')
        while newTime < startTime + move_time:
            newTime = time.time()
            pass
        self.ser.write(b'$F0Z')
        self.ser.flush()

    def back(self,move_time = 0.3, power = 150):
        startTime = time.time()
        newTime = startTime
        self.ser.write(b'$B150Z')
        while newTime < startTime + move_time:     
            newTime = time.time()
            pass
        self.ser.write(b'$B0Z')
        self.ser.flush()

    def left(self,move_time = 0.3, power = 150):
        startTime = time.time()
        newTime = startTime
        self.ser.write(b'$L255Z')
        self.ser.write(b'$R-255Z')
        while newTime < startTime + move_time:     
            newTime = time.time()
            pass
        self.ser.write(b'$L0Z')
        self.ser.write(b'$R0Z')
        self.ser.flush()

    def right(self,move_time = 0.3, power = 150):
        startTime = time.time()
        newTime = startTime
        self.ser.write(b'$R255Z')
        self.ser.write(b'$L-255Z')
        while newTime < startTime + move_time:     
            newTime = time.time()
            pass
        self.ser.write(b'$R0Z')
        self.ser.write(b'$L0Z')
        self.ser.flush()

    def armLeft(self, move_time = 0.5, power = 200):
        self.ser.write(b'$S200Z')
        time.sleep(move_time)
        self.ser.write(b'$S0Z')
        self.ser.flush()

    def armRight(self, move_time = 0.5, power = 200):
        self.ser.write(b'$S-200Z')
        time.sleep(move_time)
        self.ser.write(b'$S0Z')
        self.ser.flush()

    def armUp(self, move_time = 0.5, power = 200):
        pass

    def armDown(self, move_time = 0.5, power = 200):
        pass

    def allStop(self):
        self.ser.write(b'$XZ')
        self.ser.flush()

    def close(self):
        self.ser.close()


##############################################################################


##############################################################################
########### define classes for GUI ###########################################
##############################################################################
class BotConsole(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(BotConsole, self).__init__(parent)

        self.ports = list(serial.tools.list_ports.comports()) 
        print(self.ports)

        self.arduino1 = Arduino()
        self.arduino2 = Arduino_Motor()

        if self.arduino1.connState == 1:
            self.sonar = self.arduino1.getSonar()
            #self.sonar = self.arduino1.getData()
        else:
            self.sonar = "Waiting"

        self.button1 = QtWidgets.QPushButton("Forward")
        self.button2 = QtWidgets.QPushButton("Back")
        self.button3 = QtWidgets.QPushButton("Rotate Left")
        self.button4 = QtWidgets.QPushButton("Rotate Right")
        self.button5 = QtWidgets.QPushButton("Arm Left")
        self.button6 = QtWidgets.QPushButton("Arm Right")
        self.button7 = QtWidgets.QPushButton("Arm Up")
        self.button8 = QtWidgets.QPushButton("Arm Down")
        self.button9 = QtWidgets.QPushButton("Get Sonar")
        self.button10 = QtWidgets.QPushButton("Zero Arm")
        self.button11 = QtWidgets.QPushButton("All Stop")
        self.button12 = QtWidgets.QPushButton("Close COMs")
                     

        self.sonar1_text = QtWidgets.QLabel()
        self.sonar1_text.setText(str(self.sonar))


        layout = QtWidgets.QGridLayout()

        layout.addWidget(self.button1, 0, 0)
        layout.addWidget(self.button2, 0, 1)
        layout.addWidget(self.button3, 0, 2)
        layout.addWidget(self.button4, 1, 0)
        layout.addWidget(self.button5, 1, 1)
        layout.addWidget(self.button6, 1, 2)
        layout.addWidget(self.button7, 2, 0)
        layout.addWidget(self.button8, 2, 1)
        layout.addWidget(self.sonar1_text, 3,0)
        layout.addWidget(self.button9, 3,1)
        layout.addWidget(self.button10, 4,0)
        layout.addWidget(self.button11, 4,1)
        layout.addWidget(self.button12, 4,2)

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
        self.connect(self.button10,SIGNAL("clicked()"),self.button_10) 
        self.connect(self.button11,SIGNAL("clicked()"),self.button_11) 
        self.connect(self.button12,SIGNAL("clicked()"),self.button_12)
        
    def button_1(self, move_time = 0.3, power = 150):
        print('Forward: ', move_time," ", power)
        self.arduino2.forward()
        

    def button_2(self, move_time = 0.3, power = 150):
        print('Back: ', move_time," ", power)
        self.arduino2.back()

    def button_3(self, move_time = 0.3, power = 255):
        print('Left: ', move_time," ", power)
        self.arduino2.left()

    def button_4(self, move_time = 0.3, power = 255):
        print('Right: ', move_time," ", power)
        self.arduino2.right()

    def button_5(self, move_time = 0.5, power = 200):
        print('Arm Left: ', move_time," ", power)
        self.arduino2.armLeft()


    def button_6(self, move_time = 0.5, power = 200):
        print('Arm Right: ', move_time," ", power)
        self.arduino2.armRight()
        
    def button_7(self, move_time = 0.3, power = 150):
        print('Arm Up: ', move_time," ", power)


    def button_8(self, move_time = 0.3, power = 150):
        print('Arm Down: ', move_time," ", power)


    def button_9(self):
        try:
            if self.arduino1.connState == 1:
                self.sonar = self.arduino1.getSonar()
                #self.sonar = self.arduino1.getData()
        except:
            self.sonar = "Error"
            print("error")

        self.sonar1_text.setText(str(self.sonar)) 
        return

    def button_10(self):
        sonarRead = self.arduino1.getSonar()[0]
        while sonarRead >19:
            self.arduino2.armRight()
            print (sonarRead)
            time.sleep(0.2)
            newSonarRead = self.arduino1.getSonar()[0]
            if newSonarRead >= sonarRead+5:
                while newSonarRead >= sonarRead+5:
                    self.arduino2.allStop()
                    newSonarRead = self.arduino1.getSonar()[0]
            
            sonarRead = newSonarRead  


    def button_11(self):
        print('All Stop')
        self.arduino2.allStop()

    def button_12(self):
        try: 
            self.arduino2.close()
            print('Motor COMs closed')
        except:
            pass
        try:
            self.arduino1.close()
            print('Sonar COMs closed')
        except:
            pass



###############################################################################


class CameraConsole(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(CameraConsole, self).__init__(parent)
        
        try:
            self.face_cascade =cv2.CascadeClassifier('/Users/George/Documents/GitHub/opencv/data/haarcascades/haarcascade_frontalface_alt.xml')
            if self.face_cascade.empty(): raise Exception("your face_cascade is empty. are you sure, the path is correct ?")
        except: 
            print("No face cascade found")
        
        try:
            self.eye_cascade = cv2.CascadeClassifier('/Users/George/Documents/GitHub//opencv/data/haarcascades/haarcascade_eye.xml')
            if self.eye_cascade.empty(): raise Exception("your eye_cascade is empty. are you sure, the path is correct ?")
        except:
            print("No eye cascade found")
        
        self.colourFlag = 'COLOUR'
        self.savePath = r'C:\Users\George\Pictures\Camera Roll'
        self.cameraFlag = 'OFF'
        self.recordFlag = 'OFF'
        self.playRecordingFlag = "OFF"
        self.framerate = 20.0
        self.framerateMin = 1
        self.framerateMax = 40.0
        self.channelFlag = 'BGR'
        self.channelList = ['BGR', 'Red Mask', 'Green Mask', 'Blue Mask']
        self.faceDetectFlag = "OFF"

        self.filterList = ["None", "Threshold", "Blur", "Edge Detect", "Equalize"]
        self.filterFlag = 'None'


        self.button1 = QtWidgets.QPushButton("Start Camera")
        self.button2 = QtWidgets.QPushButton("Black & White")
        self.button3 = QtWidgets.QPushButton("Start Recording")
        self.button4 = QtWidgets.QPushButton("Play Recording")
        self.button5 = QtWidgets.QPushButton("Take picture")
        self.button6 = QtWidgets.QPushButton("Apply Filter")
        self.button7 = QtWidgets.QPushButton("Detect Faces")
        self.button8 = QtWidgets.QPushButton("Optical Flow")               
        self.button9 = QtWidgets.QPushButton("Track Object")
        
        self.channelBox = QtWidgets.QComboBox()
        self.channelBox.addItems(self.channelList)

        self.filterBox = QtWidgets.QComboBox()
        self.filterBox.addItems(self.filterList)
        
        self.sld1 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sld1.setRange(self.framerateMin,self.framerateMax)
        self.sld1.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld1.setValue(self.framerate)
        #self.sld1.setGeometry(30, 40, 100, 30)

        self.SpinBox1=QtWidgets.QDoubleSpinBox()
        self.SpinBox1.setRange(self.framerateMin,self.framerateMax)
        self.SpinBox1.setValue(self.framerate)

        layout = QtWidgets.QGridLayout()
        
        layout.addWidget(self.button1, 0, 0)
        layout.addWidget(self.button2, 0, 1)
        layout.addWidget(self.button3, 0, 2)
        layout.addWidget(self.button4, 1, 0)
        layout.addWidget(self.button5, 1, 1)
        layout.addWidget(self.button6, 1, 2)
        layout.addWidget(self.button7, 2, 0)
        layout.addWidget(self.button8, 2, 1)
        layout.addWidget(self.button9, 2, 2)
        
        layout.addWidget(self.channelBox, 0,3)
        layout.addWidget(self.filterBox, 1,3)  
        layout.addWidget(self.sld1, 3,0,3,3)  
        layout.addWidget(self.SpinBox1, 3,3) 
     
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
        
        self.connect(self.channelBox,SIGNAL("currentIndexChanged(QString)"),self.channelBox_select)         
        self.connect(self.filterBox,SIGNAL("currentIndexChanged(QString)"),self.filterBox_select) 
        
        self.connect(self.sld1,SIGNAL("valueChanged(int)"), self.slider_1)
        self.connect(self.sld1,SIGNAL("valueChanged(int)"),self.SpinBox1.setValue)
        

    def channelBox_select(self):
        self.channelFlag = self.channelBox.currentText()
        
    def filterBox_select(self):
        self.filterFlag = self.filterBox.currentText()       

    def threshold(self, frame):
        ret, frame = cv2.threshold(frame,127,255,cv2.THRESH_BINARY)
        return frame
 
    def medianBlur (self,frame):
        return cv2.medianBlur(frame,5)
 
    def edgeDetect(self,frame):
        minVal = 100
        maxVal = 200
        return cv2.Canny(frame,minVal,maxVal)
    
    def equalize(self,frame):
        return cv2.equalizeHist(frame)

     
    def button_1(self):
        if self.cameraFlag == "OFF" and self.faceDetectFlag == "OFF":
            try:
                self.video = cv2.VideoCapture(0)
            except:
                print('No Camera Detected')
                return

            try:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                filename = self.savePath + r'\output.avi'
                frameSize = (640,480)
                self.out = cv2.VideoWriter(filename,fourcc, self.framerate, frameSize)
            except:
                print('No codec detected')
        
            self.button1.setText('Stop Camera')
            self.cameraFlag = "ON"
            ret, previousFrame = self.video.read()
            ret, oldFrame = self.video.read()
            
            while(self.video.isOpened()):
                ret, self.frame = self.video.read()
                if self.frame == None:
                    break


                #turn off if face detect 
                if self.faceDetectFlag == "ON":
                    break

                #turn on/off colour mask
    
                if self.channelFlag == "Blue Mask":
                    #self.frame = self.frame[:,:,2]
                    #ret,self.frame = cv2.threshold(self.frame,175,255,cv2.THRESH_BINARY)
                    lower = np.array([85, 30, 4], dtype = "uint8")
                    upper = np.array([221, 89, 51], dtype = "uint8")
                    
                    mask = cv2.inRange(self.frame, lower, upper)
                    self.frame = cv2.bitwise_and(self.frame, self.frame, mask = mask)

                if self.channelFlag == "Green Mask":
                    #uses HSV
                    #self.frame = self.frame[:,:,1]
                    #ret,self.frame = cv2.threshold(self.frame,175,255,cv2.THRESH_BINARY)
                    lower = np.array([29, 86, 6], dtype = "uint8")
                    upper = np.array([64, 255, 255], dtype = "uint8")
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
                    mask = cv2.inRange(self.frame, lower, upper)
                    self.frame = cv2.bitwise_and(self.frame, self.frame, mask = mask)

                if self.channelFlag == "Red Mask":
                    #self.frame = self.frame[:,:,0]
                    #ret,self.frame = cv2.threshold(self.frame,175,255,cv2.THRESH_BINARY)
                    lower = np.array([16, 14, 99], dtype = "uint8")
                    upper = np.array([51, 57, 201], dtype = "uint8")
                    mask = cv2.inRange(self.frame, lower, upper)
                    self.frame = cv2.bitwise_and(self.frame, self.frame, mask = mask)
    
                if self.colourFlag == 'BGR':
                    pass
 
                #set colourspace

                elif self.colourFlag == 'GRAY':
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                    if self.filterFlag == "Equalize":
                        self.frame = self.equalize(self.frame) 
                    
                elif self.colourFlag == 'HSV':
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)      
 
    
                #filters
                if self.filterFlag == "Threshold":
                    self.frame = self.threshold(self.frame)

                if self.filterFlag == "Blur":
                    self.frame = self.medianBlur(self.frame)    
                    
                if self.filterFlag == "Edge Detect":
                    self.frame = self.edgeDetect(self.frame) 

    
                cv2.imshow('Video', self.frame)  
  
                
              
                if self.recordFlag == "ON":
                    #self.frame = cv2.flip(self.frame,0)
                    # write the flipped frame
                    self.out.write(self.frame)
                
                if self.cameraFlag == "OFF":
                    break
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    
            self.video.release()
            self.out.release()
            cv2.destroyAllWindows()
            self.cameraFlag = "OFF"
            self.button1.setText('Start Camera')

        else:
            self.cameraFlag = "OFF"
            self.button1.setText('Start Camera') 
            
        return

    def button_2(self):
        if self.colourFlag == 'GRAY':
            self.colourFlag = 'COLOUR'
            self.button2.setText('Black & White')  
        else:
            self.colourFlag = 'GRAY'
            self.button2.setText('Colour')
    
    def button_3(self):
        if self.cameraFlag == "OFF":
            print ("Camera not on")
            return
        if self.recordFlag == "ON":
            self.recordFlag = "OFF"
            self.button3.setText("Start Recording")
        else:
            self.recordFlag = "ON"
            self.button3.setText("Stop Recording")

    def button_4(self):
        if self.playRecordingFlag == "OFF":
            try:
                filename = self.savePath + r'\output.avi'
                self.recording = cv2.VideoCapture(filename)
            except:
                print('No Recording Detected')
                return
        
            self.button4.setText('Stop Playing')
            self.playRecordingFlag = "ON"
            
            while(self.recording.isOpened()):
                ret, frame = self.recording.read()
                if frame == None:
                    break
    
                if self.colourFlag == 'BGR':
                    pass
                elif self.colourFlag == 'GRAY':
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                elif self.colourFlag == 'HSV':
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)      
    
                cv2.imshow('Recording', frame)  
                
                if self.playRecordingFlag == "OFF":
                    break
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    
            self.recording.release()
            cv2.destroyAllWindows()
            self.playRecordingFlag = "OFF"
            self.button4.setText('Play Recording')

        else:
            self.playRecordingFlag = "OFF"
            self.button4.setText('Play Recording')
            
        return

    def button_5(self):
        global newimg, original_image
        if self.cameraFlag == "OFF":
            if self.faceDetectFlag == "ON":
                img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                img = np.rot90(img,k=1)
                img = np.flipud(img)
                newimg = img
                original_image = newimg
                return               
            print ("No Camera Running")
            return
        else:
            img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            img = np.rot90(img,k=1)
            img = np.flipud(img)
            newimg = img
            original_image = newimg

    def button_6(self):
        print("not implemented")

    def button_7(self):
        if self.faceDetectFlag == 'OFF':
            self.faceDetectFlag = 'ON'
            self.button7.setText('Stop Face Detect')  
            
            self.cameraFlag = "OFF"
            self.button1.setText ("Start Camera")

            
            def playcamera():
                video = cv2.VideoCapture(0)
                
                while(video.isOpened()):
                    ret, self.frame = video.read()
                    if self.frame == None:
                        break
                
                    if self.faceDetectFlag == "OFF":
                        break

                    if self.cameraFlag == "ON":
                        break
                     
                    
                    facedetect(self.frame)        
                    cv2.imshow('Video', self.frame)    
            
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                video.release()
                cv2.destroyAllWindows()
                self.faceDetectFlag = 'OFF'
                self.button7.setText('Detect Faces')                

                return 
            
            def facedetect(gray):
                frame = gray
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = frame[y:y+h, x:x+w]
                    eyes = self.eye_cascade.detectMultiScale(roi_gray)
                    for (ex,ey,ew,eh) in eyes:
                        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)                    
                        if self.cameraFlag == "ON":
                            break
                    
                return
            
            playcamera()
            cv2.destroyAllWindows()
        else:
            self.faceDetectFlag = 'OFF'
            self.button7.setText('Detect Faces')  
        
    def button_8(self):
        cap = cv2.VideoCapture(0)
        
        # params for ShiTomasi corner detection
        feature_params = dict( maxCorners = 100,
                               qualityLevel = 0.3,
                               minDistance = 7,
                               blockSize = 7 )
        
        # Parameters for lucas kanade optical flow
        lk_params = dict( winSize  = (15,15),
                          maxLevel = 2,
                          criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        
        # Create some random colors
        color = np.random.randint(0,255,(100,3))
        
        # Take first frame and find corners in it
        ret, old_frame = cap.read()
        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
        p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
        
        # Create a mask image for drawing purposes
        mask = np.zeros_like(old_frame)
        
        while(1):
            ret,frame = cap.read()
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
            # calculate optical flow
            p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        
            # Select good points
            good_new = p1[st==1]
            good_old = p0[st==1]
        
            # draw the tracks
            for i,(new,old) in enumerate(zip(good_new,good_old)):
                a,b = new.ravel()
                c,d = old.ravel()
                mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
                frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
            img = cv2.add(frame,mask)
        
            cv2.imshow('frame',img)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        
            # Now update the previous frame and previous points
            old_gray = frame_gray.copy()
            p0 = good_new.reshape(-1,1,2)
        
        cv2.destroyAllWindows()
        cap.release()       

    def button_9(self):
        print("not implemented")        



    def slider_1(self):
            self.framerate = self.sld1.value()
            print(self.framerate)

        
class Console_Analysis(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(Console_Analysis, self).__init__(parent)
        
        global newimg, filename, colourSpace
        
        self.image = newimg
        self.randomPoints = []
        self.numberPoints = 50
        self.activePoint = 0
        self.currentX = None
        self.currentY = None
        self.x, self.y = self.image.shape[0:2]
        self.totalPixels = self.x * self.y
        self.randomPlot = False
        self.randomPlotWithPoints = copy.deepcopy(self.image)
        
        self.randomPlot = pg.ImageView(view = pg.PlotItem())
        self.randomPlot.setImage(self.randomPlotWithPoints)
        self.randomPlot.show()
        self.randomPlot.view.setTitle(title = 'Random Point Analysis')
        
        self.displayPoints = True
        self.displayPointsEdge = False
        self.displaySinglePoint = False

       
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
        
        self.n_coverboard = 0
        self.n_notCoverboard = 0
        
        self.n_sky = 0
        self.n_canopy = 0
        

        self.percent_type1 = 0
        self.percent_type2 = 0
        
        self.numberPointsAssigned = 0
        
        ########## set up widgets ####################################
        
        self.button1 = QtWidgets.QPushButton("Generate Points")
        self.button2 = QtWidgets.QPushButton("Hide Points")
        self.button3 = QtWidgets.QPushButton("Show Edge")
        self.button4 = QtWidgets.QPushButton("Show current point")
        self.button5 = QtWidgets.QPushButton("Go forward a point")
        self.button6 = QtWidgets.QPushButton("Go back a point")
        self.button9 = QtWidgets.QPushButton("Center on current point")
        
        self.SpinBox1=QtWidgets.QSpinBox()
        self.SpinBox1.setRange(0,self.totalPixels)
        self.SpinBox1.setValue(self.numberPoints)
                
        self.number_points = QtWidgets.QLabel()
        self.number_points.setText("Number of Points = %d" % len(self.randomPoints)) 
        
        self.number_pixels = QtWidgets.QLabel()
        self.number_pixels.setText("Total pixels = %d" % self.totalPixels) 
        
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
        
        self.pixelCount1 = QtWidgets.QLabel()
        self.pixelCount2 = QtWidgets.QLabel()
       
        
        self.pixelCount1.setText("coverboard pixels = %s" % self.n_coverboard)
        self.pixelCount2.setText("not coverboard pixels = %s" % self.n_notCoverboard)

        self.percent1_text = QtWidgets.QLabel()
        self.percent1_text.setText("percent = %s" % self.percent_type1)
        self.percent2_text = QtWidgets.QLabel()
        self.percent2_text.setText("percent = %s" % self.percent_type2)

        self.filename_text = QtWidgets.QLabel()
        self.filename_text.setText("file: %s" % filename)
        
        self.numberAssigned_text = QtWidgets.QLabel()
        self.numberAssigned_text.setText("number of points assigned = %s" % self.numberPointsAssigned)
        
                    
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.button1, 0, 0)
        layout.addWidget(self.button2, 0, 1)
        layout.addWidget(self.button3, 0, 2)
        
        layout.addWidget(self.number_points, 1, 0)
        layout.addWidget(self.SpinBox1, 1, 1)
        layout.addWidget(self.number_pixels, 1, 2)
        
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
        
        layout.addWidget(self.pixelCount1, 7,1)
        layout.addWidget(self.pixelCount2, 7,2) 

        layout.addWidget(self.percent1_text, 8,1)
        layout.addWidget(self.percent2_text, 8,2)
        layout.addWidget(self.numberAssigned_text, 8,3)
        
        layout.addWidget(self.filename_text, 9,0,4,4)  

        self.setLayout(layout)

        self.connect(self.button1,SIGNAL("clicked()"),self.button_1)                
        self.connect(self.button2,SIGNAL("clicked()"),self.button_2)
        self.connect(self.button3,SIGNAL("clicked()"),self.button_3)
        self.connect(self.button4,SIGNAL("clicked()"),self.button_4)
        self.connect(self.button5,SIGNAL("clicked()"),self.button_5)
        self.connect(self.button6,SIGNAL("clicked()"),self.button_6)
        
        self.connect(self.button7,SIGNAL("clicked()"),self.button_7)       
        self.connect(self.button8,SIGNAL("clicked()"),self.button_8)    
        
        self.connect(self.button7,SIGNAL("clicked()"),self.stats)       
        self.connect(self.button8,SIGNAL("clicked()"),self.stats)
        
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
        
        self.assignedPixelTypes = []
        for i in range (self.numberPoints):
            self.assignedPixelTypes.append('None')
        
        self.analysis_text.setText("Current pixel = %s" % self.assignedPixelTypes[self.activePoint])

        self.randomPlot.setImage(self.randomPlotWithPoints)
        print(self.randomPlot.axes)
        self.button3.setText("Show Edge")
        self.displayPointsEdge = False
        
        if self.current_selection_flag == 'coverboard':
            self.pixelCount1.setText("coverboard pixels = %s" % 0)
            self.pixelCount2.setText("not coverboard pixels = %s" % 0)
                    
        elif self.current_selection_flag == 'sky-canopy':
            self.pixelCount1.setText("sky pixels = %s" % 0)
            self.pixelCount2.setText("canopy pixels = %s" % 0) 
        
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
        if self.displaySinglePoint == False:
            
            self.randomPlotCurrentPointWithEdge = copy.deepcopy(self.image) 
            self.randomPlotCurrentPointWithEdge = self.addEdge(self.randomPlotCurrentPointWithEdge, self.currentX, self.currentY, self.randomPoints, size = self.edgeSize)

            self.randomPlotCurrentPointNoEdge = copy.deepcopy(self.image) 
            self.randomPlotCurrentPointNoEdge[self.currentX, self.currentY] = 0

            if self.displayPointsEdge == True:
                self.randomPlot.setImage(self.randomPlotCurrentPointWithEdge, autoRange = False)
            else:
                self.randomPlot.setImage(self.randomPlotCurrentPointNoEdge, autoRange = False)

            self.button4.setText('Hide current point')
            self.displaySinglePoint = True
            self.displayPoints = False
            self.button2.setText("Show Points")
        
        else:            
            self.randomPlot.setImage(self.image, autoRange = False)
            self.button4.setText('Show current point')
            self.displaySinglePoint = False
            self.displayPoints = False
            self.button2.setText("Show Points")
            

    def button_5(self):
        if self.activePoint +1 <= self.numberPoints:
            self.activePoint += 1
            self.active_point.setText("Current Point = %d" % self.activePoint) 
            self.analysis_text.setText("Current pixel = %s" % self.assignedPixelTypes[self.activePoint])
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
            self.analysis_text.setText("Current pixel = %s" % self.assignedPixelTypes[self.activePoint])
            self.currentX, self.currentY = self.randomPoints[self.activePoint] 
            self.active_x.setText("X = %d" % self.currentX)
            self.active_y.setText("Y = %d" % self.currentY)
            self.SpinBox2.setValue(self.activePoint)
            self.randomPlotCurrentPointWithEdge = copy.deepcopy(self.image) 
            self.randomPlotCurrentPointWithEdge = self.addEdge(self.randomPlotCurrentPointWithEdge, self.currentX, self.currentY, self.randomPoints, size = self.edgeSize)
            self.randomPlot.setImage(self.randomPlotCurrentPointWithEdge, autoRange = False)      


    def button_7(self):
        if self.randomPoints != []:
            self.currentPixelType = self.current_selection_types[0]
            self.analysis_text.setText("Current pixel = %s" % self.currentPixelType)
            self.assignedPixelTypes[self.activePoint] = self.currentPixelType
            n1 = 0
            n2 = 0
            for each in self.assignedPixelTypes:
                if each == self.current_selection_types[0]:
                    n1+=1
                elif each == self.current_selection_types[1]:
                    n2+=1
            if self.current_selection_flag == 'coverboard':
                self.n_coverboard = n1
                self.pixelCount1.setText("coverboard pixels = %s" % self.n_coverboard)
                self.n_notCoverboard = n2
                self.pixelCount2.setText("not coverboard pixels = %s" % self.n_notCoverboard)
                
            
            elif self.current_selection_flag == 'sky-canopy':
                self.n_sky = n1
                self.current_selection_types = self.skyCanopy_selection
                self.pixelCount1.setText("sky pixels = %s" % self.n_sky)
                self.n_canopy = n2
                self.current_selection_types = self.skyCanopy_selection
                self.pixelCount2.setText("canopy pixels = %s" % self.n_canopy)            
            
		

    def button_8(self):
        if self.randomPoints != []:
            self.currentPixelType = self.current_selection_types[1]
            self.analysis_text.setText("Current pixel = %s" % self.currentPixelType)
            self.assignedPixelTypes[self.activePoint] = self.currentPixelType
            n1 = 0
            n2 = 0
            for each in self.assignedPixelTypes:
                if each == self.current_selection_types[1]:
                    n1+=1
                elif each == self.current_selection_types[0]:
                    n2+=1
    
            if self.current_selection_flag == 'coverboard':
                self.n_notCoverboard = n1
                self.pixelCount2.setText("not coverboard pixels = %s" % self.n_notCoverboard)
                self.n_coverboard = n2
                self.pixelCount1.setText("coverboard pixels = %s" % self.n_coverboard)
            
            elif self.current_selection_flag == 'sky-canopy':
                self.n_canopy = n1
                self.current_selection_types = self.skyCanopy_selection
                self.pixelCount2.setText("canopy pixels = %s" % self.n_canopy)
                self.n_sky = n2
                self.current_selection_types = self.skyCanopy_selection
                self.pixelCount1.setText("sky pixels = %s" % self.n_sky)


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
            self.pixelCount1.setText("coverboard pixels = %s" % self.n_coverboard)
            self.pixelCount2.setText("not coverboard pixels = %s" % self.n_notCoverboard)
        
        elif self.current_selection_flag == 'sky-canopy':
            self.current_selection_types = self.skyCanopy_selection
            self.pixelCount1.setText("sky pixels = %s" % self.n_sky)
            self.pixelCount2.setText("canopy pixels = %s" % self.n_canopy)
        
        self.button7.setText(self.current_selection_types[0])
        self.button8.setText(self.current_selection_types[1])
        
    def stats(self):
        n1 = 0
        n2 = 0
        for each in self.assignedPixelTypes:
            if each == self.current_selection_types[0]:
                n1+=1
            elif each == self.current_selection_types[1]:
                n2+=1      
                
        
        self.percent_type1 = n1/self.numberPoints *100
        self.percent_type2 = n2/self.numberPoints *100
        
        self.percent1_text.setText("percent = %s" % self.percent_type1)
        self.percent2_text.setText("percent = %s" % self.percent_type2)
        
        self.numberPointsAssigned = n1+n2
        self.numberAssigned_text.setText("number of points assigned = %s" % self.numberPointsAssigned)
        
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
        
        global filename, sky_array, canopy_array, sky_mean, sky_n, sky_sd, canopy_mean, canopy_n, canopy_sd

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

   
        self.sld1 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld1.setRange(0,255)
        self.sld1.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld1.setValue(self.intensity_min)
        self.sld1.setGeometry(30, 40, 100, 30)

        self.sld2 = QtWidgets.QSlider(QtCore.Qt.Vertical)
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
        
        self.filename_text = QtWidgets.QLabel()
        self.filename_text.setText("current file: %s" %filename)


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
        
        layout.addWidget(self.filename_text, 4,0,4,4) 


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

        self.sld1 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld1.setRange(0,255)
        self.sld1.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld1.setValue(self.red_min)
        self.sld1.setGeometry(30, 40, 100, 30)

        self.sld2 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld2.setRange(0,255)
        self.sld2.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sld2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld2.setValue(self.red_max)
        self.sld2.setGeometry(30, 40, 100, 30)

        self.sld3 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld3.setRange(0,255)
        self.sld3.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld3.setValue(self.green_min)
        self.sld3.setGeometry(30, 40, 100, 30)

        self.sld4 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld4.setRange(0,255)
        self.sld4.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sld4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld4.setValue(self.green_max)
        self.sld4.setGeometry(30, 40, 100, 30)

        self.sld5 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld5.setRange(0,255)
        self.sld5.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld5.setValue(self.blue_min)
        self.sld5.setGeometry(30, 40, 100, 30)

        self.sld6 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld6.setRange(0,255)
        self.sld6.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sld6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld6.setValue(self.blue_max)
        self.sld6.setGeometry(30, 40, 100, 30)

        self.sld7 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld7.setRange(0,255)
        self.sld7.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld7.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld7.setValue(self.green_blue_ratio_min)
        self.sld7.setGeometry(30, 40, 100, 30)

        self.sld8 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld8.setRange(0,255)
        self.sld8.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sld8.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld8.setValue(self.green_blue_ratio_max)
        self.sld8.setGeometry(30, 40, 100, 30)

        self.sld9 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld9.setRange(0,255)
        self.sld9.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld9.setValue(self.red_green_ratio_min)
        self.sld9.setGeometry(30, 40, 100, 30)

        self.sld10 = QtWidgets.QSlider(QtCore.Qt.Vertical)
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
        
        self.filename_text = QtWidgets.QLabel()
        self.filename_text.setText("file: %s" %filename)

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
        
        layout.addWidget(self.filename_text, 4,0,5,5)

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

class Console_Coverboard_2(QtWidgets.QDialog):
    
    def __init__(self, parent = None):
        super(Console_Coverboard_2, self).__init__(parent)
        
        global roi_mean_hue, roi_mean_sat, roi_mean_val,\
            roi_min_hue, roi_min_sat, roi_min_val, roi_max_hue,\
            roi_max_sat, roi_max_val, filename, roi_mean_red, roi_mean_green,\
            roi_mean_blue, roi_mean_intensity, roi_min_intensity, roi_max_intensity,\
            roi_min_red, roi_max_red, roi_min_green, roi_max_green, roi_min_blue,\
            roi_max_blue, board_min_red, board_max_red, board_mean_red, board_min_green,\
            board_max_green, board_mean_green, board_min_blue, board_max_blue, board_mean_blue,\
            board_min_intensity, board_max_intensity, board_mean_intensity, board_mean_hue,\
            board_mean_sat, board_mean_val, board_min_hue, board_min_sat, board_min_val,\
            board_max_hue, board_max_sat, board_max_val 


        ### Variables ####
        #filter variables
        
        self.red_min = 120
        self.red_max = 210
        self.green_min = 53
        self.green_max = 68
        self.blue_min = 12
        self.blue_max = 42 

        self.hue_min = 6
        self.sat_min = 165
        self.val_min = 121
        self.hue_max = 12
        self.sat_max = 240
        self.val_max = 210

        self.sample_min_red = 0
        self.sample_max_red = 0
        self.sample_mean_red = 0

        self.sample_min_green = 0
        self.sample_max_green = 0
        self.sample_mean_green = 0

        self.sample_min_blue = 0
        self.sample_max_blue = 0
        self.sample_mean_blue = 0

        self.sample_min_hue = 0
        self.sample_max_hue = 0
        self.sample_mean_hue = 0

        self.sample_min_sat = 0
        self.sample_max_sat = 0
        self.sample_mean_sat = 0

        self.sample_min_val = 0
        self.sample_max_val = 0
        self.sample_mean_val = 0

        self.sample_min_intensity = 0
        self.sample_max_intensity = 0
        self.sample_mean_intensity = 0

        board_min_red = self.red_min
        board_min_green = self.green_min
        board_min_blue = self.blue_min
        
        board_max_red = self.red_max
        board_max_green = self.green_max
        board_max_blue = self.blue_max
        
        board_mean_red = (board_min_red+board_max_red)/2
        board_mean_green = (board_min_green+board_max_green)/2
        board_mean_blue = (board_min_blue+board_max_blue)/2

        board_min_hue = self.hue_min
        board_min_sat = self.sat_min
        board_min_val = self.val_min
        
        board_max_hue = self.hue_max
        board_max_sat = self.sat_max
        board_max_val = self.val_max
        
        board_mean_hue = (board_min_hue+board_max_hue)/2
        board_mean_sat = (board_min_sat+board_max_sat)/2
        board_mean_val = (board_min_val+board_max_val)/2

        board_min_intensity = (board_min_red+board_min_green+board_min_blue)/3
        board_max_intensity = (board_max_red+board_max_green+board_max_blue)/3
        board_mean_intensity = (board_mean_red+board_mean_green+board_mean_blue)/3
        
        self.rgbValues = []
        self.hsvValues = []
   
        self.pathname = 'None'

        #### Widgets #####
        self.buttonRun = QtWidgets.QPushButton("Run")
        self.onFlag = False      
        self.buttonSetAsBoard = QtWidgets.QPushButton("Sample board values")  
        self.buttonSetSliders = QtWidgets.QPushButton("Set board values")  
        self.buttonReset = QtWidgets.QPushButton("Clear board values")
        self.buttonPicker = QtWidgets.QPushButton("Set from colour picker")
        self.buttonBatchPath = QtWidgets.QPushButton("Get batch path")
        self.buttonBatch = QtWidgets.QPushButton("Batch run")
        
        
        self.stats_textRed = QtWidgets.QLabel()
        self.stats_textRed.setText("Red: Min = %d, Max = %d, Mean = %d" % (board_min_red, board_max_red, board_mean_red))
  
        self.stats_textGreen = QtWidgets.QLabel()
        self.stats_textGreen.setText("Green: Min = %d, Max = %d, Mean = %d" % (board_min_green, board_max_green, board_mean_green))

        self.stats_textBlue = QtWidgets.QLabel()
        self.stats_textBlue.setText("Blue: Min = %d, Max = %d, Mean = %d" % (board_min_blue, board_max_blue, board_mean_blue))

        self.stats_textHue = QtWidgets.QLabel()
        self.stats_textHue.setText("Hue: Min = %d, Max = %d, Mean = %d" % (board_min_hue,board_max_hue, board_mean_hue))
  
        self.stats_textSat = QtWidgets.QLabel()
        self.stats_textSat.setText("Saturation: Min = %d, Max = %d, Mean = %d" % (board_min_sat, board_max_sat, board_mean_sat))

        self.stats_textVal = QtWidgets.QLabel()
        self.stats_textVal.setText("Value: Min = %d, Max = %d, Mean = %d" % (board_min_val, board_max_val, board_mean_val))

        self.stats_textIntensity = QtWidgets.QLabel()
        self.stats_textIntensity.setText("Intensity: Min = %d, Max = %d, Mean = %d" % (board_min_intensity, board_max_intensity, board_mean_intensity))

        self.label1 = QtWidgets.QLabel()
        self.label1.setText("---- Coverboard values set by user ----")
        
        self.filename_text = QtWidgets.QLabel()
        self.filename_text.setText("file: %s" %filename)
        
        self.batchpath_text = QtWidgets.QLabel()
        self.batchpath_text.setText("Batch folder = : %s" %self.pathname)       

        self.label_RMin = QtWidgets.QLabel()
        self.label_BMin = QtWidgets.QLabel()
        self.label_GMin = QtWidgets.QLabel()
        self.label_RMax = QtWidgets.QLabel()
        self.label_BMax = QtWidgets.QLabel()
        self.label_GMax = QtWidgets.QLabel()

        self.label_HMin = QtWidgets.QLabel()
        self.label_SMin = QtWidgets.QLabel()
        self.label_VMin = QtWidgets.QLabel()
        self.label_HMax = QtWidgets.QLabel()
        self.label_SMax = QtWidgets.QLabel()
        self.label_VMax = QtWidgets.QLabel()

        self.label_blank = QtWidgets.QLabel()
        self.label_blank.setText("      ")


        self.label_RMin.setText("Red Min")
        self.label_BMin.setText("Blue Min")
        self.label_GMin.setText("Green Min")
        self.label_RMax.setText("Red Max")
        self.label_BMax.setText("Blue Max")
        self.label_GMax.setText("Green Max")
     
        self.label_RMin.setStyleSheet('color: red')
        self.label_RMax.setStyleSheet('color: red')      
        self.label_GMin.setStyleSheet('color: green')
        self.label_GMax.setStyleSheet('color: green')      
        self.label_BMin.setStyleSheet('color: blue')
        self.label_BMax.setStyleSheet('color: blue')
        
        self.label_HMin.setText("Hue Min")
        self.label_SMin.setText("Sat Min")
        self.label_VMin.setText("Val Min")
        self.label_HMax.setText("Hue Max")
        self.label_SMax.setText("Sat Max")
        self.label_VMax.setText("Val Max")


        self.SpinBox1=QtWidgets.QDoubleSpinBox()
        self.SpinBox1.setRange(0,self.red_max)
        self.SpinBox1.setValue(self.red_min)
        self.SpinBox1.setStyleSheet('color: red')

        self.SpinBox2=QtWidgets.QDoubleSpinBox()
        self.SpinBox2.setRange(self.red_min,255)
        self.SpinBox2.setValue(self.red_max)
        self.SpinBox2.setStyleSheet('color: red')

        self.SpinBox3=QtWidgets.QDoubleSpinBox()
        self.SpinBox3.setRange(0,self.green_max)
        self.SpinBox3.setValue(self.green_min)
        self.SpinBox3.setStyleSheet('color: green')

        self.SpinBox4=QtWidgets.QDoubleSpinBox()
        self.SpinBox4.setRange(self.green_min,255)
        self.SpinBox4.setValue(self.green_max)
        self.SpinBox4.setStyleSheet('color: green')

        self.SpinBox5=QtWidgets.QDoubleSpinBox()
        self.SpinBox5.setRange(0,self.blue_max)
        self.SpinBox5.setValue(self.blue_min)
        self.SpinBox5.setStyleSheet('color: blue')

        self.SpinBox6=QtWidgets.QDoubleSpinBox()
        self.SpinBox6.setRange(self.blue_min,255)
        self.SpinBox6.setValue(self.blue_max)
        self.SpinBox6.setStyleSheet('color: blue')

        self.SpinBox7=QtWidgets.QDoubleSpinBox()
        self.SpinBox7.setRange(0,self.hue_max)
        self.SpinBox7.setValue(self.hue_min)

        self.SpinBox8=QtWidgets.QDoubleSpinBox()
        self.SpinBox8.setRange(self.hue_min,255)
        self.SpinBox8.setValue(self.hue_max)

        self.SpinBox9=QtWidgets.QDoubleSpinBox()
        self.SpinBox9.setRange(0,self.sat_max)
        self.SpinBox9.setValue(self.sat_min)

        self.SpinBox10=QtWidgets.QDoubleSpinBox()
        self.SpinBox10.setRange(self.sat_min,255)
        self.SpinBox10.setValue(self.sat_max)
        
        self.SpinBox11=QtWidgets.QDoubleSpinBox()
        self.SpinBox11.setRange(0,self.val_max)
        self.SpinBox11.setValue(self.val_min)

        self.SpinBox12=QtWidgets.QDoubleSpinBox()
        self.SpinBox12.setRange(self.val_min,255)
        self.SpinBox12.setValue(self.val_max)

        self.sld1 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld1.setRange(0,255)
        self.sld1.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld1.setValue(self.red_min)
        self.sld1.setGeometry(30, 40, 100, 30)

        self.sld2 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld2.setRange(0,255)
        self.sld2.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sld2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld2.setValue(self.red_max)
        self.sld2.setGeometry(30, 40, 100, 30)

        self.sld3 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld3.setRange(0,255)
        self.sld3.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld3.setValue(self.green_min)
        self.sld3.setGeometry(30, 40, 100, 30)

        self.sld4 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld4.setRange(0,255)
        self.sld4.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sld4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld4.setValue(self.green_max)
        self.sld4.setGeometry(30, 40, 100, 30)

        self.sld5 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld5.setRange(0,255)
        self.sld5.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld5.setValue(self.blue_min)
        self.sld5.setGeometry(30, 40, 100, 30)

        self.sld6 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld6.setRange(0,255)
        self.sld6.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sld6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld6.setValue(self.blue_max)
        self.sld6.setGeometry(30, 40, 100, 30)

        self.sld7 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld7.setRange(0,255)
        self.sld7.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld7.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld7.setValue(self.hue_min)
        self.sld7.setGeometry(30, 40, 100, 30)

        self.sld8 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld8.setRange(0,255)
        self.sld8.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sld8.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld8.setValue(self.hue_max)
        self.sld8.setGeometry(30, 40, 100, 30)

        self.sld9 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld9.setRange(0,255)
        self.sld9.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld9.setValue(self.sat_min)
        self.sld9.setGeometry(30, 40, 100, 30)

        self.sld10 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld10.setRange(0,255)
        self.sld10.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sld10.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld10.setValue(self.sat_max)
        self.sld10.setGeometry(30, 40, 100, 30)

        self.sld11 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld11.setRange(0,255)
        self.sld11.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld11.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld11.setValue(self.val_min)
        self.sld11.setGeometry(30, 40, 100, 30)

        self.sld12 = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.sld12.setRange(0,255)
        self.sld12.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sld12.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld12.setValue(self.val_max)
        self.sld12.setGeometry(30, 40, 100, 30)

        layout = QtWidgets.QGridLayout()

        layout.addWidget(self.buttonRun, 0, 8)
        layout.addWidget(self.buttonSetAsBoard, 1, 8)
        layout.addWidget(self.buttonSetSliders, 2, 8)        
        layout.addWidget(self.buttonPicker, 4, 8)  
        layout.addWidget(self.buttonReset, 5, 8)
        layout.addWidget(self.buttonBatchPath, 6, 8) 
        layout.addWidget(self.buttonBatch, 7, 8)
        
        layout.addWidget(self.label1, 8,8)
        
        layout.addWidget(self.stats_textRed, 9,8)
        layout.addWidget(self.stats_textGreen, 10,8)
        layout.addWidget(self.stats_textBlue, 11,8)

        layout.addWidget(self.stats_textHue, 16,8)
        layout.addWidget(self.stats_textSat, 17,8)
        layout.addWidget(self.stats_textVal, 18,8)        
        
        layout.addWidget(self.stats_textIntensity, 20,8)
   
        layout.addWidget(self.label_blank, 3,8)      
        layout.addWidget(self.label_blank, 12,8)     
        layout.addWidget(self.label_blank, 13,8)
        layout.addWidget(self.label_blank, 14,8)
        layout.addWidget(self.label_blank, 15,8)
        layout.addWidget(self.label_blank, 19,8)
        layout.addWidget(self.label_blank, 21,8)
        layout.addWidget(self.label_blank, 22,8)

        layout.addWidget(self.label_RMin, 8,0)
        layout.addWidget(self.label_RMax, 8,1)
                
        layout.addWidget(self.SpinBox1, 9, 0)
        layout.addWidget(self.SpinBox2, 9, 1)
        
        layout.addWidget(self.label_GMin, 8,2)
        layout.addWidget(self.label_GMax, 8,3)

        layout.addWidget(self.SpinBox3, 9, 2)
        layout.addWidget(self.SpinBox4, 9, 3)
        
        layout.addWidget(self.label_BMin, 8,4)
        layout.addWidget(self.label_BMax, 8,5)        

        layout.addWidget(self.SpinBox5, 9, 4)
        layout.addWidget(self.SpinBox6, 9, 5)

        layout.addWidget(self.label_HMin, 19,0)
        layout.addWidget(self.label_HMax, 19,1)
        
        layout.addWidget(self.SpinBox7, 20, 0)
        layout.addWidget(self.SpinBox8, 20, 1)
        
        layout.addWidget(self.label_SMin, 19,2)
        layout.addWidget(self.label_SMax, 19,3)
        
        layout.addWidget(self.SpinBox9, 20, 2)
        layout.addWidget(self.SpinBox10, 20, 3)
        
        layout.addWidget(self.label_VMin, 19,4)
        layout.addWidget(self.label_VMax, 19,5)
        
        layout.addWidget(self.SpinBox11, 20, 4)
        layout.addWidget(self.SpinBox12, 20, 5)
        
        layout.addWidget(self.sld1, 0,0,8,0)
        layout.addWidget(self.sld2, 0,1,8,1)
        
        layout.addWidget(self.sld3, 0,2,8,2)
        layout.addWidget(self.sld4, 0,3,8,3)  
        
        layout.addWidget(self.sld5, 0,4,8,4)
        layout.addWidget(self.sld6, 0,5,8,5)
        
 
        layout.addWidget(self.sld7, 10,0,9,0)
        layout.addWidget(self.sld8, 10,1,9,1)
        
        layout.addWidget(self.sld9, 10,2,9,2)
        layout.addWidget(self.sld10, 10,3,9,3)  
        
        layout.addWidget(self.sld11, 10,4,9,4)
        layout.addWidget(self.sld12, 10,5,9,5)
  
        layout.addWidget(self.filename_text, 21,0,21,-1)
        layout.addWidget(self.batchpath_text, 22, 0, 22, -1)

        self.setLayout(layout)

        self.connect(self.buttonRun,SIGNAL("clicked()"),self.button_run)
        self.connect(self.buttonSetAsBoard,SIGNAL("clicked()"),self.button_setAsBoard)
        self.connect(self.buttonSetSliders,SIGNAL("clicked()"),self.setSliders)
        self.connect(self.buttonReset,SIGNAL("clicked()"),self.resetSampling)
        self.connect(self.buttonBatchPath,SIGNAL("clicked()"),self.getPath) 
        self.connect(self.buttonPicker,SIGNAL("clicked()"),self.setFromPicker)   
         

        self.connect(self.sld1,SIGNAL("valueChanged(int)"), self.slider_1)
        self.connect(self.sld1,SIGNAL("valueChanged(int)"),self.SpinBox1.setValue)
        self.connect(self.sld1,SIGNAL("valueChanged(int)"),self.update_HSV)   
        self.connect(self.sld2,SIGNAL("valueChanged(int)"), self.slider_2)
        self.connect(self.sld2,SIGNAL("valueChanged(int)"),self.SpinBox2.setValue)
        self.connect(self.sld2,SIGNAL("valueChanged(int)"),self.update_HSV)
        self.connect(self.sld3,SIGNAL("valueChanged(int)"), self.slider_3)
        self.connect(self.sld3,SIGNAL("valueChanged(int)"),self.SpinBox3.setValue)
        self.connect(self.sld3,SIGNAL("valueChanged(int)"),self.update_HSV)
        self.connect(self.sld4,SIGNAL("valueChanged(int)"), self.slider_4)
        self.connect(self.sld4,SIGNAL("valueChanged(int)"),self.SpinBox4.setValue)
        self.connect(self.sld4,SIGNAL("valueChanged(int)"),self.update_HSV)
        self.connect(self.sld5,SIGNAL("valueChanged(int)"), self.slider_5)
        self.connect(self.sld5,SIGNAL("valueChanged(int)"),self.SpinBox5.setValue)
        self.connect(self.sld5,SIGNAL("valueChanged(int)"),self.update_HSV)
        self.connect(self.sld6,SIGNAL("valueChanged(int)"), self.slider_6)
        self.connect(self.sld6,SIGNAL("valueChanged(int)"),self.SpinBox6.setValue)
        self.connect(self.sld6,SIGNAL("valueChanged(int)"),self.update_HSV)

        self.connect(self.sld7,SIGNAL("valueChanged(int)"), self.slider_7)
        self.connect(self.sld7,SIGNAL("valueChanged(int)"),self.SpinBox7.setValue)
        #self.connect(self.sld7,SIGNAL("valueChanged(int)"),self.update_RGB)        
        self.connect(self.sld8,SIGNAL("valueChanged(int)"), self.slider_8)
        self.connect(self.sld8,SIGNAL("valueChanged(int)"),self.SpinBox8.setValue)
        #self.connect(self.sld8,SIGNAL("valueChanged(int)"),self.update_RGB)         
        self.connect(self.sld9,SIGNAL("valueChanged(int)"), self.slider_9)
        self.connect(self.sld9,SIGNAL("valueChanged(int)"),self.SpinBox9.setValue)
        #self.connect(self.sld9,SIGNAL("valueChanged(int)"),self.update_RGB)        
        self.connect(self.sld10,SIGNAL("valueChanged(int)"), self.slider_10)
        self.connect(self.sld10,SIGNAL("valueChanged(int)"),self.SpinBox10.setValue)
        #self.connect(self.sld10,SIGNAL("valueChanged(int)"),self.update_RGB)          
        self.connect(self.sld11,SIGNAL("valueChanged(int)"), self.slider_11)
        self.connect(self.sld11,SIGNAL("valueChanged(int)"),self.SpinBox11.setValue)
        #self.connect(self.sld11,SIGNAL("valueChanged(int)"),self.update_RGB)         
        self.connect(self.sld12,SIGNAL("valueChanged(int)"), self.slider_12)
        self.connect(self.sld12,SIGNAL("valueChanged(int)"),self.SpinBox12.setValue)
        #self.connect(self.sld12,SIGNAL("valueChanged(int)"),self.update_RGB) 


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
        if self.sld7.value() < self.hue_max:
            self.hue_min = self.sld7.value()
            self.SpinBox8.setRange(self.hue_min,255)
            self.setGlobalHSV()
        else:
            self.sld7.setValue(self.hue_max)
            self.SpinBox7.setValue(self.hue_max)
            self.setGlobalHSV()

    def slider_8(self):
        if self.sld8.value() > self.hue_min:
            self.hue_max = self.sld8.value()
            self.SpinBox7.setRange(0,self.hue_max)
            self.setGlobalHSV()
        else:
            self.sld8.setValue(self.hue_min)
            self.SpinBox8.setValue(self.hue_min)
            self.setGlobalHSV()

    def slider_9(self):
        if self.sld9.value() < self.sat_max:
            self.sat_min = self.sld9.value()
            self.SpinBox10.setRange(self.sat_min,255)
            self.setGlobalHSV()
        else:
            self.sld9.setValue(self.sat_max)
            self.SpinBox9.setValue(self.sat_max)
            self.setGlobalHSV()

    def slider_10(self):
        if self.sld10.value() > self.sat_min:
            self.sat_max = self.sld10.value()
            self.SpinBox9.setRange(0,self.sat_max)
            self.setGlobalHSV()
        else:
            self.sld10.setValue(self.sat_min)
            self.SpinBox10.setValue(self.sat_min)
            self.setGlobalHSV()

    def slider_11(self):
        if self.sld11.value() < self.val_max:
            self.val_min = self.sld11.value()
            self.SpinBox10.setRange(self.val_min,255)
            self.setGlobalHSV()
        else:
            self.sld11.setValue(self.val_max)
            self.SpinBox11.setValue(self.val_max)
            self.setGlobalHSV()

    def slider_12(self):
        if self.sld12.value() > self.val_min:
            self.val_max = self.sld12.value()
            self.SpinBox11.setRange(0,self.val_max)
            self.setGlobalHSV()
        else:
            self.sld12.setValue(self.val_min)
            self.SpinBox12.setValue(self.val_min)
            self.setGlobalHSV()

    def update_HSV(self):
        global roi_mean_hue, roi_mean_sat, roi_mean_val, roi_min_hue, roi_min_sat, roi_min_val, roi_max_hue, roi_max_sat, roi_max_val, filename, roi_mean_red, roi_mean_green, roi_mean_blue, roi_mean_intensity, roi_min_intensity, roi_max_intensity, roi_min_red, roi_max_red, roi_min_green, roi_max_green, roi_min_blue, roi_max_blue, board_min_red, board_max_red, board_mean_red, board_min_green, board_max_green, board_mean_green, board_min_blue, board_max_blue, board_mean_blue, board_min_intensity, board_max_intensity, board_mean_intensity, board_mean_hue, board_mean_sat, board_mean_val, board_min_hue, board_min_sat, board_min_val, board_max_hue, board_max_sat, board_max_val 

        min_hsv = RGB_2_HSV((self.red_min,self.green_min,self.blue_min))
        max_hsv = RGB_2_HSV((self.red_max,self.green_max,self.blue_max))
        self.sld7.setValue(min_hsv[0])
        self.sld8.setValue(max_hsv[0])       
        self.sld9.setValue(min_hsv[1])   
        self.sld10.setValue(max_hsv[1])
        self.sld11.setValue(min_hsv[2])
        self.sld12.setValue(max_hsv[2])  
 
        self.SpinBox7.setValue(min_hsv[0])
        self.SpinBox8.setRange(max_hsv[0])
        self.SpinBox9.setValue(min_hsv[1])
        self.SpinBox10.setRange(max_hsv[1])
        self.SpinBox11.setValue(min_hsv[2])
        self.SpinBox12.setRange(max_hsv[2])
        
        board_min_hue = min_hsv[0]
        board_max_hue = max_hsv[0]
        board_min_sat = min_hsv[1]
        board_max_sat = max_hsv[1]
        board_min_val = min_hsv[2]
        board_max_val = max_hsv[2]      
    
    def update_RGB(self):
        global roi_mean_hue, roi_mean_sat, roi_mean_val, roi_min_hue, roi_min_sat, roi_min_val, roi_max_hue, roi_max_sat, roi_max_val, filename, roi_mean_red, roi_mean_green, roi_mean_blue, roi_mean_intensity, roi_min_intensity, roi_max_intensity, roi_min_red, roi_max_red, roi_min_green, roi_max_green, roi_min_blue, roi_max_blue, board_min_red, board_max_red, board_mean_red, board_min_green, board_max_green, board_mean_green, board_min_blue, board_max_blue, board_mean_blue, board_min_intensity, board_max_intensity, board_mean_intensity, board_mean_hue, board_mean_sat, board_mean_val, board_min_hue, board_min_sat, board_min_val, board_max_hue, board_max_sat, board_max_val 

        min_rgb = HSV_2_RGB((self.hue_min,self.sat_min,self.val_min))
        max_rgb = HSV_2_RGB((self.hue_max,self.sat_max,self.val_max))
        self.sld1.setValue(min_rgb[0])
        self.sld2.setValue(max_rgb[0])       
        self.sld3.setValue(min_rgb[1])   
        self.sld4.setValue(max_rgb[1])
        self.sld5.setValue(min_rgb[2])
        self.sld6.setValue(max_rgb[2])  
 
        self.SpinBox1.setValue(min_rgb[0])
        self.SpinBox2.setRange(max_rgb[0])
        self.SpinBox3.setValue(min_rgb[1])
        self.SpinBox4.setRange(max_rgb[1])
        self.SpinBox5.setValue(min_rgb[2])
        self.SpinBox6.setRange(max_rgb[2])

        board_min_red = min_rgb[0]
        board_max_red = max_rgb[0]
        board_min_green = min_rgb[1]
        board_max_green = max_rgb[1]
        board_min_blue = min_rgb[2]
        board_max_blue = max_rgb[2]

        board_min_hue = self.hue_min
        board_max_hue = self.hue_max
        board_min_sat = self.sat_min
        board_max_sat = self.sat_max
        board_min_val = self.val_min
        board_max_val = self.val_max


    def button_run(self):
        if self.onFlag == False:
            self.onFlag = True
            self.buttonRun.setText("Run")
        else:
            self.onFlag = False
            self.buttonRun.setText("Run")

    def button_setAsBoard(self):
        
        global roi_mean_hue, roi_mean_sat, roi_mean_val, roi_min_hue, roi_min_sat, roi_min_val, roi_max_hue, roi_max_sat, roi_max_val, filename, roi_mean_red, roi_mean_green, roi_mean_blue, roi_mean_intensity, roi_min_intensity, roi_max_intensity, roi_min_red, roi_max_red, roi_min_green, roi_max_green, roi_min_blue, roi_max_blue, board_min_red, board_max_red, board_mean_red, board_min_green, board_max_green, board_mean_green, board_min_blue, board_max_blue, board_mean_blue, board_min_intensity, board_max_intensity, board_mean_intensity, board_mean_hue, board_mean_sat, board_mean_val, board_min_hue, board_min_sat, board_min_val, board_max_hue, board_max_sat, board_max_val 

        self.rgbValues.append([roi_min_red, roi_min_green, roi_min_blue])
        self.rgbValues.append([roi_max_red, roi_max_green, roi_max_blue])
             
        self.hsvValues.append([roi_min_hue, roi_min_sat, roi_min_val])
        self.hsvValues.append([roi_max_hue, roi_max_sat, roi_max_val])
 
        
        self.sample_min_red = np.min(np.array(self.rgbValues)[:,0])
        self.sample_max_red = np.max(np.array(self.rgbValues)[:,0])
        self.sample_mean_red = np.mean(np.array(self.rgbValues)[:,0])
        
        self.sample_min_green = np.min(np.array(self.rgbValues)[:,1])
        self.sample_max_green = np.max(np.array(self.rgbValues)[:,1])
        self.sample_mean_green = np.mean(np.array(self.rgbValues)[:,1])
        
        self.sample_min_blue = np.min(np.array(self.rgbValues)[:,2])
        self.sample_max_blue = np.max(np.array(self.rgbValues)[:,2])
        self.sample_mean_blue = np.mean(np.array(self.rgbValues)[:,2])

        self.sample_min_hue = np.min(np.array(self.hsvValues)[:,0])
        self.sample_max_hue = np.max(np.array(self.hsvValues)[:,0])
        self.sample_mean_hue = np.mean(np.array(self.hsvValues)[:,0])
        
        self.sample_min_sat = np.min(np.array(self.hsvValues)[:,1])
        self.sample_max_sat = np.max(np.array(self.hsvValues)[:,1])
        self.sample_mean_sat = np.mean(np.array(self.hsvValues)[:,1])
        
        self.sample_min_val = np.min(np.array(self.hsvValues)[:,2])
        self.sample_max_val = np.max(np.array(self.hsvValues)[:,2])
        self.sample_mean_val = np.mean(np.array(self.hsvValues)[:,2])

        self.stats_textRed.setText("Red: Min = %d, Max = %d, Mean = %d" % (self.sample_min_red, self.sample_max_red, self.sample_mean_red))
        self.stats_textGreen.setText("Green: Min = %d, Max = %d, Mean = %d" % (self.sample_min_green, self.sample_max_green, self.sample_mean_green))
        self.stats_textBlue.setText("Blue: Min = %d, Max = %d, Mean = %d" % (self.sample_min_blue, self.sample_max_blue, self.sample_mean_blue))
        self.stats_textIntensity.setText("Intensity: Min = %d, Max = %d, Mean = %d" % (board_min_intensity, board_max_intensity, board_mean_intensity))
        self.stats_textHue.setText("Hue: Min = %d, Max = %d, Mean = %d" % (self.sample_min_hue, self.sample_max_hue, self.sample_mean_hue))
        self.stats_textSat.setText("Saturation: Min = %d, Max = %d, Mean = %d" % (self.sample_min_sat, self.sample_max_sat, self.sample_mean_sat))
        self.stats_textVal.setText("Value: Min = %d, Max = %d, Mean = %d" % (self.sample_min_val, self.sample_max_val, self.sample_mean_val))


        board_min_red = self.sample_min_red
        board_max_red = self.sample_max_red
        board_min_green = self.sample_min_green
        board_max_green = self.sample_max_green
        board_min_blue = self.sample_min_blue
        board_max_blue = self.sample_max_blue


        board_min_hue = self.sample_min_hue
        board_max_hue = self.sample_max_hue
        board_min_sat = self.sample_min_sat
        board_max_sat = self.sample_max_sat
        board_min_val = self.sample_min_val
        board_max_val = self.sample_max_val
        

    def resetSampling (self):
        global board_min_red, board_max_red, board_min_green, board_max_green, board_min_blue, board_max_blue, board_min_hue, board_max_hue, board_min_sat, board_max_sat, board_min_val, board_max_val 
        
        self.rgbValues = []      
        self.hsvValues = []
       
        self.sample_min_red = 0
        self.sample_max_red = 0
        self.sample_mean_red = 0

        self.sample_min_green = 0
        self.sample_max_green = 0
        self.sample_mean_green = 0

        self.sample_min_blue = 0
        self.sample_max_blue = 0
        self.sample_mean_blue = 0

        self.sample_min_hue = 0
        self.sample_max_hue = 0
        self.sample_mean_hue = 0

        self.sample_min_sat = 0
        self.sample_max_sat = 0
        self.sample_mean_sat = 0

        self.sample_min_val = 0
        self.sample_max_val = 0
        self.sample_mean_val = 0

        self.sample_min_intensity = 0
        self.sample_max_intensity = 0
        self.sample_mean_intensity = 0

        board_min_red = self.sld1.value()
        board_max_red = self.sld2.value()
        board_min_green = self.sld3.value()
        board_max_green = self.sld4.value()
        board_min_blue = self.sld5.value()
        board_max_blue = self.sld6.value()
        
        board_min_hue = self.sld7.value()
        board_max_hue = self.sld8.value()
        board_min_sat = self.sld9.value()
        board_max_sat = self.sld10.value()
        board_min_val = self.sld11.value()
        board_max_val = self.sld12.value()     
        
        board_min_intensity = 0
        board_max_intensity = 0
        board_mean_intensity = 0

        self.stats_textRed.setText("Red: Min = %d, Max = %d, Mean = %d" % (self.sample_min_red, self.sample_max_red, self.sample_mean_red))
        self.stats_textGreen.setText("Green: Min = %d, Max = %d, Mean = %d" % (self.sample_min_green, self.sample_max_green, self.sample_mean_green))
        self.stats_textBlue.setText("Blue: Min = %d, Max = %d, Mean = %d" % (self.sample_min_blue, self.sample_max_blue, self.sample_mean_blue))
        self.stats_textIntensity.setText("Intensity: Min = %d, Max = %d, Mean = %d" % (board_min_intensity, board_max_intensity, board_mean_intensity))
        self.stats_textHue.setText("Hue: Min = %d, Max = %d, Mean = %d" % (self.sample_min_hue, self.sample_max_hue, self.sample_mean_hue))
        self.stats_textSat.setText("Saturation: Min = %d, Max = %d, Mean = %d" % (self.sample_min_sat, self.sample_max_sat, self.sample_mean_sat))
        self.stats_textVal.setText("Value: Min = %d, Max = %d, Mean = %d" % (self.sample_min_val, self.sample_max_val, self.sample_mean_val))

    def setSliders(self):
        global board_min_red, board_max_red, board_min_green, board_max_green, board_min_blue, board_max_blue, board_min_hue, board_max_hue, board_min_sat, board_max_sat, board_min_val, board_max_val 
        
        self.SpinBox1.setRange(0, self.sample_max_red)
        self.sld1.setValue(self.sample_min_red)
        self.SpinBox1.setValue(self.sample_min_red)
        
        self.SpinBox2.setRange(self.sample_min_red, 255)
        self.sld2.setValue(self.sample_max_red)
        self.SpinBox2.setValue(self.sample_max_red)

        self.SpinBox3.setRange(0,self.sample_max_green)
        self.sld3.setValue(self.sample_min_green)
        self.SpinBox3.setValue(self.sample_min_green)
        
        self.SpinBox4.setRange(self.sample_min_green, 255)
        self.sld4.setValue(self.sample_max_green)
        self.SpinBox4.setValue(self.sample_max_green)

        self.SpinBox5.setRange(0,self.sample_max_blue)
        self.sld5.setValue(self.sample_min_blue)
        self.SpinBox5.setValue(self.sample_min_blue)
        
        self.SpinBox6.setRange(self.sample_min_blue, 255)
        self.sld6.setValue(self.sample_max_blue)
        self.SpinBox6.setValue(self.sample_max_blue)

        self.SpinBox7.setRange(0,self.sample_max_hue)
        self.sld7.setValue(self.sample_min_hue)
        self.SpinBox7.setValue(self.sample_min_hue)
        
        self.SpinBox8.setRange(self.sample_min_hue, 255)
        self.sld8.setValue(self.sample_max_hue)
        self.SpinBox8.setValue(self.sample_max_hue)

        self.SpinBox9.setRange(0,self.sample_max_sat)
        self.sld9.setValue(self.sample_min_sat)
        self.SpinBox9.setValue(self.sample_min_sat)
        
        self.SpinBox10.setRange(self.sample_min_sat, 255)
        self.sld10.setValue(self.sample_max_sat)
        self.SpinBox10.setValue(self.sample_max_sat)

        self.SpinBox11.setRange(0,self.sample_max_val)
        self.sld11.setValue(self.sample_min_val)
        self.SpinBox11.setValue(self.sample_min_val)
        
        self.SpinBox12.setRange(self.sample_min_val, 255)
        self.sld12.setValue(self.sample_max_val)
        self.SpinBox12.setValue(self.sample_max_val)
       
        board_min_red = self.sld1.value()
        board_max_red = self.sld2.value()
        board_min_green = self.sld3.value()
        board_max_green = self.sld4.value()
        board_min_blue = self.sld5.value()
        board_max_blue = self.sld6.value()
        
        board_min_hue = self.sld7.value()
        board_max_hue = self.sld8.value()
        board_min_sat = self.sld9.value()
        board_max_sat = self.sld10.value()
        board_min_val = self.sld11.value()
        board_max_val = self.sld12.value() 
        
        self.red_min = board_min_red
        self.red_max = board_max_red
        self.green_min = board_min_green
        self.green_max = board_max_green
        self.blue_min = board_min_blue
        self.blue_max = board_max_blue

        self.hue_min = board_min_hue
        self.sat_min = board_max_hue
        self.val_min = board_min_sat
        self.hue_max = board_max_sat
        self.sat_max = board_min_sat
        self.val_max = board_max_sat
        
        return

    def setGlobalHSV(self):   
        global board_median_hue, board_median_sat, board_median_val,\
                board_min_hue, board_min_sat, board_min_val, board_max_hue,\
                board_max_sat, board_max_val 

        board_min_red = self.sld1.value()
        board_max_red = self.sld2.value()
        board_min_green = self.sld3.value()
        board_max_green = self.sld4.value()
        board_min_blue = self.sld5.value()
        board_max_blue = self.sld6.value()
        
        board_min_hue = self.sld7.value()
        board_max_hue = self.sld8.value()
        board_min_sat = self.sld9.value()
        board_max_sat = self.sld10.value()
        board_min_val = self.sld11.value()
        board_max_val = self.sld12.value() 
        
        board_median_hue = (self.hue_max + self.hue_min)/2
        board_median_sat = (self.sat_max + self.sat_min)/2
        board_median_val = (self.val_max + self.val_min)/2

    def getPath(self):
        pathname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a folder',
                os.path.expanduser("~"), QtWidgets.QFileDialog.ShowDirsOnly)
        
        self.pathname = str(pathname)
        #print(pathname)
#        if pathname == '':
#            return False
#        else:
#            self.runBatch(pathname)
#            return
        self.batchpath_text.setText("Batch folder = : %s" %self.pathname) 
        
    def setFromPicker(self):
        
        global picker_HSV, picker_RGB

        self.board_min_hue = picker_HSV[0] - 5
        self.board_min_sat = picker_HSV[1] - 15
        self.board_min_val = picker_HSV[2] - 15

        self.board_max_hue = picker_HSV[0] + 5
        self.board_max_sat = picker_HSV[1] + 15
        self.board_max_val = picker_HSV[2] + 15

        
        self.board_min_red,self.board_min_green,self.board_min_blue  = RGB_2_HSV((self.board_min_hue,self.board_min_sat,self.board_min_val))
        self.board_max_red,self.board_max_green,self.board_max_blue  = RGB_2_HSV((self.board_max_hue,self.board_max_sat,self.board_max_val))


        self.SpinBox1.setRange(0, self.board_max_red)
        self.sld1.setValue(self.board_min_red)
        self.SpinBox1.setValue(self.board_min_red)
    
        self.SpinBox2.setRange(self.board_min_red, 255)
        self.sld2.setValue(self.board_max_red)
        self.SpinBox2.setValue(self.board_max_red)

        self.SpinBox3.setRange(0,self.board_max_green)
        self.sld3.setValue(self.board_min_green)
        self.SpinBox3.setValue(self.board_min_green)
        
        self.SpinBox4.setRange(self.board_min_green, 255)
        self.sld4.setValue(self.board_max_green)
        self.SpinBox4.setValue(self.board_max_green)

        self.SpinBox5.setRange(0,self.board_max_blue)
        self.sld5.setValue(self.board_min_blue)
        self.SpinBox5.setValue(self.board_min_blue)
        
        self.SpinBox6.setRange(self.board_min_blue, 255)
        self.sld6.setValue(self.board_max_blue)
        self.SpinBox6.setValue(self.board_max_blue)

        self.SpinBox7.setRange(0,self.board_max_hue)
        self.sld7.setValue(self.board_min_hue)
        self.SpinBox7.setValue(self.board_min_hue)
        
        self.SpinBox8.setRange(self.board_min_hue, 255)
        self.sld8.setValue(self.board_max_hue)
        self.SpinBox8.setValue(self.board_max_hue)

        self.SpinBox9.setRange(0,self.board_max_sat)
        self.sld9.setValue(self.board_min_sat)
        self.SpinBox9.setValue(self.board_min_sat)
        
        self.SpinBox10.setRange(self.board_min_sat, 255)
        self.sld10.setValue(self.board_max_sat)
        self.SpinBox10.setValue(self.board_max_sat)

        self.SpinBox11.setRange(0,self.board_max_val)
        self.sld11.setValue(self.board_min_val)
        self.SpinBox11.setValue(self.board_min_val)
        
        self.SpinBox12.setRange(self.board_min_val, 255)
        self.sld12.setValue(self.board_max_val)
        self.SpinBox12.setValue(self.board_max_val)
        
        self.setGlobalHSV()
        
        return




############ Main Viewing Window ##############################################
class Viewer(QtWidgets.QMainWindow):

    def __init__(self):
        super(Viewer, self).__init__()

        self.initUI()
        global ROI_flag, picker_RGB, picker_HSV, picker_HSL
        ROI_flag = False
#    def mousePressEvent(self, QtGui.QMouseEvent):
#        print (QMouseEvent.pos())
#
#    def mouseReleaseEvent(self, QtGui.QMouseEvent):
#        cursor =QtGui.QCursor()
#        print (cursor.pos())  

    def initUI(self):

        self.ImageView = pg.ImageView(view=pg.PlotItem())
        self.ImageView.view.setTitle('No file loaded')
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
        activateConsole.triggered.connect(self.initConsole_CoverBoard_1)
        
        activateConsole2 = QtWidgets.QAction(QtGui.QIcon('save.png'), 'ROI Console_2', self)
        activateConsole2.setShortcut('Ctrl+2')
        activateConsole2.setStatusTip('Start Console2')
        activateConsole2.triggered.connect(self.initConsole_CoverBoard_2)
        activateConsole2.triggered.connect(self.startROIExaminer)
                
        activateConsoleCanopy = QtWidgets.QAction(QtGui.QIcon('save.png'), 'Canopy Console', self)
        activateConsoleCanopy.setShortcut('Ctrl+N')
        activateConsoleCanopy.setStatusTip('Start Console')
        activateConsoleCanopy.triggered.connect(self.initConsole_Canopy)
        activateConsoleCanopy.triggered.connect(self.startROIExaminer)
        
        activateAnalysisConsole = QtWidgets.QAction(QtGui.QIcon('save.png'), 'Analysis Console', self)
        activateAnalysisConsole.setShortcut('Ctrl+A')
        activateAnalysisConsole.setStatusTip('Start Analysis')
        activateAnalysisConsole.triggered.connect(self.initConsole_Analysis)
        
        activateColourPicker = QtWidgets.QAction(QtGui.QIcon('save.png'), 'Colour Picker', self)
        activateColourPicker.setShortcut('Ctrl+0')
        activateColourPicker.setStatusTip('Launch Colour Picker')
        activateColourPicker.triggered.connect(self.colour_picker)
        
        activateCameraConsole = QtWidgets.QAction(QtGui.QIcon('save.png'), 'Camera Console', self)
        activateCameraConsole.setShortcut('Ctrl+8')
        activateCameraConsole.setStatusTip('Launch Camera Console')
        activateCameraConsole.triggered.connect(self.initCameraConsole)

        activateBotConsole = QtWidgets.QAction(QtGui.QIcon('save.png'), 'Bot Console', self)
        activateBotConsole.setShortcut('Ctrl+R')
        activateBotConsole.setStatusTip('Launch Bot Console')
        activateBotConsole.triggered.connect(self.initBotConsole)
      
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
        fileMenu3.addAction(activateConsole2)
        
        fileMenu4 = menubar.addMenu('&Canopy Detection')       
        fileMenu4.addAction(activateConsoleCanopy)
        
        fileMenu5 = menubar.addMenu('&Random Point Analysis')       
        fileMenu5.addAction(activateAnalysisConsole)    
        
        fileMenu6 = menubar.addMenu('&Colour Picker')       
        fileMenu6.addAction(activateColourPicker) 
        
        fileMenu7 = menubar.addMenu('&Camera')       
        fileMenu7.addAction(activateCameraConsole)      

        fileMenu8 = menubar.addMenu('&Bot')       
        fileMenu8.addAction(activateBotConsole)


#        fileMenu3 = menubar.addMenu('&Analysis')
#        fileMenu3.addAction(analysis1)

        #self.setGeometry(300, 300, 350, 300)

        self.setWindowTitle('ImageView')

        #self.initROI()
        self.show()

    def initBotConsole(self):
        self.BotConsole = BotConsole()
        self.BotConsole.show()       

    def initCameraConsole(self):
        self.cameraConsole = CameraConsole()
        self.cameraConsole.connect(self.cameraConsole.button5,SIGNAL("clicked()"),self.getCameraPic)
        self.cameraConsole.show()

    def getCameraPic(self):
        global newimg
        self.ImageView.setImage(newimg)

    def initConsole_CoverBoard_1(self):
        self.console = Console_Coverboard()
        #self.console.connect(self.console.button1,SIGNAL("clicked()"),self.testPrint)
        self.console.connect(self.console.button1,SIGNAL("clicked()"),self.detect_coverBoard)
        self.console.connect(self.console.button2,SIGNAL("clicked()"),self.cluster_coverBoard)
        self.console.show()

    def initConsole_CoverBoard_2(self):
        self.console2 = Console_Coverboard_2()
        #self.console.connect(self.console.button1,SIGNAL("clicked()"),self.testPrint)
        self.console2.connect(self.console2.buttonRun,SIGNAL("clicked()"),self.detect_coverBoard_2)
        self.console2.show()


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
        global newimg, original_image, ROI_flag, colourSpace
        newimg = imread(filename)
        original_image = copy.deepcopy(newimg)
        newimg = np.rot90(newimg,k=1)
        newimg = np.flipud(newimg)
        self.statusBar().showMessage('{} successfully loaded ({} s)'.format(os.path.basename(filename), time.time()-t))
        self.ImageView.view.setTitle(filename)
        colourSpace = 'rgb'
        
        if ROI_flag == False:
            self.initROI()
            ROI_flag = True
        
        return newimg


    def openDialog(self):
        global filename
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image file',
                '/home', 'Images (*.png *.xpm *.jpg *.tif *.tiff *.pdf *.ps *.eps *.raw)')

        print(filename)
        if platform.system() == "Windows":
            if (sys.version_info < (3, 0)) and (os.environ["QT_API"] == 'pyside'):
              filename=str(filename[0])            
            else:
                filename=str(filename)
        elif platform.system() == "Darwin":
            filename=str(filename)
        else:
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
        global newimg, colourSpace
        img = rgb2gray(img)
        #reset datatype to unit8 for RGB 0-255
        newimg = img_as_ubyte(img)
        self.ImageView.setImage(newimg)
        colourSpace = 'bw'
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

    def colour_picker(self):
        global picker_RGB, picker_HSV, picker_HSL
        self.colour = QtWidgets.QColorDialog.getColor()
        if self.colour.isValid(): 
            picker_RGB = self.colour.getRgb()
            picker_HSV = self.colour.getHsv()
            picker_HSL = self.colour.getHsl()
            self.statusBar().showMessage("Colour Picker: RGB = " + str(picker_RGB) +  " HSV = " +str(picker_HSV))
            #print("R: %s, G: %s, B: %s --- H: %s, S: %s, V: %s" % picker_RGB[0], picker_RGB[1], picker_RGB[2], picker_HSV[0], picker_HSV[1], picker_HSV[2])
        else:
            print('No colour selected')

    def updateWin(self):
            
        global roi_mean_hue, roi_mean_sat, roi_mean_val, roi_min_hue, roi_min_sat, roi_min_val, roi_max_hue, roi_max_sat, roi_max_val, roi_mean_red, roi_mean_green, roi_mean_blue, roi_mean_intensity, roi_min_intensity, roi_max_intensity, roi_min_red, roi_max_red, roi_min_green, roi_max_green, roi_min_blue, roi_max_blue
       
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
        
        roi_min_red = np.min(self.imgROI[:, :, 0])
        roi_min_green = np.min(self.imgROI[:, :, 1])
        roi_min_blue = np.min(self.imgROI[:, :, 2])
        roi_min_intensity = np.min(self.imgROI[:, :, :,])        
        
        roi_max_red = np.max(self.imgROI[:, :, 0])
        roi_max_green = np.max(self.imgROI[:, :, 1])
        roi_max_blue = np.max(self.imgROI[:, :, 2])
        roi_max_intensity = np.max(self.imgROI[:, :, :,])         
        
               
        roi_mean_hue, roi_mean_sat, roi_mean_val = RGB_2_HSV([roi_mean_red, roi_mean_green, roi_mean_blue])
        roi_min_hue, roi_min_sat, roi_min_val = RGB_2_HSV([roi_min_red, roi_min_green, roi_min_blue])
        roi_max_hue, roi_max_sat, roi_max_val = RGB_2_HSV([roi_max_red, roi_max_green, roi_max_blue])
        
                
        self.roi_numberPixels = np.size(self.imgROI[:, :, 0])
        
        self.statusBar().showMessage("Mean R: %d, Mean G: %d, Mean B: %d --- Mean H: %.2f, Mean S: %.2f, Mean V: %.2f --- Mean Intensity: %d, Pixels: %d" % (round(roi_mean_red,2), round(roi_mean_green,2), round(roi_mean_blue,2), round(roi_mean_hue,2), round(roi_mean_sat,2), round(roi_mean_val,2), round(roi_mean_intensity,2), self.roi_numberPixels))
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
        #import global variables
        global newimg, roi_origin, roi_size
        
        #set up array
        image = newimg

        #image stats
        
        mean_coverBoard_values = np.array(([0,0,0]))
        mean_notBoard_values = np.array(([0,0,0]))
        
        mean_red, mean_green, mean_blue = np.mean(image, axis=(0, 1))
        min_red, min_green, min_blue = np.min(image, axis=(0, 1))
        max_red, max_green, max_blue = np.max(image, axis=(0, 1))
        mean_intensity = np.mean(image)
        min_intensity = np.min(image)
        max_intensity = np.max(image)

        #copy arrays
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
                    mean_notBoard_values = mean_notBoard_values + image[x,y]

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
                        mean_coverBoard_values = mean_coverBoard_values + image[x,y]

                    else:
                        image_board[x,y] = 255
                        image_other[x,y] = 0
                        other_pixel += 1
                        mean_notBoard_values = mean_notBoard_values + image[x,y]

                #count green pixels
                elif image[x,y][g] > image[x,y][r] and image[x,y][g] > image[x,y][b]:
                    image_other[x,y] = 0
                    image_board[x,y] = 255
                    other_pixel += 1
                    mean_notBoard_values = mean_notBoard_values + image[x,y]

                #count blue pixels
                elif image[x,y][b] > image[x,y][r] and image[x,y][b] > image[x,y][g]:
                    image_board[x,y] = 255
                    image_other[x,y] = 0
                    other_pixel += 1
                    mean_notBoard_values = mean_notBoard_values + image[x,y]

                else:
                    image_other[x,y] = 0
                    image_board[x,y] = 255
                    other_pixel += 1
                    mean_notBoard_values = mean_notBoard_values + image[x,y]


        mean_notBoard_values = np.divide(mean_notBoard_values,other_pixel) 
        mean_coverBoard_values = np.divide(mean_coverBoard_values,board_pixel)

        print("board_pixels = ", board_pixel)
        print("other_pixels = ", other_pixel)
        print("ROI_pixels = ", roi_area)
        print("----------------------------------------------")
        print("Area of ROI detected as board = ", round((board_pixel/roi_area)*100, 1), " %")
        print("Area of ROI detected as other = ", round((other_pixel/roi_area)*100, 1), " %")
        print("mean intensity = %d" % round(mean_intensity,2))
        print("mean rgb = %d" % round(mean_red,2), round(mean_green,2), round( mean_blue,2))
        print("mean coverboard rgb = %d" % mean_coverBoard_values[0],mean_coverBoard_values[1],mean_coverBoard_values[2])
        print("mean other rgb = %d" % mean_notBoard_values[0],mean_notBoard_values[1],mean_notBoard_values[2])

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


    def detect_coverBoard_2(self):
        print('start analysis')
        #import global variables
        global newimg, roi_origin, roi_size, filename, roi_mean_red,\
        roi_mean_green, roi_mean_blue, roi_mean_intensity, roi_min_intensity,\
        roi_max_intensity, roi_min_red, roi_max_red, roi_min_green, roi_max_green,\
        roi_min_blue, roi_max_blue, board_min_red, board_max_red, board_mean_red,\
        board_min_green, board_max_green, board_mean_green, board_min_blue, board_max_blue,\
        board_mean_blue, board_min_intensity, board_max_intensity, board_mean_intensity,\
        board_mean_hue, board_mean_sat, board_mean_val, board_min_hue, board_min_sat, board_min_val, board_max_hue, board_max_sat, board_max_val, board_median_hue, board_median_sat, board_median_val
        
        #set up array
        image = newimg

        #image stats       
        mean_coverBoard_values = np.array(([0,0,0]))
        mean_notBoard_values = np.array(([0,0,0]))
        
        mean_red, mean_green, mean_blue = np.mean(image, axis=(0, 1))
        min_red, min_green, min_blue = np.min(image, axis=(0, 1))
        max_red, max_green, max_blue = np.max(image, axis=(0, 1))
        mean_intensity = np.mean(image)
        min_intensity = np.min(image)
        max_intensity = np.max(image)

        #copy arrays
        image_original = copy.deepcopy(image)
        image_board = copy.deepcopy(image)
        image_other = copy.deepcopy(image)

        #set image size variables
        image_x_origin = int(roi_origin[0])
        image_y_origin = int(roi_origin[1])

#        # colour settings
#        red = [255,0,0]
#        green = [0,255,0]
#        blue = [0,0,255]
#        black = [0,0,0]
#        white = [255,255,255]

#       hue = 0-360
#       sat = 0-255
#       val = 0-255

        #filter variables  
        h_buffer = 5
        s_buffer = 20
        v_buffer = 20
#        
#        h_range = abs(board_max_hue-board_min_hue) + h_buffer
#        s_range = abs(board_max_sat-board_min_sat) + s_buffer
#        v_range = abs(board_max_val-board_min_val) + v_buffer
#        
#        low_h = board_median_hue - h_range
#        low_s = board_median_sat - s_range
#        low_v = board_median_val - v_range
#        
#        high_h = board_median_hue + h_range
#        high_s = board_median_sat + s_range
#        high_v = board_median_val + v_range
 

        low_h = board_min_hue - h_buffer
        #for some reason hue valuespassed to here  are higher than they should be! Fudging problem with buffer until I can track down the error
        if board_min_hue >50 and board_min_hue <150:
            low_h = board_min_hue - h_buffer*6
        
        if board_min_hue >149:
            low_h = board_min_hue - h_buffer*10
        
        low_s = board_min_sat - s_buffer
        low_v = board_min_val - v_buffer
        
        high_h = board_max_hue + h_buffer
        high_s = board_max_sat + s_buffer
        high_v = board_max_val + v_buffer

       
        if low_h <0:
            low_h = 0
        if low_s <0:
            low_s = 0
        if low_v <0:
            low_v = 0

        if high_h >255:
            high_h = 255
        if high_s >255:
            high_s = 255
        if high_v >255:
            high_v = 255



        lower_board_range = np.array([low_h, low_s, low_v]) 
        upper_board_range = np.array([high_h, high_s, high_v]) 
        
        print(np.round(lower_board_range,2), np.round(upper_board_range,2))

        #convert image to hsc colourspace
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        
        # define range of blue color in HSV
        lower_blue = np.array([110,50,50])
        upper_blue = np.array([130,255,255])
        
        # define range of orange color in HSV
        lower_orange = np.array([5,50,50])
        upper_orange = np.array([15,255,255])
                
        #lower_board = np.array([0,100,100])
        #upper_board = np.array([100,255,255])

        lower_board = lower_board_range
        upper_board = upper_board_range
        
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_board, upper_board)
        
        detected_pixels = cv2.countNonZero(mask)
        total_pixels = np.size(image)

        print("board_pixels = ", detected_pixels)
        print("ROI_pixels = ", total_pixels)
        print("----------------------------------------------")
        print("Area of ROI detected as board = ", round((detected_pixels/total_pixels)*100, 1), " %")

        #plot result
        #image_board = np.rot90(mask, k=1)
        #image_board = np.flipud(mask)
        self.imageBoard = copy.deepcopy(mask)
        
        resultCoverBoard = pg.image(mask)

    def detect_coverBoard_3(self):
        #print('start analysis')
        print('not implemented')
        #import global variables
        global newimg, roi_origin, roi_size, filename, roi_mean_red, roi_mean_green,\
        roi_mean_blue, roi_mean_intensity, roi_min_intensity, roi_max_intensity,\
        roi_min_red, roi_max_red, roi_min_green, roi_max_green, roi_min_blue, roi_max_blue
        
        #set up array
        image = newimg


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

        #image stats
        mean_red, mean_green, mean_blue = np.mean(image, axis=(0, 1))
        min_red, min_green, min_blue = np.min(image, axis=(0, 1))
        max_red, max_green, max_blue = np.max(image, axis=(0, 1))
        mean_intensity = np.mean(image)
        min_intensity = np.min(image)
        max_intensity = np.max(image)

       
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
        print ("--------------------------------")
        print("mean intensity = %d" % round(mean_intensity,2))
        print("mean rgb = %d" % round(mean_red,2), round(mean_green,2), round( mean_blue,2))

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
            self.cameraConsole.close()
            self.console2.close()
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
                self.cameraConsole.close()
                self.console2.close()
                
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
        app.setGraphicsSystem("raster") #spyder warning recommended this
    ex = Viewer()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
