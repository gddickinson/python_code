# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 12:14:34 2015

@author: robot
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
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file', 
                '/home')
        
        f = open(fname, 'r')
        
        with f:        
            data = f.read()
            print(data) 


    def cameraDialog(self):        
        img = self.getImage()
        self.ImageView.setImage(img)
        time.sleep(.1)

    def cameraRecordDialog(self):        
        myCamera = Camera()
        while True:
            img = myCamera.getImage()
            img.show()
            time.sleep(.1)

    def getImage(self):
        myCamera = Camera()
        img = myCamera.getImage()
        newimg = img.getNumpy()
        del(myCamera)
        return newimg        
        
def main():
    if QtCore.QCoreApplication.instance() != None:
        app = QtCore.QCoreApplication.instance()	
    else:
        app = QtGui.QApplication(sys.argv)
    ex = Viewer()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    
