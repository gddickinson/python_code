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
import os

#==============================================================================
# #####  random data  ######################
# N=500
# N2=10000
# np.random.seed(100)
# 
# x = np.random.random(N)
# y = np.random.random(N)
# 
# x2 = np.random.random(N2)
# y2 = np.random.random(N2)
# ###########################################
#==============================================================================

path1 = 'J:\\WORK_IN_PROGRESS\\STORM\\Calcium_STORM\\150317\\Distance_from_puff_to_nearest_IP3R\\KDEL_andIP3R-clusters\\IP3R1\\'
path2 = 'J:\\WORK_IN_PROGRESS\\STORM\\Calcium_STORM\\150317\\Distance_from_puff_to_nearest_IP3R\\KDEL_andIP3R-clusters\\KDEL\\'
path3 = 'J:\\WORK_IN_PROGRESS\\STORM\\Calcium_STORM\\150317\\Distance_from_puff_to_nearest_IP3R\\KDEL_andIP3R-clusters\\result_nearestNeigbours\\'
files = os.listdir(path1)

for filename in files:

    FileName = path1 + filename
    FileName2 = path2 + filename
    OutputFilename = path3 + 'result_' + filename
    
    x = np.loadtxt(FileName,skiprows=0,usecols=(0,))
    y = np.loadtxt(FileName,skiprows=0,usecols=(1,))
    print('File1 Loaded')
    
    
    x2 = np.loadtxt(FileName2,skiprows=0,usecols=(0,))
    y2 = np.loadtxt(FileName2,skiprows=0,usecols=(1,))
    print('File2 Loaded')
    
    
    ###### Make array #################
    data = np.vstack((x,y))
    comparisonSet = np.vstack((x2,y2))
    ##############################################
    
    ########### Set square search area ############
    searchRadius = 40000
    ##############################################
    
    ######## Functions ###########################
    #==============================================================================
    def getNeigbours(x, y, comparisonSet, searchRadius):
        keptX = []
        keptY = []
        for i in range (comparisonSet[0].size):
            if abs(x-comparisonSet[0][i]) < searchRadius and abs(y-comparisonSet[1][i]) < searchRadius:
                keptX.append(comparisonSet[0][i])
                keptY.append(comparisonSet[1][i])
        answer = np.vstack((keptX,keptY))
        answer = len(answer)
        return answer
    #==============================================================================
    
    def shortestDistance(x,y, searchSet, searchRadius):
        answer = searchRadius
        for i in range (searchSet[0].size):
            dist = ((x-searchSet[0][i])*(x-searchSet[0][i])) + ((y-searchSet[1][i])*(y-searchSet[1][i]))
            dist = math.sqrt(dist)
            #print(i, dist, answer)
            if dist < answer:
                if dist > 0:
                    answer = dist
        return answer
    
    def dataShortestDist(dataSet,comparisonSet,searchRadius):
        dataX = []
        dataY = []
        dataDist = []    
        for i in range (dataSet[0].size):
            dataX.append(dataSet[0][i])
            dataY.append(dataSet[1][i])
            dataDist.append(shortestDistance(dataSet[0][i],dataSet[1][i],comparisonSet,searchRadius))
            #print(i);
        answer = np.vstack((dataX,dataY,dataDist))
        return answer    
    
        
    #data3distance = shortestDistance(data['x'][5],data['y'][5],comparisonSet,searchRadius)
    
    ############# number of nearest neighbours #####################
    #numberNearestLocalizations = []    
    #for i in range(len(x)):    
    #    numberNearestLocalizations.append(getNeigbours(x[i],y[i],comparisonSet,searchRadius))
    #    print (((i)/len(x))*100)
    #np.savetxt(OutputFilename, numberNearestLocalizations, delimiter=',')
    #print("Result File Saved")
    ###########################################################
    
    #==============================================================================
    # 
    # ############# NP Array with x,y,dist #####################
    distanceSet = dataShortestDist(data,comparisonSet,searchRadius)
    
    uniqueDistances = list(set(distanceSet[2]))
    
    np.savetxt(OutputFilename, np.transpose(uniqueDistances), delimiter=',')
    print("Result File Saved")
    ###########################################################
    #hist=plt.hist(distanceSet[2])
    #print (distanceSet)
     
    #fig1 = plt.scatter(data[0],data[1], c='red')
    #fig2 = plt.scatter(comparisonSet[0],comparisonSet[1], c='green')
    #fig3 = plt.scatter(data3[0],data3[1], c='blue')
    #==============================================================================
    #plt.show()
