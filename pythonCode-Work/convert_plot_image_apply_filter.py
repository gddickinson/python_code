# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 14:58:35 2015

@author: George
"""

from __future__ import (absolute_import, division,print_function, unicode_literals)
#from future.builtins import (bytes, dict, int, list, object, range, str, ascii, chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
#import win32com.client
#from win32com.client import constants
import time
from pylab import rcParams
import scipy.ndimage as ndi

imageName  = 'J:\\WORK\\STORM_After-Cellights-and-Calcium-Imaging\\COS-CellLights-Red_ER\\150723\\150723_cos_celllights-er-rfp_5umcal520_1umip3_1umegta_uv-flash-ER_after_Calicum-imaging_before-Fix-Average.tif'
puffFileName = 'J:\\WORK\\STORM_After-Cellights-and-Calcium-Imaging\\COS-CellLights-Red_ER\\150723\\150723_cos_celllights-er-rfp_5umcal520_1umip3_1umegta_uv-flash_Calicum-imaging_FLIKA_XY.txt'
STORMFileName = 'J:\\WORK\\STORM_After-Cellights-and-Calcium-Imaging\\COS-CellLights-Red_ER\\150723\\150723_Cos_STORM_KDEL_Cy3-A647_001.txt'
#STORMFileName = 'J:\\WORK\\STORM_After-Cellights-and-Calcium-Imaging\\COS-CellLights-Red_ER\\150723\\150723_Cos_STORM_IP3R1_AB5882_Cy3-A647_005.txt'
#STORMFileName = 'J:\\WORK\\STORM_After-Cellights-and-Calcium-Imaging\\COS-CellLights-Red_ER\\150723\\150723_Cos_STORM_IP3R1_AB5882_Cy3-A647_ALL.txt'

scaleFactor = 2 ##for FLIKA performed with pixel bining
scaleFactor2 = 161  ##160 nm / pixel


puffX = np.loadtxt(puffFileName,skiprows=1,usecols=(0,))
puffY = np.loadtxt(puffFileName,skiprows=1,usecols=(1,))

puffX = np.multiply(puffX, scaleFactor)
puffY = np.multiply(puffY, scaleFactor)

######################## extract STORM coordinates ############################
STORMX = np.loadtxt(STORMFileName,skiprows=1,usecols=(3,))
STORMY = np.loadtxt(STORMFileName,skiprows=1,usecols=(4,))

STORMX = np.divide(STORMX,scaleFactor2)
STORMY = np.divide(STORMY,scaleFactor2)

#######################  shifted STORM positions ##############################
Xshift = 15
Yshift = 20

STORMX = np.add(STORMX, Xshift)
STORMY = np.add(STORMY, Yshift)

originalSTORMX = STORMX
originalSTORMY = STORMY

#data = np.random.rand(30000,2)*255       ## create random dataset for testing

#################### convert data points to image array ######################

img = np.zeros((300,300))                ## blank image
for i in range(len(STORMX)):          ## draw pixels
    img[STORMX[i], STORMY[i]] += 1

############################## apply filters ##########
img = ndi.gaussian_filter(img, (1,1))  ## gaussian convolution
#img = ndi.grey_closing(img, size=(3,3)) ##grey closing

implot = plt.imshow(img, cmap=cm.Greys_r, interpolation = 'nearest', vmin=0, vmax=50) #vmax=255