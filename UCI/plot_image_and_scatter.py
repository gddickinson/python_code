# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:08:35 2015

@author: George
"""


from __future__ import (absolute_import, division,print_function, unicode_literals)
from future.builtins import (bytes, dict, int, list, object, range, str, ascii, chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import win32com.client
from win32com.client import constants

######## Set filenammes & variables ###########################################
imageName  = r'J:\WORK_IN_PROGRESS\STORM\CellLights_AND_FIXATION\Calcium_Imaging_and_fixation\COS-CellLights-Red_ER\150723\150723_cos_celllights-er-rfp_5umcal520_1umip3_1umegta_uv-flash_beforeCalciumImaging_frames1-50_average_divideByLowPassFilter.tif'
#imageName  = 'J:\\WORK\\STORM_After-Cellights-and-Calcium-Imaging\\COS-CellLights-Red_ER\\150717\\150717_cos_celllights-er-rfp_5umcal520_1umip3_1umegta_uv-flash-ER_before_calcium-imaging_average_divided-by-low-pass.tif'
puffFileName = r'J:\WORK_IN_PROGRESS\STORM\CellLights_AND_FIXATION\Calcium_Imaging_and_fixation\COS-CellLights-Red_ER\150723\150723_COS_CellLights-ER-RFP_5uMCal520_1uMIP3_1uMEGTA_UV-Flash-calciumImaging.xlsx'
STORMFileName = r'J:\WORK_IN_PROGRESS\STORM\CellLights_AND_FIXATION\Calcium_Imaging_and_fixation\COS-CellLights-Red_ER\150723\150723_Cos_STORM_KDEL_XY.txt'

scaleFactor = 2 ##for FLIKA performed with pixel bining
scaleFactor2 = 160  ##160 nm / pixel

####### Plot Image ############################################################
im = plt.imread(imageName)
implot = plt.imshow(im, cmap=cm.Greys_r, interpolation = 'nearest')

################### extract puff coordinates ##################################
excel = win32com.client.Dispatch("Excel.Application")
#excel.Visible = True
workbook = excel.Workbooks.Open(puffFileName)
sheet = workbook.Worksheets('Event Data')

header=np.array(sheet.Rows(1).Value[0])
nCols=np.max(np.argwhere(header.astype(np.bool)))+1
nPuffs=np.max(np.argwhere(np.array(sheet.Columns(1).Value).astype(np.bool)))
header=header[:nCols]
puff_info=[]

for row in np.arange(nPuffs)+2:
    puff=np.array(sheet.Rows(int(row)).Value[0][:nCols])
    puff_info.append(dict(zip(header,puff)))

puffX,puffY=[],[]

for i,puff in enumerate(puff_info):
    puffX.append(puff['x']*scaleFactor)
    puffY.append(puff['y']*scaleFactor)

excel.Application.Quit()

######################## extract STORM coordinates ############################
STORMX = np.loadtxt(STORMFileName,skiprows=1,usecols=(0,))
STORMY = np.loadtxt(STORMFileName,skiprows=1,usecols=(1,))

STORMX = np.divide(STORMX,scaleFactor2)
STORMY = np.divide(STORMY,scaleFactor2)

STORMX = np.add(STORMX,0)
STORMY = np.add(STORMY,0)
##################### Make Scatter plot #######################################
# put a blue dot at (10, 20)
#plt.scatter([10], [20])

# put a red dot, size 40, at 2 locations:
#plt.scatter(x=[30, 40], y=[50, 60], c='r', s=40)

plt.scatter(STORMX,STORMY, c='r', edgecolor ='', s=3)
plt.scatter(puffX,puffY, c ='y', s =20)

plt.show()
