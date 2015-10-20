# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 20:14:05 2015

@author: george
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('/home/george/Pictures/python.jpg',0)
plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()