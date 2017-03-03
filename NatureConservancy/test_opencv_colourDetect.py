# -*- coding: utf-8 -*-
"""
Created on Fri Mar 03 12:26:13 2017

@author: George
"""

import cv2
import numpy as np
from skimage import io
import copy
#import pyqtgraph as pg
from matplotlib import pyplot as plt
from skimage.color import label2rgb, rgb2hsv


filename = r'C:\Users\George\Desktop\testImages\IMG_2039_test_crop.jpg'
#filename = r'C:\Users\George\Desktop\testImages\test.tiff'

image = cv2.imread(filename)

board_mean_values = (198,96,60)


hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# define range of blue color in HSV
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

lower_red = np.array([0,100,100])
upper_red = np.array([100,255,255])

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_red, upper_red)

detected_pixels = cv2.countNonZero(mask)
total_pixels = np.size(image)
print(detected_pixels)
print(total_pixels)
# Bitwise-AND mask and original image
#res = cv2.bitwise_and(image,image, mask= mask)

cv2.imshow('image',image)
cv2.imshow('mask',mask)
#cv2.imshow('res',res)


