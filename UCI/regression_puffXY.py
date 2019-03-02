# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 12:58:51 2015

@author: George
"""

from __future__ import (absolute_import, division,print_function, unicode_literals)
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math
from scipy import stats

filename = "J:\\WORK\\STORM_CA_Manuscript\\trial2_rise_peak_fall_xy.txt"
output = "J:\\WORK\\STORM_CA_Manuscript\\trial2_rise_peak_fall_xy_result.txt"

x1 = np.loadtxt(filename,skiprows=1,usecols=(0,))
y1 = np.loadtxt(filename,skiprows=1,usecols=(1,))

x2 = np.loadtxt(filename,skiprows=1,usecols=(2,))
y2 = np.loadtxt(filename,skiprows=1,usecols=(3,))

x3 = np.loadtxt(filename,skiprows=1,usecols=(4,))
y3 = np.loadtxt(filename,skiprows=1,usecols=(5,))

print('File Loaded')


    
Xresult = []
Yresult = []

for i in range(len(x1)):
    slope, intercept, r_value, p_value, std_err = stats.linregress([[1,x1[i]],[2,x2[i]],[3,x3[i]]])
    Xresult.append(intercept)

for i in range(len(y1)):
    slope, intercept, r_value, p_value, std_err = stats.linregress([[1,y1[i]],[2,y2[i]],[3,y3[i]]])
    Yresult.append(intercept)


xy_data = np.array([Xresult,Yresult])

np.savetxt(output,np.transpose(xy_data))
print('File Saved')
plt.scatter(Xresult,Yresult)

