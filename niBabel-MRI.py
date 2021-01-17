# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 18:28:05 2020

@author: George
"""

#from pyqtgraph.Qt import QtCore, QtGui
#import pyqtgraph.opengl as gl
import numpy as np
from nibabel import load, Nifti1Image
from nibabel.viewers import OrthoSlicer3D
import os
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import tifffile


path = r"C:\Users\g_dic\OneDrive\Desktop\brain"
os.chdir(path)
img = load(path + r"\T_R_MPRAGE_Axial_0001.img")
data = img.get_fdata()

#img2 = Nifti1Image(data, np.eye(4))
#img2.to_filename(os.path.join(path,'test4d.nii.gz'))




# Interpret image data as row-major instead of col-major
pg.setConfigOptions(imageAxisOrder='row-major')

app = QtGui.QApplication([])

## Create window with ImageView widget
win = QtGui.QMainWindow()
win.resize(800,800)
imv = pg.ImageView()
win.setCentralWidget(imv)
win.show()
win.setWindowTitle('pyqtgraph example: ImageView')

#imv.setImage(data)
#OrthoSlicer3D(data).show() 
tifffile.imshow(data)

tifffile.imsave(path+r'\brainScan.tiff', data)


