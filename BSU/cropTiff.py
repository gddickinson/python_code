# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 15:06:34 2019

@author: GEORGEDICKINSON
"""
import numpy as np
from skimage import io
import matplotlib.pyplot as plt

imagePath = r"C:\Users\georgedickinson\Documents\BSU_work\Brett - analysis for automation\tiffs\20190226 DMAT Dimer ED 2Color.tif"

# read the image stack
img = io.imread(imagePath)
# show the image
plt.imshow(img)
plt.axis('off')


crop = img[0:100,0:100,:]

plt.imshow(crop)
plt.axis('off')