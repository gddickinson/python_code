# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 17:20:41 2018

@author: George
"""

import glob, os
import numpy as np
from PIL import Image

imagePath = r"C:\\Users\\George\\Desktop\\trainingImages\\notBuilding2"
savePath = r"C:\\Users\\George\\Desktop\\splitFolder2\\"


os.chdir(imagePath)
imageFolder = []
for file in glob.glob("*.jpg"):
    imageFolder.append(file)


dimension = 100

xValues = []
for i in range(0,1000,dimension):
    xValues.append(i)

yValues = []
for i in range(0,1000,dimension):
    yValues.append(i)

print ("list loaded...")


def processImage(fname,startX, startY, endX, endY):
    centerPixel = "notBuilding"
    image = Image.open(fname)
    b, g, r = image.split()
    image = Image.merge("RGB", (g, b, r))
    #print((startX, startY, endX, endY))
    cropImage = image.crop((startX, startY, endX, endY))
               
    return cropImage, centerPixel



for i in range(0,len(imageFolder)):
    fname = imageFolder[i]
    j=0
    for xvalue in xValues:
        for yvalue in yValues:
            try:
                image, label = processImage(fname, xvalue,yvalue,xvalue+dimension,yvalue+dimension)
                image.save(savePath + "crop_" + str(i) + "_" + str(j) + "_" + str(label) + ".jpg","JPEG")
                print(savePath + "crop_" + str(i) + "_" + str(j) + "_" + str(label))
                j +=1
            except:
                pass
            
print("finished...")