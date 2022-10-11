#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 20:20:36 2022

@author: george
"""

import matplotlib.pyplot as plt
import numpy as np

#setting the centroid
x_centroid=5
y_centroid=5

#generating random points
theta=np.random.uniform(0,2*np.pi,100)

#defining the radius
r=10

#defining x and y
x=r*np.cos(theta)+x_centroid
y=r*np.sin(theta)+y_centroid

#plotting the points
plt.scatter(x,y)
plt.show()