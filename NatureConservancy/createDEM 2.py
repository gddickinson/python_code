# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 10:11:22 2017

@author: George
"""

from __future__ import (absolute_import, division,print_function, unicode_literals)
import os
import sys
import numpy as np
from matplotlib import pyplot as plt
from scipy.sparse import diags
from scipy import ndimage

fileName = r"C:\arcgis\dem_test\dem_test_4.png"
saveName = r"C:\arcgis\dem_test\dem_test_4.txt"


#f = open(fileName, 'r')#r returns file as str
#data = f.readlines()
##data  = set(f.read().split()) #using set
#f.close()

f = ndimage.imread(fileName)
plt.imshow(f)

newF = (f*3)+820.0

#newF = np.fliplr(newF)

plt.imshow(newF)

np.savetxt(saveName,newF, fmt='%.2f')
