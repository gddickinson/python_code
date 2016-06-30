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


filename = r"J:\WORK_IN_PROGRESS\STORM\Files for cluster analysis\IP3R1\UCDavis_Primary_labelled_Ab\Results\1-8000_dilution_data_xy\result_allDistances\result_allDistances140107_UCDavis_primary_1-8000_dilution_003_crop3.txt"
output = r"J:\WORK_IN_PROGRESS\STORM\Files for cluster analysis\IP3R1\UCDavis_Primary_labelled_Ab\Results\1-8000_dilution_data_xy\result_allDistances\result_allDistances140107_UCDavis_primary_1-8000_dilution_003_crop3_RandomSample.txt"

data = np.loadtxt(filename, delimiter=',')
print("File loaded")

randomSample = np.random.choice(data,100000,replace=False)

np.savetxt(output, randomSample, delimiter=',')
print("Result File Saved")

