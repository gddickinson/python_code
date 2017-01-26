# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 13:06:36 2017

@author: George
"""

import operator
from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import functools


#define path
path = r"C:\Users\George\Desktop\images\Image_Interpretation\PVER Photos\DL008\\"
file = r"IMG_2073.jpg"
filename = path + file
filename2 = path + "result_" + file
filename3 = path + "result_other_" + file

#open image file
image = io.imread(filename)


def equalize(im):
    h = im.convert("L").histogram()
    lut = []
    for b in range(0, len(h), 256):
        # step size
        step = functools.reduce(operator.add, h[b:b+256]) / 255
        # create equalization lookup table
        n = 0
        for i in range(256):
            lut.append(n / step)
            n = n + h[i+b]
    # map image through lookup table
    return im.point(lut*im.layers)
    
    
    
new_image = equalize(image)    
