# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
from __future__ import (absolute_import, division,print_function, unicode_literals)
import numpy as np
from scipy import stats
import matplotlib
from matplotlib import pyplot as plt
import math

pointsToFit = 4
noiseAmp = 9

#### fake data ########
#==============================================================================
# n = 500
# x = np.arange(1,n+1)
# y = np.random.rand(n,)
# y = y*noiseAmp
# z = [100,20,50,30,10,60,100,30,100]
# z1 = [0,25,20,10,5,7,15,2,0]
# 
# data = []
# for i in range(len(z)):
#     for t in range(z[i]):
#         data.append(z1[i])
#         
# data = np.array(data)        
# y = data + y
#==============================================================================
############################

FileName = "J:\\WORK\\PUFF_ANALYSIS\\FLIKA2_ShadowlessTIRF_WITH_FLASH\\11_07_2014_ShadowlessTIRF\\trial1_shadowlessTIRF_500msflash_EGTA.txt"
FileName="C:\\Users\\George\\Desktop\\BilateralFilter.txt"
#x = np.loadtxt(FileName,skiprows=0,usecols=(0,))
y = np.loadtxt(FileName,skiprows=1,usecols=(0,))
print('File1 Loaded')
n = np.size(y)
x = np.arange(1,n+1)


fitsToKeep_X =[]
fitsToKeep_Y =[]
fitNumber =[]
fitMean_Y = []

for i in range(np.size(x)-pointsToFit):
    x1 = x[i:i+pointsToFit]
    y1 = y[i:i+pointsToFit]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x1,y1)
    if slope < 1.1 and slope > -0.9 and std_err <0.2:
        fitsToKeep_X.append(x1)
        fitsToKeep_Y.append(y1)
        fitMean_Y.append(y1.mean())
        fitNumber.append(i)


fig1 = plt.plot(x,y)
#fig2 = plt.scatter(fitsToKeep_X,fitsToKeep_Y, c='r')
fig3 = plt.scatter(fitNumber,fitMean_Y, c='r')
plt.figure()
plt.hist(fitMean_Y,bins=50)
plt.figure()
plt.hist(y,bins=50)
plt.show()