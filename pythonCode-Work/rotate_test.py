# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 15:53:05 2015

@author: George
"""

from __future__ import (absolute_import, division,print_function, unicode_literals)
from future.builtins import (bytes, dict, int, list, object, range, str, ascii, chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import win32com.client
from win32com.client import constants
import time
from pylab import rcParams

from scipy import *
from scipy import ndimage


######## Set filenammes & variables ###########################################
imageName  = 'J:\\WORK\\STORM_After-Cellights-and-Calcium-Imaging\\COS-CellLights-Red_ER\\150717\\150717_cos_celllights-er-rfp_5umcal520_1umip3_1umegta_uv-flash-ER_before_calcium-imaging_average.tif'
#imageName  = 'J:\\WORK\\STORM_After-Cellights-and-Calcium-Imaging\\COS-CellLights-Red_ER\\150717\\150717_cos_celllights-er-rfp_5umcal520_1umip3_1umegta_uv-flash-ER_before_calcium-imaging_average_divided-by-low-pass.tif'
puffFileName = 'J:\\WORK\\STORM_After-Cellights-and-Calcium-Imaging\\COS-CellLights-Red_ER\\150717\\150717_cos_celllights-er-rfp_5umcal520_1umip3_1umegta_uv-flash-calcium-imaging_FLIKA.xlsx'
STORMFileName = 'J:\\WORK\\STORM_After-Cellights-and-Calcium-Imaging\\COS-CellLights-Red_ER\\150717\\150717_Cos_STORM_IP3R1-NTerm-A405-A647_test2_filtered-5in100.txt'

scaleFactor = 2 ##for FLIKA performed with pixel bining
scaleFactor2 = 160  ##160 nm / pixel

####### Plot Image ############################################################
#rcParams['figure.figsize'] = 11, 11

#im = plt.imread(imageName)
#implot = plt.imshow(im, cmap=cm.Greys_r, interpolation = 'nearest')



################### extract puff coordinates ##################################

def extractPuffData(data_name, puffFileName, scaleFactor):
    excel = win32com.client.Dispatch("Excel.Application")
    #excel.Visible = True
    workbook = excel.Workbooks.Open(puffFileName)
    sheet = workbook.Worksheets('Puff Data')
    
    header=np.array(sheet.Rows(1).Value[0])
    nCols=np.max(np.argwhere(header.astype(np.bool)))+1
    nPuffs=np.max(np.argwhere(np.array(sheet.Columns(1).Value).astype(np.bool)))
    header=header[:nCols]
    puff_info=[]
    
    for row in np.arange(nPuffs)+2:
        puff=np.array(sheet.Rows(int(row)).Value[0][:nCols])
        puff_info.append(dict(zip(header,puff)))
    
    puff_data = []
    
    for i,puff in enumerate(puff_info):
        puff_data.append(puff[data_name]*scaleFactor)
        
    
    excel.Application.Quit()
    return puff_data

puffX = extractPuffData('x', puffFileName, scaleFactor)
puffY = extractPuffData('y', puffFileName, scaleFactor)

centerX = np.median(puffX)
centerY = np.median(puffY)
zeroX = np.subtract(puffX, centerX)
zeroY = np.subtract(puffY, centerY)

puffXY = np.column_stack((zeroX,zeroY))
puffXY2 = ndimage.interpolation.rotate(puffXY,1, reshape=False)



puffX = puffXY2[:,0]
puffY = puffXY2[:,1]

plt.scatter(puffX, puffY, c ='y', s =20)
plt.draw()