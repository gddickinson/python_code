# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 12:17:03 2015

@author: george
"""
from __future__ import (absolute_import, division,print_function, unicode_literals)
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math
from math import radians, cos, sin, asin, sqrt
import os

filename1 = r"C:\Google Drive\SiCr_Digitization\Data\shadeData_for_analysis\boiseRiver_shade_50nodes_centerLine1.txt"
filename2 = r"C:\Google Drive\SiCr_Digitization\Data\shadeData_for_analysis\luke_ShadeData.txt"
output = r"C:\Google Drive\SiCr_Digitization\Data\shadeData_for_analysis\result.txt"

#x = np.loadtxt(filename1,skiprows=1,usecols=(1,))
#y = np.loadtxt(filename1,skiprows=1,usecols=(2,))
shade1 = np.loadtxt(filename1,skiprows=1,usecols=(3,))
shade2 = np.loadtxt(filename2,skiprows=1,usecols=(3,))

shade1mean = np.mean(shade1)
shade2mean = np.mean(shade2)

shade1SD = np.std(shade1)
shade2SD = np.std(shade2)

text1 = 'mean = '+ str(np.round(shade1mean)) + ' StDev = ' + str(np.round(shade1SD))
text2 = 'mean = '+ str(np.round(shade2mean)) + ' StDev = ' + str(np.round(shade2SD))

plt.figure(1)
plt.subplot(211)
plt.title('Histograms of shade values')
n, bins, patches = plt.hist(shade1, 20, normed=1,facecolor='g', alpha=0.75)
plt.xlabel('shade')
plt.ylabel('probability')
plt.text(60, .1, text1)
plt.xlim(0,100)
plt.grid(True)
plt.subplot(212)
n, bins, patches = plt.hist(shade2, 40, normed=1,facecolor='g', alpha=0.75)
plt.xlabel('solar unavailable')
plt.ylabel('probability')
plt.text(60, .021, text2)
plt.xlim(0,100)
plt.grid(True)

plt.show()