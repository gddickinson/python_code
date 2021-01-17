# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 12:15:21 2020

@author: g_dic
"""

from matplotlib import pyplot as plt
import numpy as np

t = np.linspace(0,2*np.pi,100)
xc = 3*np.random.rand() #x-coordinate of center of circle 
yc = 3*np.random.rand() #y-coordinate of center of circle
r = 2*np.random.rand() + 0.5 #radius of circle

x = r*np.cos(t)  + xc  
y = r*np.sin(t) + yc


plt.plot(x,y,'o')
plt.grid(True)
plt.axes().set_aspect('equal','datalim')