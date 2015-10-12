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
#from scipy import spatial
#####  random data  ######################
#==============================================================================
# N=18299
# #N2=10000
# np.random.seed(100)
# 
# x = np.random.random(N)
# y = np.random.random(N)
# 
# #scale random data
# x = (x*(40000-35000))+35000
# y = (y*(40000-25000))+25000
# 
# #x2 = np.random.random(N2)
# #y2 = np.random.random(N2)
#==============================================================================
###########################################

#FileName = "J:\\WORK\\2-colour\\IP3R1_KDEL\\XY_positions\\150224_SY5Y_IP3R1_3D_003_crop1.txt"
#FileName2 = "J:\\WORK\\2-colour\\IP3R1_KDEL\\XY_positions\\150224_SY5Y_KDEL_3D_003_crop1.txt"

FileName = "J:\\WORK\\2-colour\\IP3R1-nTerminal_UCDavisIP3R1_MonoClonal\\150224SY5Y_IP3R1_SC28614_A488_AND_UCDavis-IP3R1_L24_A647_004_UCDavis_XY_filtered.txt"
FileName2 = "J:\\WORK\\2-colour\\IP3R1-nTerminal_UCDavisIP3R1_MonoClonal\\150224SY5Y_IP3R1_SC28614_A488_AND_UCDavis-IP3R1_L24_A647_004_UCDavis_XY_filtered.txt"
Output = "J:\\WORK\\2-colour\\IP3R1-nTerminal_UCDavisIP3R1_MonoClonal\\150224SY5Y_IP3R1_SC28614_A488_AND_UCDavis-IP3R1_L24_A647_004_SC28614_XY_v_SC28614_result.txt"
#Output = "J:\\WORK\\2-colour\\IP3R1_KDEL\\XY_positions\\150224_SY5Y_IP3R1vKDEL_001_3D_crop3_result.txt"


x = np.loadtxt(FileName,skiprows=0,usecols=(0,))
y = np.loadtxt(FileName,skiprows=0,usecols=(1,))
#print('File1 Loaded')
x2 = np.loadtxt(FileName2,skiprows=0,usecols=(0,))
y2 = np.loadtxt(FileName2,skiprows=0,usecols=(1,))
print('File2 Loaded')

###### Make array #################
data = np.vstack((x,y))
comparisonSet = np.vstack((x2,y2))
##############################################

########### Set square search area ############
searchRadius = 1000
##############################################

######## Functions ###########################
def getNeighbours(x, y, comparisonSet, searchRadius):
    keptX = []
    keptY = []
    for i in range (comparisonSet[0].size):
        if abs(x-comparisonSet[0][i]) < searchRadius and abs(y-comparisonSet[1][i]) < searchRadius:
            keptX.append(comparisonSet[0][i])
            keptY.append(comparisonSet[1][i])
    answer = np.vstack((keptX,keptY))
    return answer

def getDistances(x,y, searchSet, searchRadius):
    answer = []
    for i in range (searchSet[0].size):
        dist = math.sqrt((x-searchSet[0][i])*(x-searchSet[0][i])) + ((y-searchSet[1][i])*(y-searchSet[1][i]))
        if dist < searchRadius:
            answer.append(dist)
    #print(answer)
    return answer

def allDists(dataSet,comparisonSet,searchRadius):
    dataDist = []    
    for i in range (dataSet[0].size):
        distance1 = (getDistances(dataSet[0][i],dataSet[1][i],getNeighbours(dataSet[0][i],dataSet[1][i],comparisonSet,searchRadius),searchRadius))
        for s in range (len(distance1)):
            dataDist.append(distance1[s])
        print((i/dataSet[0].size)*100,"%");
    return dataDist   
    
    
#data3 = getNeighbours(data[0][3],data[1][3],comparisonSet,searchRadius)
#data3distance = shortestDistance(data['x'][5],data['y'][5],comparisonSet,searchRadius)

############# NP Array with x,y,dist #####################
distanceSet = allDists(data,comparisonSet,searchRadius)
np.savetxt(Output, np.transpose(distanceSet), delimiter=',')
print("Result File Saved")
###########################################################
hist=plt.hist(distanceSet,50)
#print (distanceSet)

#fig1 = plt.scatter(data[0],data[1], c='red')
#fig2 = plt.scatter(comparisonSet[0],comparisonSet[1], c='green')
#fig3 = plt.scatter(data3[0],data3[1], c='blue')
plt.show()