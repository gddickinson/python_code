# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 15:40:58 2016

@author: George
"""

from __future__ import (absolute_import, division,print_function, unicode_literals)
import numpy as np
import pylab
import math
import random
import itertools

### Localization parameters ########
#np.random.seed(100)
N=100
Xdimension = 40000
Ydimension = 40000
meanNumberLocalizations = 10
numberLocalizationsStandardDeviation = 2
localizationXYStandardDeviation = 100

### Normal distribution function ###########
def makeNormal(mean, sd, numSamples, floatOK = True):
    samples = []
    for i in range(numSamples):
        if floatOK == True:
            samples.append(random.gauss(mean, sd))
        else:
            samples.append(int(random.gauss(mean, sd)))
    return samples

### create positions ##########
x = np.random.random(N)
y = np.random.random(N)
 
x = (x*(Xdimension))
y = (y*(Ydimension))


#### normally distributed number of localizations per position #####
localizationsAtPosition = makeNormal(meanNumberLocalizations, numberLocalizationsStandardDeviation, N, floatOK = False)
    

### normally distributed x,y for each position ######
newX = []
newY = []

for i in range(len(x)):
    newX.append(makeNormal(x[i],localizationXYStandardDeviation,localizationsAtPosition[i]))
    
for i in range(len(y)):
    newY.append(makeNormal(y[i],localizationXYStandardDeviation,localizationsAtPosition[i]))

### concatinate list ####
newX = list(itertools.chain.from_iterable(newX))
newY = list(itertools.chain.from_iterable(newY))

centerPositions = np.vstack((x,y))
normalDistributedLocalizations = np.vstack((newX,newY))


### plot xy ####

pylab.scatter(newX,newY, hold = True)
pylab.axis([0,Xdimension,0,Ydimension])
pylab.scatter(x,y, color = 'red')


filename = r'C:\\Users\\George\\Desktop\\tmp.txt'

np.savetxt(filename, np.transpose(normalDistributedLocalizations), delimiter=',')
print("Result File Saved")