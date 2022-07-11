# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 10:06:17 2016

@author: George
"""
from __future__ import (absolute_import, division,print_function, unicode_literals)
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math
import os

np.random.seed(100)

def generateRandomPoints(startX, endX, startY, endY, number):   
    x = np.random.random_integers(startX,endX,number)
    y = np.random.random_integers(startY,endY,number)        
    return list(x),list(y)

def generateRandomDimers(startX, endX, startY, endY, number, spacing = 20):
    x = np.random.random_integers(startX,endX,number)
    y = np.random.random_integers(startY,endY,number)
    newX = []
    newY = []
    for i in range(len(x)):
        #subunit1
        newX.append(x[i]+spacing)
        newY.append(y[i]-spacing)
        #subunit2      
        newX.append(x[i]+spacing)
        newY.append(y[i]+spacing)               
    return newX, newY


def generateRandomTrimers(startX, endX, startY, endY, number, spacing = 20):
    x = np.random.random_integers(startX,endX,number)
    y = np.random.random_integers(startY,endY,number)
    newX = []
    newY = []
    for i in range(len(x)):
        #subunit1
        newX.append(x[i]+spacing)
        newY.append(y[i]-spacing)
        #subunit2      
        newX.append(x[i]+spacing)
        newY.append(y[i]+spacing)
        #subunit3     
        newX.append(x[i]-spacing)
        newY.append(y[i]-spacing)
    return newX, newY


def generateRandomTetramers(startX, endX, startY, endY, number, spacing = 20):
    x = np.random.random_integers(startX,endX,number)
    y = np.random.random_integers(startY,endY,number)
    newX = []
    newY = []
    for i in range(len(x)):
        #subunit1
        newX.append(x[i]+spacing)
        newY.append(y[i]-spacing)
        #subunit2      
        newX.append(x[i]+spacing)
        newY.append(y[i]+spacing)
        #subunit3     
        newX.append(x[i]-spacing)
        newY.append(y[i]-spacing)
        #subunit4    
        newX.append(x[i]-spacing)
        newY.append(y[i]+spacing)                
    return newX, newY


def addScatter(x,y,number,standardDeviation):
    scatterX = []
    scatterY = []
    for i in range(len(x)):
        scatterX.append(np.random.normal(x[i],standardDeviation,number))
        scatterY.append(np.random.normal(y[i],standardDeviation,number))    
    return scatterX, scatterY



randomPointsX, randomPointsY = generateRandomPoints(0, 5000, 0, 5000, 50)
dimersX, dimersY = generateRandomDimers(0, 5000, 0, 5000, 50, spacing = 20)
trimersX, trimersY = generateRandomTrimers(0, 5000, 0, 5000, 50, spacing = 20)
tetramersX, tetramersY = generateRandomTetramers(0, 5000, 0, 5000, 50, spacing = 20)

allPointsX = randomPointsX + dimersX + trimersX + tetramersX
allPointsY = randomPointsY + dimersY + trimersY + tetramersY


scatteredPointsX, scatteredPointsY = addScatter(allPointsX, allPointsY,5,5)


newScatteredPointsX = np.reshape(scatteredPointsX, -1)
newScatteredPointsY = np.reshape(scatteredPointsY, -1)


fig1 = plt.scatter(tetramersX, tetramersY, c='red')
fig2 = plt.scatter(newScatteredPointsX,newScatteredPointsY, c='green')
#fig3 = plt.scatter(data3[0],data3[1], c='blue')
plt.show()


result = np.transpose(np.vstack((newScatteredPointsX,newScatteredPointsY)))

output = r"C:\Users\George\Desktop\randomScatter_test\data\results.txt"
np.savetxt(output, result, delimiter='\t')