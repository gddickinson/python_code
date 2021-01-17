# -*- coding: utf-8 -*-
"""
Created on Mon May 14 15:22:29 2018

@author: George
"""

from PIL import Image
import matplotlib.pyplot as plt
from skimage import io
#import gdal
#import rasterio
import os
import numpy as np
import glob
from tqdm import tqdm


path = r"D:\_FromNathan\picr_blaine\converted\\"
savePath = r"D:\_FromNathan\picr_blaine_jpg\\"

fileList = glob.glob(path + "*.tif")

for file in tqdm(fileList):
    img = io.imread(file)
    img = img.astype('int32')
    saveName = savePath + file.split("\\")[-1].split(".")[0] + ".jpg"
    io.imsave(saveName,img,quality=100)



#plt.imshow(img)