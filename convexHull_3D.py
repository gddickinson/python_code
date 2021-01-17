# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 18:26:23 2020

@author: g_dic
"""


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull


# 8 points defining the cube corners
pts = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
                [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1], ])


#random points on a sphere
size = 200
n = 3 # or any positive integer
x = np.random.normal(size=(size, n)) 
x /= np.linalg.norm(x, axis=1)[:, np.newaxis]
pts = x

#points clustered within sphere
def clusteredPoints(n=100):
    radius = np.random.uniform(0.0,1.0, (n,1)) 
    theta = np.random.uniform(0.,1.,(n,1))* np.pi
    phi = np.arccos(1-2*np.random.uniform(0.0,1.,(n,1)))
    x = radius * np.sin( theta ) * np.cos( phi )
    y = radius * np.sin( theta ) * np.sin( phi )
    z = radius * np.cos( theta )
    array = np.array([x,y,z]).reshape(n,3)
    return array

#pts = clusteredPoints()

#uniform pts within sphere
from scipy.special import gammainc

def sample(center = np.array([0,0,0]),radius = 1,n_per_sphere=1000):
    r = radius
    ndim = center.size
    x = np.random.normal(size=(n_per_sphere, ndim))
    ssq = np.sum(x**2,axis=1)
    fr = r*gammainc(ndim/2,ssq/2)**(1/ndim)/np.sqrt(ssq)
    frtiled = np.tile(fr.reshape(n_per_sphere,1),(1,ndim))
    p = center + np.multiply(x,frtiled)
    return p


pts = sample()


hull = ConvexHull(pts)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Plot defining corner points
ax.plot(pts.T[0], pts.T[1], pts.T[2], "ko")

# 12 = 2 * 6 faces are the simplices (2 simplices per square face)
for s in hull.simplices:
    s = np.append(s, s[0])  # Here we cycle back to the first coordinate
    ax.plot(pts[s, 0], pts[s, 1], pts[s, 2], "r-")

# Make axis label
for i in ["x", "y", "z"]:
    eval("ax.set_{:s}label('{:s}')".format(i, i))

plt.show()