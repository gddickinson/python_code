# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 10:11:13 2020

@author: g_dic
"""


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# Create a 3D array
# meshgrid produces all combinations of given x and y
x=np.linspace(-3,3,256) # x goes from -3 to 3, with 256 steps
y=np.linspace(-3,3,256) # y goes from -3 to 3, with 256 steps
X,Y=np.meshgrid(x,y) # combine all x with all y

# A function of x and y for demo purposes
#Z=np.sinc(np.sqrt(X**2 + Y**2))
Z = np.zeros_like(X)

#sphere
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x2 = np.cos(u)*np.sin(v)
y2 = np.sin(u)*np.sin(v)
z2 = np.cos(v)

fig=plt.figure()
ax=fig.gca(projection='3d')

# rstride: Array row stride (step size), defaults to 1
# cstride: Array column stride (step size), defaults to 1
# rcount: Use at most this many rows, defaults to 50
# ccount: Use at most this many columns, defaults to 50

ax.plot_wireframe(X,Y,Z,color='k',rcount=25,ccount=25)

ax.plot_surface(x2, y2, z2, color="w", edgecolor="r")

plt.show()