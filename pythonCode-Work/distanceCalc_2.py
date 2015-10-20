# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 16:53:45 2015

@author: George
"""

from __future__ import division
import numpy as np
from scipy import spatial
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


filename="C:\\Users\\George\\Desktop\\Ab_alone\\testXY_001.txt"
storm_positions=np.fromfile(filename,sep=" ")
storm_positions=storm_positions.reshape((len(storm_positions)/2,2))
Output ="C:\\Users\\George\\Desktop\\Ab_alone\\testXY_001_result.txt"
print("File1 loaded")

filename="C:\\Users\\George\\Desktop\\Ab_alone\\testXY_001.txt"
puff_site=np.fromfile(filename,sep=" ")
puff_site=puff_site.reshape((len(puff_site)/2,2))

print("File2 loaded")

dist=spatial.distance_matrix(storm_positions,puff_site)

dist0 = dist[:,0]
dist0.sort()
dist0  = dist0[dist0<2000]


num_bins = 50

n, bins, patches = plt.hist(dist0, num_bins, normed=0, facecolor='green', alpha=0.5)

np.savetxt(Output, dist0)
print("Result Saved")