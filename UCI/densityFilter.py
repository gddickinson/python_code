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

#==============================================================================
# #####  random data  ####
# N=2500
# np.random.seed(100)
# 
# x = np.random.random(N)
# y = np.random.random(N)
# #########################
#==============================================================================


####### Load X,Y data from txt file into np array #################
FileName = "J:\\WORK\\2-colour\\IP3R1-nTerminal_UCDavisIP3R1_MonoClonal\\150224SY5Y_IP3R1_SC28614_A488_AND_UCDavis-IP3R1_L24_A647_004_SC28614_XY.txt"
Output = "J:\\WORK\\2-colour\\IP3R1-nTerminal_UCDavisIP3R1_MonoClonal\\150224SY5Y_IP3R1_SC28614_A488_AND_UCDavis-IP3R1_L24_A647_004_SC28614_XY_filtered.txt"

x = np.loadtxt(FileName,skiprows=0,usecols=(0,))
y = np.loadtxt(FileName,skiprows=0,usecols=(1,))

###### Make labelled array #######
data = np.vstack((x,y))
originalData = data
##################################

print("File loaded");

### square search area #####
searchRadius = 100
density = 2

def getNumberofNeigbours(x, y, data, searchRadius):
    answer = 0
    for i in range (data[0].size):
        if abs(x-data[0][i]) < searchRadius and abs(y-data[1][i]) < searchRadius:
            answer += 1
    return answer

def filterData(data,searchRadius,density):
    filteredX = []
    filteredY = []
    for i in range (data[0].size):
        if getNumberofNeigbours(data[0][i],data[1][i],data,searchRadius) >= density:
            filteredX.append(data[0][i])
            filteredY.append(data[1][i])
            progress = (i/data[0].size)*100
            print (progress,"%");                
    answer = np.vstack((filteredX,filteredY))
    return answer
    
filteredData = filterData(data,searchRadius,density)
np.savetxt(Output, np.transpose(filteredData), delimiter=',')
print("Filtered Data Saved")

fig1 = plt.scatter(originalData[0],originalData[1], c='green')
fig2 = plt.scatter(filteredData[0],filteredData[1], c='red')

plt.show()