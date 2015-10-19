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
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import tifffile
import json
import re
import SimpleCV as simplecv
from SimpleCV import Camera, Display, Image
import cv2
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


        self.fromComboBox=QComboBox()
        self.fromComboBox.addItem("Filter1")
        self.fromComboBox.addItem("Filter2")
        self.fromComboBox.addItem("Filter3")
        self.fromComboBox.addItem("Filter4")
        
        self.fromSpinBox=QDoubleSpinBox()
        self.fromSpinBox.setRange(0,1000)
        self.fromSpinBox.setValue(1.00)
        
        self.toComboBox=QComboBox()
        self.toComboBox.addItem("Filter1")
        self.toComboBox.addItem("Filter2")
        self.toComboBox.addItem("Filter3")
        self.toComboBox.addItem("Filter4")
                        
        self.toLabel=QLabel("1.00")       
        
        self.dial = QDial()
        self.dial.setNotchesVisible(True)
        self.zerospinbox = ZeroSpinBox()
        
        self.button1 = QPushButton("Click to Turn Face Detect ON")
        self.facedetectFlag = False
        self.button2 = QPushButton("Quit Live Camera")
        self.liveCameraFlag = False        
        self.button3 = QPushButton("Black & White")
        self.blackandwhiteFlag = False
        
                     
        layout = QHBoxLayout()
        layout.addWidget(self.dial)
        layout.addWidget(self.zerospinbox)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)        

        layout.addWidget(self.fromComboBox)
        layout.addWidget(self.fromSpinBox)
        layout.addWidget(self.toComboBox)
        layout.addWidget(self.toLabel)


        self.setLayout(layout)
                       
        self.connect(self.dial,SIGNAL("valueChanged(int)"), self.zerospinbox.setValue)
        self.connect(self.zerospinbox,SIGNAL("valueChanged(int)"),self.dial.setValue)
        self.connect(self.zerospinbox,SIGNAL("atzero"),self.announce)
        self.connect(self.button1,SIGNAL("clicked()"),self.one)
        self.connect(self.button2,SIGNAL("clicked()"),self.two)
        self.connect(self.button3,SIGNAL("clicked()"),self.three)       
        
        self.connect(self.fromComboBox,SIGNAL("currentIndexChanged(int)"),self.updateUi)
        self.connect(self.toComboBox,SIGNAL("currentIndexChanged(int)"),self.updateUi)
        self.connect(self.fromSpinBox,SIGNAL("valueChanged(double)"),self.updateUi)        
        
        
        self.setWindowTitle("Camera Record Options")
  
    def one(self):
        if self.facedetectFlag == False:
            self.facedetectFlag = True
            self.button1.setText("Face Detect ON")
        else:
            self.facedetectFlag = False
            self.button1.setText("Face Detect OFF")


    def two(self):
        if self.liveCameraFlag == False:
            self.liveCameraFlag = True            
        else:
            self.liveCameraFlag = False
            
    

    def three(self):
        if self.blackandwhiteFlag == False:
            self.blackandwhiteFlag = True
            self.button3.setText("Colour")
        else:
            self.blackandwhiteFlag = False
            self.button3.setText("Black & White")

    #def anyButton(self, who):
    #    self.label.setText("You clicked button '%s" % who)

    def announce(self,zeros):
        print ("ZeroSpinBox has been at zero %d times" %zeros)

    def updateUi(self):
        to = unicode(self.toComboBox.currentText())
        from_ = unicode(self.fromComboBox.currentText())
        amount = self.fromSpinBox.value()
        self.to.Label.setText("%0.2f"%amount)
        
        
class Viewer(QtGui.QMainWindow):
    
    def __init__(self):
        super(Viewer, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        self.ImageView = pg.ImageView()
        self.resize(800,800)
        self.setCentralWidget(self.ImageView)
        self.statusBar()

        openTiff = QtGui.QAction(QtGui.QIcon('open.png'), 'Open tiff', self)
        openTiff.setShortcut('Ctrl+O')
        openTiff.setStatusTip('Open new tiff')
        openTiff.triggered.connect(self.openDialog1)

        openImage = QtGui.QAction(QtGui.QIcon('open.png'), 'Open image', self)
        openImage.setShortcut('Ctrl+I')
        openImage.setStatusTip('Open new Image')
        openImage.triggered.connect(self.openDialog3)
        
        openXY = QtGui.QAction(QtGui.QIcon('open.png'), 'Open XY', self)
        openXY.setShortcut('Ctrl+F')
        openXY.setStatusTip('Open new XY File')
        openXY.triggered.connect(self.openDialog2)
                
        saveFile = QtGui.QAction(QtGui.QIcon('save.png'), 'Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.saveDialog)

        startCamera = QtGui.QAction(QtGui.QIcon('save.png'), 'Take Shot', self)
        startCamera.setShortcut('Ctrl+C')
        startCamera.setStatusTip('Start Camera')
        startCamera.triggered.connect(self.cameraDialog)

        runCamera = QtGui.QAction(QtGui.QIcon('save.png'), 'Record Video', self)
        runCamera.setShortcut('Ctrl+R')
        runCamera.setStatusTip('Start Recording')
        runCamera.triggered.connect(self.cameraRecordDialog)

        quitApp = QtGui.QAction(QtGui.QIcon('save.png'), 'Quit Now', self)
        quitApp.setShortcut('Ctrl+Q')
        quitApp.setStatusTip('Quit')
        quitApp.triggered.connect(self.quitDialog)

        menubar = self.menuBar()
        fileMenu1 = menubar.addMenu('&Image Files')
        fileMenu1.addAction(openTiff)
        fileMenu1.addAction(openImage)
        fileMenu1.addAction(saveFile)
        
        fileMenu2 = menubar.addMenu('&Data Files')        
        fileMenu2.addAction(openXY)

        fileMenu3 = menubar.addMenu('&Camera')
        fileMenu3.addAction(startCamera)
        fileMenu3.addAction(runCamera)
        
        fileMenu4 = menubar.addMenu("&Quit")
        fileMenu4.addAction(quitApp)
        
        
        #self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('ImageView')
        self.show()


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

    def convertXY(self, X, Y):
        maxXScale = 200/(max(X)-min(X))
        maxYScale = 200/(max(Y)-min(Y))        
        canvas = np.zeros((200,200))        
        x = X*maxXScale
        y = Y*maxYScale

        for i in X:
            canvas[(x[i])-1,(y[i])-1] = 1        
        #print(canvas)
        return canvas   

    
    def open_xyfile(self,filename):
        self.statusBar().showMessage('Loading {}'.format(os.path.basename(filename)))
        t=time.time()        
        X = np.loadtxt(filename,skiprows=1,usecols=(0,))
        Y = np.loadtxt(filename,skiprows=1,usecols=(1,))
        xyData = self.convertXY(X,Y)       
        #print(xyData)        
        self.statusBar().showMessage('{} successfully loaded ({} s)'.format(os.path.basename(filename), time.time()-t))        
        return xyData


    def open_file(self,filename):
        self.statusBar().showMessage('Loading {}'.format(os.path.basename(filename)))
        t=time.time()
        Tiff=tifffile.TiffFile(filename)
        try:
            metadata=Tiff[0].image_description
            metadata = self.txt2dict(metadata)
        except AttributeError:
            metadata=dict()
        tif=Tiff.asarray().astype(np.float64)
        Tiff.close()        
        #tif=imread(filename,plugin='tifffile').astype(g.m.settings['internal_data_type'])
        if len(tif.shape)>3: # WARNING THIS TURNS COLOR movies TO BLACK AND WHITE BY AVERAGING ACROSS THE THREE CHANNELS
            tif=np.mean(tif,3)
        tif=np.squeeze(tif) #this gets rid of the meaningless 4th dimention in .stk files
        if len(tif.shape)==3: #this could either be a movie or a colored still frame
            if tif.shape[2]==3: #this is probably a colored still frame
                tif=np.mean(tif,2)
                tif=np.transpose(tif,(1,0)) # This keeps the x and y the same as in FIJI. 
            else:
                tif=np.transpose(tif,(0,2,1)) # This keeps the x and y the same as in FIJI. 
        elif len(tif.shape)==2: # I haven't tested whether this preserved the x y and keeps it the same as in FIJI.  TEST THIS!!
            tif=np.transpose(tif,(0,1))
        self.statusBar().showMessage('{} successfully loaded ({} s)'.format(os.path.basename(filename), time.time()-t))
        return tif  


    def open_image(self, filename):
        self.statusBar().showMessage('Loading {}'.format(os.path.basename(filename)))
        t=time.time()
        img = simplecv.Image(filename)
        newimg = img.getNumpy()
        self.statusBar().showMessage('{} successfully loaded ({} s)'.format(os.path.basename(filename), time.time()-t))
        return newimg
        
        
    def openDialog1(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open tiff file', 
                '/home', '*.tif *.tiff *.stk')
        
        filename=str(filename)
        if filename=='':
            return False
        else:
            data = self.open_file(filename)
            #print(len(data.shape))
            self.ImageView.setImage(data)
            
    def openDialog2(self):      
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open XY file', 
                '/home')
        
        filename=str(filename)
        if filename=='':
            return False
        else:
            data = self.open_xyfile(filename)
            print(len(data.shape))
            self.ImageView.setImage(data)

    def openDialog3(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Image file', 
                '/home')
        
        filename=str(filename)
        if filename=='':
            return False
        else:
            data = self.open_image(filename)
            #print(len(data.shape))
            self.ImageView.setImage(data)


    def saveDialog(self):        
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save file', 
                '/home')
        
        filename=str(filename)
        img = self.ImageView.getProcessedImage()
        print(img)
        if filename=='':
            return False
        else:
            self.statusBar().showMessage('Saving {}'.format(os.path.basename(filename)))
            #self.ImageView.export(filename)            
            cv2.imwrite(filename,img)

    def cameraDialog(self):        
        img = self.getImage()
        #file = "/home/codeplasma/test_image.png"
        # A nice feature of the imwrite method is that it will automatically choose the
        # correct format based on the file extension you provide. Convenient!
        #cv2.imwrite(file, camera_capture) 
        self.ImageView.setImage(img)
        time.sleep(.05)

    def cameraRecordDialog(self):        
        cap = cv2.VideoCapture(0)

        #app2 = QtGui.QApplication(sys.argv)
        dialogbox = Form()
        dialogbox.show()
        dialogbox.liveCameraFlag = True        
        
        while(cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
        
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            #if self.cannyFlag == True:
            #    edges = cv2.Canny(gray,100,20)

            if dialogbox.facedetectFlag == True:
                self.faceDetect(gray)        
            if dialogbox.blackandwhiteFlag == True:        
                # Display the resulting frame
                cv2.imshow('Live Camera',edges)
            else: 
                cv2.imshow('Live Camera',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break        
            if dialogbox.liveCameraFlag == False:
                break
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
        dialogbox.close()
        return
        
    def faceDetect(self, gray):
        face_cascade =cv2.CascadeClassifier('/home/george/opencv/data/haarcascades/haarcascade_frontalface_alt.xml')
        if face_cascade.empty(): raise Exception("your face_cascade is empty. are you sure, the path is correct ?")        
        eye_cascade = cv2.CascadeClassifier('/home/george/opencv/data/haarcascades/haarcascade_eye.xml')
        if eye_cascade.empty(): raise Exception("your eye_cascade is empty. are you sure, the path is correct ?")
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            #roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_gray,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        time.sleep(.05)
        return

    def getImage(self):
        #myCamera = Camera()
        #img = myCamera.getImage()
        # set camera port
        camera_port = 0         
        #Number of frames to throw away while the camera adjusts to light levels (30)
        ramp_frames = 10         
        # Now we can initialize the camera capture object with the cv2.VideoCapture class.
        # All it needs is the index to a camera port.
        camera = cv2.VideoCapture(camera_port)         
        # Captures a single image from the camera and returns it in PIL format
        def get_image(camera):
            # read is the easiest way to get a full image out of a VideoCapture object.
            retval, im = camera.read()
            return im         
        # Ramp the camera - these frames will be discarded and are only used to allow v4l2
        # to adjust light levels, if necessary
        for i in xrange(ramp_frames):
            temp = get_image(camera)
        #print("Taking image...")
        # Take the actual image we want to keep
        camera_capture = get_image(camera)        
        # You'll want to release the camera, otherwise you won't be able to create a new
        # capture object until your script exits
        del(camera)        
        img = camera_capture
        #newimg = img.getNumpy()        
        #del(myCamera)# grab the dimensions of the image and calculate the center
        # of the image
        (h, w) = img.shape[:2]
        center = (w / 2, h / 2) 
        # rotate the image by 180 degrees
        M = cv2.getRotationMatrix2D(center, 90, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h))
        #newimg = img
        return rotated        

    def quitDialog(self):
        self.ImageView.close()
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
    
