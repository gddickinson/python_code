# -*- coding: utf-8 -*-
"""
Created on Fri May  4 10:45:26 2018

@author: George
"""

from scipy import ndimage
from scipy import misc
import glob, os
import numpy as np


imgPath = r"C:\Users\George\Desktop\YOLO\buildingImages\zoom_17\gt"

#size = 200 #int gives 200%
size = 0.5 #float gives fration of size
#size = (2500,2500) #tuple gives actual size

os.chdir(imgPath)
fileList = []
for file in glob.glob("*.tif"):
    fileList.append(file)

for file in fileList:

    img = ndimage.imread(file, flatten=False)
    resize = misc.imresize(img, size, interp='bilinear', mode=None)
    saveName = file.split(".")[0] + ".jpg"
    misc.imsave(saveName,resize)
    