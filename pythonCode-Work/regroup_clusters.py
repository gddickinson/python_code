# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 13:29:27 2016

@author: George
"""

from __future__ import (absolute_import, division,print_function, unicode_literals)
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math


radius = 6

filename = 'C:\\Users\\George\\Desktop\\LaserSpot2\\160128\\160128_regroup_input'
filename = filename +'.txt'
output = 'C:\\Users\\George\\Desktop\\LaserSpot2\\160128\\160128_regroup_output.txt'

data = np.loadtxt(filename,skiprows=1)
print('File Loaded')


def distance(x,y,x2,y2):
    #pythagorean distance
    dist = ((x2-x)*(x2-x) + (y2-y)*(y2-y))
    dist = math.sqrt(dist)
    return dist


for i in range(len(data)):
    for j in range(len(data)):
        if data[j][3] == 1:
            dist = distance(data[i][1],data[i][2],data[j][1],data[j][2])
            if dist >0 and dist<radius:
                data[i][3] = data[i][3]+data[j][3]  
                if data[j][4] > data[i][4]:
                    data[i][4] = data[j][4]
                if data[j][5] < data[i][5]:
                    data[i][5] = data[j][5] 
                if data[j][7] < data[i][7]:
                    data[i][7] = data[j][7] 
                for each in range(len(data[j])):
                    data[j][each] = 0
                    

np.savetxt(output, data, delimiter=',')
print("Result File Saved")
###########################################################
#hist=plt.hist(distanceSet[2],50)
print (data)