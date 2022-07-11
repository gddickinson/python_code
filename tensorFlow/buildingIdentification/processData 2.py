# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 18:32:50 2017

@author: George
"""
import glob
import scipy
from scipy import ndimage
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import PIL.ImageOps   

# =============================================================================
# imageList_load = glob.glob(r"D:\neuralNet_data\AerialImageDataset\AerialImageDataset\train\images\*.tif")
# gtList_load = glob.glob(r"D:\neuralNet_data\AerialImageDataset\AerialImageDataset\train\gt\*.tif")
# 
# savePath = r"D:\\neuralNet_data\\AerialImageDataset\\AerialImageDataset\\train\\labelledImages\\"
# =============================================================================


imageList_load = glob.glob(r"J:\neuralNet_data\AerialImageDataset\ISPRS_BENCHMARK_DATASETS\Vaihingen\top\tiffs\*.tif")
gtList_load = glob.glob(r"J:\neuralNet_data\AerialImageDataset\ISPRS_BENCHMARK_DATASETS\Vaihingen\gts_for_participants\*.tif")

savePath = r"J:\\neuralNet_data\\AerialImageDataset\\ISPRS_BENCHMARK_DATASETS\\Vaihingen\\train\\"


dimension = 100

xValues = []
for i in range(0,1000,dimension):
    xValues.append(i)

yValues = []
for i in range(0,1000,dimension):
    yValues.append(i)

print ("list loaded...")

# =============================================================================
# def processImage(fname,gtName,startX, startY, endX, endY):
#     centerPixel = "notBuilding"
#     image = Image.open(fname)
#     gt = Image.open(gtName)
#     cropImage = image.crop((startX, startY, endX, endY))
#     cropGt = gt.crop((startX, startY, endX, endY))
#     if cropGt.getpixel(((endX-startX)/2,(endY-startY)/2)) == 255:
#         centerPixel = "building"
#     return cropImage, centerPixel
# =============================================================================


def processImage(fname,gtName,startX, startY, endX, endY):
    centerPixel = "notBuilding"
    image = Image.open(fname)
    b, g, r = image.split()
    image = Image.merge("RGB", (g, b, r))
    
    
    gt = Image.open(gtName)
    print((startX, startY, endX, endY))
    cropImage = image.crop((startX, startY, endX, endY))
    cropGt = gt.crop((startX, startY, endX, endY))
    if cropGt.getpixel(((endX-startX)/2,(endY-startY)/2)) == (0,0,255):
        centerPixel = "building"
        
    if cropGt.getpixel(((endX-startX)/2,(endY-startY)/2)) == (255,255,255):
        centerPixel = "road"
 
    if cropGt.getpixel(((endX-startX)/2,(endY-startY)/2)) == (255,255,0):
        centerPixel = "car"
               
    return cropImage, centerPixel



for i in range(0,len(imageList_load)):
    fname = imageList_load[i]
    gtName = gtList_load[i]
    j=0
    for xvalue in xValues:
        for yvalue in yValues:
            try:
                image, label = processImage(fname, gtName, xvalue,yvalue,xvalue+dimension,yvalue+dimension)
                image.save(savePath+"crop_" + str(i) + "_" + str(j) + "_" + str(label) + ".jpg","JPEG")
                print(savePath+"crop_" + str(i) + "_" + str(j) + "_" + str(label))
                j +=1
            except:
                pass
            
print("finished...")


# = plt.figure(1)
#plt.imshow(image)
#print (label)
#g.show()