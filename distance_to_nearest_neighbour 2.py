# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 12:17:03 2015

@author: george
"""

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math

#####  random data  ######################
N=500
N2=10000
np.random.seed(100)

x = np.random.random(N)
y = np.random.random(N)

x2 = np.random.random(N2)
y2 = np.random.random(N2)
###########################################

###### Make labelled array #################
data = np.array( zip(x,y), dtype=[('x',float),('y',float)])
comparisonSet = np.array( zip(x2,y2), dtype=[('x',float),('y',float)])
##############################################

########### Set square search area ############
searchRadius = 0.1
##############################################

######## Functions ###########################
def getNeigbours(x, y, comparisonSet, searchRadius):
    keptX = []
    keptY = []
    for i in range (len(comparisonSet)):
        if abs(x-comparisonSet['x'][i]) < searchRadius and abs(y-comparisonSet['y'][i]) < searchRadius:
            keptX.append(comparisonSet['x'][i])
            keptY.append(comparisonSet['y'][i])
    answer = np.array(zip(keptX,keptY), dtype=[('x',float),('y',float)])
    return answer

def shortestDistance(x,y, searchSet, searchRadius):
    answer = searchRadius
    for i in range (len(searchSet)):
        dist = math.sqrt((x-searchSet['x'][i])*(x-searchSet['x'][i])) + ((y-searchSet['y'][i])*(y-searchSet['y'][i]))
        if dist < answer:
            answer = dist
    return answer

def dataShortestDist(dataSet,comparisonSet,searchRadius):
    dataX = []
    dataY = []
    dataDist = []    
    for i in range (len(dataSet)):
        dataX.append(dataSet['x'][i])
        dataY.append(dataSet['y'][i])
        dataDist.append(shortestDistance(dataSet['x'][i],dataSet['y'][i],comparisonSet,searchRadius))
    answer = np.array(zip(dataX,dataY,dataDist), dtype=[('x',float),('y',float),('dist',float)])
    return answer    
    
    
#data3 = getNeigbours(data['x'][5],data['y'][5],comparisonSet,searchRadius)
#data3distance = shortestDistance(data['x'][5],data['y'][5],comparisonSet,searchRadius)

############# NP Array with x,y,dist #####################
distanceSet = dataShortestDist(data,comparisonSet,searchRadius)
###########################################################
hist=plt.hist(distanceSet['dist'],50)
print distanceSet

#fig1 = plt.scatter(data['x'],data['y'], c='red')
#fig2 = plt.scatter(comparisonSet['x'],comparisonSet['y'], c='green')
#fig3 = plt.scatter(data3['x'],data3['y'], c='blue')
plt.show()