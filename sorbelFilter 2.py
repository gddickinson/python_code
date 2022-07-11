# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 14:56:25 2015

@author: george
"""
import cv2
from PIL import Image
import numpy as np
from scipy.ndimage import filters

img = cv2.imread('/home/george/Desktop/data/empire.jpg')
im = np.array((Image.fromarray(img)))


#Sobel derivative filters
imx = np.zeros(im.shape)
filters.sobel(im,1,imx)
imy = np.zeros(im.shape)
filters.sobel(im,0,imy)
magnitude = np.sqrt(imx**2+imy**2)


cv2.imshow('cv2',imy)
cv2.waitKey(0)
cv2.destroyAllWindows()