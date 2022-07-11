# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 15:31:44 2017

@author: George
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
from mpl_toolkits.mplot3d import Axes3D

T = 60.
n = 512
t = np.linspace(-T/2., T/2., n+1)
t = t[0:n]
# There's a function to set up the frequencies, but doing it by hand seems to help me think 
# things through.
k = np.array([(2. * np.pi)*i if i < n/2 else (2. * np.pi) * (i - n) 
  for i in range(n)])

ks = np.fft.fftshift(k)
slc = np.arange(0, 10, 0.5)
# I haven't quite figured out how to use the meshgrid function in numpy
T, S = np.meshgrid(t, slc)
K, S = np.meshgrid(k, slc)

# Now, we have a plane flying back and forth in a sine wave and getting painted by a radar pulse
# which is a hyperbolic secant (1/cosh)
U = 1./np.cosh(T - 10. * np.sin(S)) * np.exp(1j * 0. * T)

def waterfall(X, Y, Z, nslices):

  # Function to generate formats for facecolors
  cc = lambda arg: colorConverter.to_rgba(arg, alpha=0.3)
  # This is just wrong. There must be some way to use the meshgrid or why bother.
  verts = []
  for i in range(nslices):
    verts.append(list(zip(X[i], Z[i])))

  xmin = np.floor(np.min(X))
  xmax = np.ceil(np.max(X))
  ymin = np.floor(np.min(Y))
  ymax = np.ceil(np.max(Y))
  zmin = np.floor(np.min(Z.real))
  zmax = np.ceil(np.max(np.abs(Z)))

  fig=plt.figure()
  ax = Axes3D(fig)
 
  poly = PolyCollection(verts, facecolors=[cc('g')])
  ax.add_collection3d(poly, zs=slc, zdir='y')
  ax.set_xlim(xmin,xmax)
  ax.set_ylim(ymin,ymax)
  ax.set_zlim(zmin,zmax)
  plt.show()

waterfall(T, S, U.real, len(slc))