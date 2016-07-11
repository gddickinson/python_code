# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 11:28:22 2016

@author: George
"""

from __future__ import division
import numpy as np
from scipy import spatial
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


filename = r"C:\Users\George\Desktop\randomScatter_test\result\result_allDistancesresults.txt"
output = r"C:\Users\George\Desktop\randomScatter_test\result\result_allDistancesresults_RandomSample.txt"

data = np.loadtxt(filename, delimiter=',')
print("File loaded")

randomSample = np.random.choice(data,500000,replace=False)

np.savetxt(output, randomSample, delimiter='\t')
print("Result File Saved")

