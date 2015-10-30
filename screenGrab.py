# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 18:27:39 2015

@author: george
"""

import pyscreenshot as ImageGrab
from matplotlib import pyplot as plt

# fullscreen
im=ImageGrab.grab()
#ImageMagic viewer
#im.show()

# part of the screen
im=ImageGrab.grab(bbox=(100,100,510,510)) # X1,Y1,X2,Y2

plt.imshow(im)