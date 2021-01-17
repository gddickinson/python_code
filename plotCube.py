# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 13:32:22 2019

@author: George
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def cube_coordinates(edge_len,step_size):
    X = np.arange(0,edge_len+step_size,step_size)
    Y = np.arange(0,edge_len+step_size,step_size)
    Z = np.arange(0,edge_len+step_size,step_size)
    temp=list()
    for i in range(len(X)):
        temp.append((X[i],0,0))
        temp.append((0,Y[i],0))
        temp.append((0,0,Z[i]))
        temp.append((X[i],edge_len,0))
        temp.append((edge_len,Y[i],0))
        temp.append((0,edge_len,Z[i]))
        temp.append((X[i],edge_len,edge_len))
        temp.append((edge_len,Y[i],edge_len))
        temp.append((edge_len,edge_len,Z[i]))
        temp.append((edge_len,0,Z[i]))
        temp.append((X[i],0,edge_len))
        temp.append((0,Y[i],edge_len))
    return temp


edge_len = 10


A=cube_coordinates(edge_len,0.5)
A=list(set(A))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
A=list(zip(*A))
X,Y,Z=list(A[0]),list(A[1]),list(A[2])
ax.scatter(X,Y,Z,c='g')

plt.show()