# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 12:17:03 2015

@author: george
"""

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math

#####  random data  ####
N=2500
np.random.seed(100)

x = np.random.random(N)
y = np.random.random(N)
#########################

###### Make labelled array #######
data = np.array( zip(x,y), dtype=[('x',float),('y',float)])
originalData = data
##################################

### square search area #####
searchRadius = 0.05
density = 20

def getNumberofNeigbours(x, y, data, searchRadius):
    answer = 0
    for i in range (len(data)):
        if abs(x-data['x'][i]) < searchRadius and abs(y-data['y'][i]) < searchRadius:
            answer += 1
    return answer

def filterData(data,searchRadius,density):
    filteredX = []
    filteredY = []
    for i in range (len(data)):
        if getNumberofNeigbours(data['x'][i],data['y'][i],data,searchRadius) >= density:
            filteredX.append(data['x'][i])
            filteredY.append(data['y'][i])                
    answer = np.array(zip(filteredX,filteredY), dtype=[('x',float),('y',float)])
    return answer
    
filteredData = filterData(data,searchRadius,density)

fig1 = plt.scatter(originalData['x'],originalData['y'], c='green')
fig2 = plt.scatter(filteredData['x'],filteredData['y'], c='red')

plt.show()