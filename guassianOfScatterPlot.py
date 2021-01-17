# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 12:46:44 2019

@author: George
"""

import numpy as np
from matplotlib import pyplot as plt

def gaussianSum1D(gridpoints, datapoints, sigma=1):

    a = np.exp( -((gridpoints[:,None]-datapoints)/sigma)**2 )

    return a

#some test data
x = np.random.rand(10000)
y = np.random.rand(10000)

#create grids
gridSize = 100
xedges = np.linspace(np.min(x), np.max(x), gridSize)
yedges = np.linspace(np.min(y), np.max(y), gridSize)

#calculate weights for both dimensions seperately
a = gaussianSum1D(xedges, x, sigma=2)
b = gaussianSum1D(yedges, y, sigma=0.1)

Z = np.dot(a, b.T).T

#plot original data
fig, ax = plt.subplots()
ax.scatter(x, y, s = 1)
#overlay data with contours 
ax.contour(xedges, yedges, Z, cmap = "jet")