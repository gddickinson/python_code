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
import scipy
from scipy import ndimage
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import tifffile
import json
import re
import SimpleCV as simplecv
from SimpleCV import Camera, Display, Image
import pyscreenshot as ImageGrab
#from PIL import Image
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


global globimg
globimg = 'OFF'


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
        self.filterBox.addItem("Canny Filter")
        self.filterBox.addItem("2D Convolution - Average")
        self.filterBox.addItem("2D Convolution - Smooth")
        self.filterBox.addItem("2D Convolution - Gaussian")
        self.filterBox.addItem("2D Convolution - Median")
        self.filterBox.addItem("2D Convolution - Bilateral")
        self.filterBox.addItem("Invert")
        self.filterBox.addItem("Adaptive Threshold")
        self.filterBox.addItem("Laplacian Edge")
        self.filterBox.addItem("Background Subtract")
        
        self.SpinBox1=QDoubleSpinBox()
        self.SpinBox1.setRange(0,1000)
        self.SpinBox1.setValue(1.00)

        self.SpinBox2=QDoubleSpinBox()
        self.SpinBox2.setRange(0,1000)
        self.SpinBox2.setValue(1.00) 

                       
        self.filterLabel=QLabel("No Filter")       
        self.filterFlag = 'No Filter'
        
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

        layout.addWidget(self.filterBox)
        layout.addWidget(self.filterLabel)        
        layout.addWidget(self.SpinBox1)
        layout.addWidget(self.SpinBox2)


        self.setLayout(layout)
                       
        self.connect(self.dial,SIGNAL("valueChanged(int)"), self.zerospinbox.setValue)
        self.connect(self.zerospinbox,SIGNAL("valueChanged(int)"),self.dial.setValue)
        self.connect(self.zerospinbox,SIGNAL("atzero"),self.announce)
        self.connect(self.button1,SIGNAL("clicked()"),self.one)
        self.connect(self.button2,SIGNAL("clicked()"),self.two)
        self.connect(self.button3,SIGNAL("clicked()"),self.three)       
        
        self.connect(self.filterBox,SIGNAL("currentIndexChanged(int)"),self.updateUi)
        #self.connect(self.SpinBox1,SIGNAL("valueChanged(double)"),self.updateUi)        
        
        
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

        screenGrab = QtGui.QAction(QtGui.QIcon('open.png'), 'screenGrab', self)
        screenGrab.setShortcut('Ctrl+G')
        screenGrab.setStatusTip('Grab Full Screen')
        screenGrab.triggered.connect(self.fullScreenGrab)

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

        zoom = QtGui.QAction(QtGui.QIcon('open.png'), 'Zoom (interpolation)', self)
        zoom.setShortcut('Ctrl++')
        zoom.setStatusTip('Zoom')
        zoom.triggered.connect(self.zoomImage)

        shrink = QtGui.QAction(QtGui.QIcon('open.png'), 'Shrink (interpolation)', self)
        shrink.setShortcut('Ctrl+-')
        shrink.setStatusTip('Shrink')
        shrink.triggered.connect(self.shrinkImage)
                
        saveFile = QtGui.QAction(QtGui.QIcon('save.png'), 'Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.saveDialog)
        #saveFile.setEnabled = False

        startCamera = QtGui.QAction(QtGui.QIcon('save.png'), 'Take Shot', self)
        startCamera.setShortcut('Ctrl+C')
        startCamera.setStatusTip('Start Camera')
        startCamera.triggered.connect(self.cameraDialog)

        runCamera = QtGui.QAction(QtGui.QIcon('save.png'), 'Record Video', self)
        runCamera.setShortcut('Ctrl+R')
        runCamera.setStatusTip('Start Recording')
        runCamera.triggered.connect(self.cameraRecordDialog)

        activateExaminer = QtGui.QAction(QtGui.QIcon('save.png'), 'ROI Examiner', self)
        activateExaminer.setShortcut('Ctrl+E')
        activateExaminer.setStatusTip('Start Examiner')
        activateExaminer.triggered.connect(self.startROIExaminer) 


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

        fileMenu4 = menubar.addMenu('&Screen Grab')
        fileMenu4.addAction(screenGrab)
        #fileMenu4.addAction(runCamera)

        fileMenu5 = menubar.addMenu('&Transform Image')
        fileMenu5.addAction(rotateCounter)
        fileMenu5.addAction(rotateClock)
        fileMenu5.addAction(flipLR)
        fileMenu5.addAction(flipUD)        
        fileMenu5.addAction(zoom)
        fileMenu5.addAction(shrink)

        fileMenu6 = menubar.addMenu('&ROI Examiner')
        fileMenu6.addAction(activateExaminer)
        #fileMenu6.addAction(closeExaminer)
        
        fileMenu7 = menubar.addMenu("&Quit")
        fileMenu7.addAction(quitApp)
        
        
        #self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('ImageView')

        self.roiFlag = 'not changed'



 
        def updateROI(roi):
            self.roiImg = self.ImageView.getProcessedImage()
            #arr = self.roiImg.getNumpy()
            arr = np.array(self.roiImg)
            
            x = self.roi1.getArrayRegion(arr, self.ImageView.getImageItem())
            self.roiImg = x
            
            
        self.roiImg = []
        self.roi1 = pg.RectROI([40, 40], [40, 40], pen=(0,9))    
        self.roi1.addRotateHandle([1,0], [0.5, 0.5])
        self.roi1.sigRegionChanged.connect(updateROI)
        self.ImageView.addItem(self.roi1)
        
        
        
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
        ###THERE IS A FUNCTION TO DO THIS IN PYQTGRAPH!!###
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
        newimg = cv2.imread(filename,0)        
        #newimg = np.array(img) 
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

    def zoomImage(self):
        img = self.ImageView.getProcessedImage()
        r = 1.5
        dim = (int(img.shape[1] * r), int(img.shape[0] * r)) 
        # perform the actual resizing of the image and show it
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        self.ImageView.setImage(img)        
        return

    def shrinkImage(self):
        img = self.ImageView.getProcessedImage()
        r = 1.5
        dim = (int(img.shape[1] / r), int(img.shape[0] / r)) 
        # perform the actual resizing of the image and show it
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        self.ImageView.setImage(img)        
        return

    def fullScreenGrab(self):        
        img=ImageGrab.grab() 
        img = np.array(img) 
        img = np.rot90(img,k=3)
        img = np.fliplr(img)             
        self.ImageView.setImage(img)
        return

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

            #frame = np.fliplr(frame)
        
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
           
            if dialogbox.filterFlag == "2D Convolution - Average":
                kernel = np.ones((5,5),np.float32)/25
                gray = cv2.filter2D(gray,-1,kernel)            
            
            if dialogbox.filterFlag == "2D Convolution - Smooth":
                gray = cv2.blur(gray,(5,5))             
            
            if dialogbox.filterFlag == "2D Convolution - Gaussian":
                gray = cv2.GaussianBlur(gray,(5,5),0)
 
            if dialogbox.filterFlag == "2D Convolution - Median": 
                gray = cv2.medianBlur(gray,5)

            if dialogbox.filterFlag == "2D Convolution - Bilateral":                
                gray = cv2.bilateralFilter(gray,9,75,75)
           
            if dialogbox.filterFlag == "Canny Filter":
                gray = cv2.Canny(gray,100,20)

            if dialogbox.filterFlag == "Invert":
                gray = (255-gray)

            if dialogbox.filterFlag =="Adaptive Threshold":
                gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)
                gray = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 11, 1)

            if dialogbox.filterFlag=="Laplacian Edge":
                # remove noise
                img = cv2.GaussianBlur(gray,(3,3),0)
                # convolute with proper kernels
                gray = cv2.Laplacian(img,cv2.CV_64F)


            if dialogbox.filterFlag=="Background Subtract":
                fgbg = cv2.BackgroundSubtractorMOG()
                history = 10
                while dialogbox.filterFlag=="Background Subtract":
                    retVal, frame = cap.read()
                    fgmask = fgbg.apply(frame, learningRate=1.0/history)
                    cv2.imshow('Live Camera', fgmask)
                    globimg = gray
                    global globimg
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        cap.release()
                        cv2.destroyAllWindows()
                        globimg = 'OFF'
                        global globimg
                        dialogbox.close()
                        break

            if dialogbox.facedetectFlag == True:
                self.faceDetect(gray)        

            if dialogbox.blackandwhiteFlag == True:        
                # Display the resulting frame
                cv2.imshow('Live Camera',gray)
                globimg = gray
                global globimg
                
            else: 
                cv2.imshow('Live Camera',frame)
                globimg = frame
                global globimg
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break        
            if dialogbox.liveCameraFlag == False:
                break
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
        globimg = 'OFF'
        global globimg
        dialogbox.close()
        return
        
    def faceDetect(self, gray):
        face_cascade =cv2.CascadeClassifier('/home/george2/opencv/data/haarcascades/haarcascade_frontalface_alt.xml')
        if face_cascade.empty():
            print("your face_cascade is empty. are you sure, the path is correct ?")
            return
        eye_cascade = cv2.CascadeClassifier('/home/george2/opencv/data/haarcascades/haarcascade_eye.xml')
        if eye_cascade.empty():
            print("your eye_cascade is empty. are you sure, the path is correct ?")
            return
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            #roi_color = frame[y:y+h, x:x+w]
            individualEye = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in individualEye:
                cv2.rectangle(roi_gray,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        time.sleep(.01)
        return


    def getImage(self):
        if globimg == 'OFF':
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
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = np.rot90(img,k=1)
            img = np.flipud(img)
            #newimg = img
            return img        
        else:
            img = globimg
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = np.rot90(img,k=1)
            img = np.flipud(img)
            #newimg = img
            return img

    def startROIExaminer(self):
        try:
            #imgROI = self.ImageView.getProcessedImage()
            imgROI = self.roiImg
        except:
            print('No image loaded')
            return
       
        ## create GUI
        app = QtGui.QPixmap()
        w = pg.GraphicsWindow(size=(500,400), border=True)
        w.setWindowTitle('ROI Examiner')
        
        text = """Testing..."""
        w1 = w.addLayout(row=0, col=0)
        #label1 = w1.addLabel(text, row=0, col=0)
        v1a = w1.addViewBox(row=0, col=0, lockAspect=True)
        img = pg.ImageItem(imgROI)
        v1a.addItem(img)
        #self.v1a.disableAutoRange('xy')
        #self.v1a.autoRange()
        while True:
            v1a.removeItem(img)
            imgROI = self.roiImg
            imgROI = np.fliplr(imgROI)
            img = pg.ImageItem(imgROI)
            #img.rotate(180.0)
            v1a.addItem(img)
                        
            if cv2.waitKey(1) & 0xFF == ord('q'): #change this
                app.closeAllWindows()
                break
       
        return

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
    
