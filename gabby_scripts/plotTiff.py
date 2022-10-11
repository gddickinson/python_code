#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 11:35:40 2022

@author: george
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.widgets import Slider
from sklearn.neighbors import KDTree
import random
from tqdm import tqdm
import os

from skimage import io

%matplotlib qt 

#Load starting points
#filepaths
# BAPTA DATA
#pointFile = '/Users/george/Desktop/from_Gabby/BAPTA/GB_132_2021_08_11_HTEndothelial_BAPTA_plate1_6_denoised_dataexcel.xlsx'
#xMin,xMax,yMin,yMax = [20,30,30,40]
#trackFile = '/Users/george/Desktop/from_Gabby/BAPTA/GB_132_2021_08_11_HTEndothelial_BAPTA_plate1_6_denoised_trackexcel.xlsx'

# NON-BAPTA DATA
pointFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_Denoisedai_trackdata.xlsx'
xMin,xMax,yMin,yMax = [20,30,30,40]

#image data
tiffFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_MMStack_Default.ome - Denoised.tif'

# read the image stack
img = io.imread(tiffFile)

#reshape axis to x,y,t
img = np.transpose(img,(1,2,0))

# show the image
plt.imshow(img[:,:,0])
plt.axis('off')


crop = img[0:100,0:100,:]

plt.imshow(crop[:,:,0])
