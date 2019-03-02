# -*- coding: utf-8 -*-
"""
Created on Wed Jan 06 14:58:07 2016

@author: George
"""
import random
import numpy as np

x = []
y = []

for i in range(7500):
    x.append((random.random()*5000))
    y.append((random.random()*12000))


output = np.vstack((x,y))
filename = 'J:\\WORK_IN_PROGRESS\\Files for cluster analysis\\IP3R1\\RandomXY\\randomXY2.txt'
np.savetxt(filename, np.transpose(output), delimiter=',')
print("Result File Saved")