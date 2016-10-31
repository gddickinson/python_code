# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 19:17:27 2016

@author: george
"""

from scipy.misc import imread
import numpy as np
import os, sys

def unrollImages(pathRoot, numberOfLabels):

    def flattenImage(filename):
        img = imread(filename)
        img = img.flatten()
        return img
        
    def createXArray(fileList):
        Xarray = map(lambda x: flattenImage(x),fileList)
        return Xarray
    
    def createYArray(fileList, numberOfLabels):
        Yarray = map(lambda x: (x[x.index('_C')+2:x.index('_C')+4]),fileList)
        identityMatrix = np.identity(numberOfLabels+1)
        Yarray = map(lambda x: identityMatrix[int(x)], Yarray)
        return Yarray
    
    def listFilesInDirectory(pathRoot):
        ans = []
        for path, subdirs, files in os.walk(pathRoot):
            for name in files:
                ans.append(os.path.join(path, name))
        return ans
       
    dataSet = listFilesInDirectory(pathRoot)    
    X = np.array(createXArray(dataSet))
    Y = np.array(createYArray(dataSet,numberOfLabels))
    
    return X,Y

#testX, testY = unrollImages("/home/george/plant_identifyer/data/RGB/1. Quercus suber/", 40)