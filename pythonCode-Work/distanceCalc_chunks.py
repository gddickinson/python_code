# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 16:53:45 2015

@author: George
"""

from __future__ import division
import numpy as np
from scipy import spatial
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

###### File loading ###########################

filename="J:\\WORK\\Nikon_System_Data_2\\test_of_photobleaching_persistance\\140318_COS_IP3R1_and_Tubulin\\140318_COS7_IP3R1_crop1_XY.txt"
comparisonSet=np.fromfile(filename,sep=" ")
comparisonSet=comparisonSet.reshape((len(comparisonSet)/2,2))

print("File1 loaded")

filename="J:\\WORK\\Nikon_System_Data_2\\test_of_photobleaching_persistance\\140318_COS_IP3R1_and_Tubulin\\140318_COS7_Tubulin_crop1_XY.txt"
data=np.fromfile(filename,sep=" ")
data=data.reshape((len(data)/2,2))

print("File2 loaded")


#############################################
searchRadius = 750
##############################################


#####  random data  ######################
#==============================================================================
# N=50
# N2=10000
# np.random.seed(100)
#  
# x = np.random.random(N)
# y = np.random.random(N)
#  
# x2 = np.random.random(N2)
# y2 = np.random.random(N2)
# 
# data = np.vstack((x,y))
# comparisonSet = np.vstack((x2,y2))
#==============================================================================

############################################


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


def getDistances(comparisonSet,data):
    answer = []
    for i in range(len(data)):
        searchSet = getNeighbours(data[0][i],data[1][i],comparisonSet,searchRadius)
        dist=spatial.distance_matrix(searchSet,data[i])
        dist0 = dist[:,0]
        dist0.sort()
        dist0  = dist0[dist0<searchRadius]
        answer.append(dist0)
    return answer

allDistances = getDistances(comparisonSet,data)

num_bins = 50

n, bins, patches = plt.hist(allDistances, num_bins, normed=0, facecolor='green', alpha=0.5)