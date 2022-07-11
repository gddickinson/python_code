# -*- coding: utf-8 -*-
"""
Created on Thu May 30 11:01:24 2019

@author: GEORGEDICKINSON
"""

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import h5py
import os
import shutil

#picasso hdf5 format (without averaging): ['frame', 'x', 'y', 'photons', 'sx', 'sy', 'bg', 'lpx', 'lpy']
#Column Name       |	Description                                                                                                                      |	C Data Type
#frame	            |The frame in which the localization occurred, starting with zero for the first frame.	                                                |unsigned long
#x                |The subpixel x coordinate in camera pixels	                                                                                          |float
#y	              |The subpixel y coordinate in camera pixels	                                                                                          |float
#photons	       |The total number of detected photons from this event, not including background or camera offset	                                      |float
#sx	             |The Point Spread Function width in camera pixels                                                                                       |	float
#sy	             |The Point Spread Function height in camera pixels                                                                                      |	float
#bg	             |The number of background photons per pixel, not including the camera offset                                                            |	float
#lpx	         |The localization precision in x direction, in camera pixels, as estimated by the Cramer-Rao Lower Bound of the Maximum Likelihood fit.  |	float
#lpy	         |The localization precision in y direction, in camera pixels, as estimated by the Cramer-Rao Lower Bound of the Maximum Likelihood fit.  |	float


#set filepath to hdf5
filePath = r"C:\Users\g_dic\Documents\simulated_dNAM_data\simulatedData\simulate_1_locs.hdf5"
#set xy_pos filepath
filePath_2 = r"C:\Users\g_dic\Documents\simulated_dNAM_data\simulatedData\simulate_1_xy.csv"

savePath = filePath.split('.')[0] + '_filtered.hdf5'

#info data in yaml
yamlPath = filePath.split('.')[0] + '.yaml'
yamlSavePath = filePath.split('.')[0] + '_filtered.yaml'

#open picasso hdf5 file as DF
locs = pd.read_hdf(filePath, '/locs')
#check header
headers = locs.dtypes.index
print(headers)
print(locs.head(n=1))

#scatter plot
#locs.plot.scatter(x='x',y='y')
x = locs['x']
y = locs['y']

#open xy data file as DF
locs_groundTruth = np.loadtxt(filePath_2,delimiter=',').T

#locs_groundTruth  = np.fliplr(locs_groundTruth)
locs_groundTruth = pd.DataFrame(locs_groundTruth,columns=['x','y'])

#scatter plot
#locs_groundTruth.plot.scatter(x='x',y='y')
x2 = locs_groundTruth['x']
y2 = locs_groundTruth['y']

#correct for axis flip + shift
x2 = x2-0.5
y2 = abs(y2-255.5)

#plot all data
#fig = plt.figure(figsize=(8, 8))
#ax1 = fig.add_subplot(111)
#ax1.scatter(x,y, s=1, c='r')
#ax1.scatter(x2,y2, s=4, c='b')

#save 
