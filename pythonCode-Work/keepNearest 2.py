# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 11:28:22 2016

@author: George
"""

from __future__ import division
import numpy as np
from scipy import spatial
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


filename = r"J:\WORK_IN_PROGRESS\Puff Anchoring\Nocodozole\SY5Y_Nocodazole_NEW_Analysis\Nocodazole\puff_XY_data\allDistances_Nocodazole_20uM.txt"
output = r"J:\WORK_IN_PROGRESS\Puff Anchoring\Nocodozole\SY5Y_Nocodazole_NEW_Analysis\Nocodazole\puff_XY_data\allDistances_Nocodazole_20uM_nearestNeighbours.txt"

distance = np.loadtxt(filename, skiprows=1,usecols=(0,))
maxamp = np.loadtxt(filename, skiprows=1,usecols=(1,))
density = np.loadtxt(filename, skiprows=1,usecols=(2,))
print("File loaded")

newDistance = []
newMaxAmp = []
newDensity = []

for i in range(len(maxamp)):
    if len(newMaxAmp) == 0:
        newMaxAmp.append(maxamp[i])
    
    elif maxamp[i] > newMaxAmp[-1]:
        newMaxAmp.append(maxamp[i])
    
for each in newMaxAmp:
    testDistance = 100000
    testDensity = 0    
    for i in range(len(maxamp)):
        if maxamp[i] == each:
            if distance[i] < testDistance:
                testDistance = distance[i]
                testDensity = density[i]

    newDistance.append(testDistance)
    newDensity.append(testDensity)



answer = np.transpose(np.vstack((newDistance,newMaxAmp,newDensity)))
#answer = np.transpose(np.vstack((newDistance,newMaxAmp)))

np.savetxt(output, answer, delimiter='\t')
print("Result File Saved")

