# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 15:40:58 2016

@author: George
"""

from __future__ import (absolute_import, division,print_function, unicode_literals)
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math

####  random data  ######################
N=34358
#np.random.seed(100)

x = np.random.random(N)
y = np.random.random(N)
 
#scale random data
#x = (x*(40000-35000))+35000
#y = (y*(40000-25000))+25000

x = (x*(40000))
y = (y*(40000))


output = np.vstack((x,y))

plt.scatter(x,y)

filename = r'C:\\Users\\George\\Desktop\\tmp.txt'

np.savetxt(filename, np.transpose(output), delimiter=',')
print("Result File Saved")