# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 13:17:14 2015

@author: George
"""

import nd2reader
import numpy as np
#import cv2
import tifffile

#no filetype
filename = 'J:\\WORK\\CellLights_AND_FIXATION\\Fixation\\Fixation_cellLights-Tubulin_actin_ER_SY5Y\\151028_SY5Y_Tubulin-GFP_CellLights_005_FIX'

array = []

#make nd2 object
nd2 = nd2reader.Nd2(filename+'.nd2')

n = 0
#iterate over each image
for image in nd2:
    array.append(image)
    print(round(n/len(nd2.frames)*100), '%')
    n+=1

array = np.array(array)

#cv2.imwrite(filename+'tif', array)
tifffile.imsave(filename+'.tif',array)


print('File saved')