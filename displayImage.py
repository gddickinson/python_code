# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 18:42:30 2015

@author: george
"""

import numpy as np
import cv2

# Load an color image in grayscale (flag: -1,0,1 -- or command)
#-1 --- cv2.IMREAD_COLOR : Loads a color image. Any transparency of image will be neglected. It is the default flag.
# 0 --- cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode
# 1 --- cv2.IMREAD_UNCHANGED : Loads image as such including alpha channel


img = cv2.imread('/home/george/Pictures/messi5.jpg',1)

# Use the function cv2.imshow() to display an image in a window. The window automatically fits to the image size.

cv2.imshow('image',img)
print('esc to exit, s to save')
k = cv2.waitKey(0) & 0xFF
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite('python.png',img)
    cv2.destroyAllWindows()