# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 12:17:03 2015

@author: george
"""
from __future__ import (absolute_import, division,print_function, unicode_literals)
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math
from math import radians, cos, sin, asin, sqrt
import os


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km


def distances(filename1, filename2, output):
    
    x = np.loadtxt(filename1,skiprows=1,usecols=(1,))
    y = np.loadtxt(filename1,skiprows=1,usecols=(2,))
    shade = np.loadtxt(filename1,skiprows=1,usecols=(3,))
    print('File1 Loaded')

    x2 = np.loadtxt(filename2,skiprows=1,usecols=(1,))
    y2 = np.loadtxt(filename2,skiprows=1,usecols=(2,))
    shade2 = np.loadtxt(filename2,skiprows=1,usecols=(3,))
    print('File2 Loaded')


    ###### Make array #################
    data = np.vstack((x,y,shade))
    comparisonSet = np.vstack((x2,y2, shade2))
    ##############################################
    
    ########### Set square search area ############
    searchRadius = 40000
    ##############################################
    
    ######## Functions ###########################
    def getNeighbours(x, y, comparisonSet, searchRadius):
        keptX = []
        keptY = []
        keptShade = []
        for i in range (comparisonSet[0].size):
            if abs(x-comparisonSet[0][i]) < searchRadius and abs(y-comparisonSet[1][i]) < searchRadius:
                keptX.append(comparisonSet[0][i])
                keptY.append(comparisonSet[1][i])
                keptShade.append(comparisonSet[2][i])
        answer = np.vstack((keptX,keptY,keptShade))
        return answer
    
    def getDistances(x,y,shade, searchSet, searchRadius):
        answer = []
        shadeList = []
        for i in range (searchSet[0].size):
            
            #long,lat 
            dist = haversine(x,y,searchSet[0][i],searchSet[1][i])
            
            #x,y coordinates
            #dist = ((x-searchSet[0][i])*(x-searchSet[0][i])) + ((y-searchSet[1][i])*(y-searchSet[1][i]))
            #dist = math.sqrt(dist)
            if dist < searchRadius:
                answer.append(dist)
                shadeList.append(abs(shade-searchSet[2][i]))
                #print(shade, searchSet[2][i])
        #print(answer, shadeList)
        return answer, shadeList
    
    def allDists(dataSet,comparisonSet,searchRadius):
        dataDist = []
        shadeDiffSet = []
        for i in range (dataSet[0].size):
            distance1, shadeOfsearchSet = (getDistances(dataSet[0][i],dataSet[1][i],dataSet[2][i],getNeighbours(dataSet[0][i],dataSet[1][i],comparisonSet,searchRadius),searchRadius))
            for s in range (len(distance1)):
                dataDist.append(distance1[s])
                shadeDiffSet.append(shadeOfsearchSet[s])
            print((i/dataSet[0].size)*100,"%");
        return dataDist, shadeDiffSet   
        

    
    ############# NP Array with x,y,dist #####################
    distanceSet, shadeSet = allDists(data,comparisonSet,searchRadius)
    result = np.vstack((distanceSet,shadeSet))
    np.savetxt(output, np.transpose(result), delimiter=',')
    print("Result File Saved")
    ###########################################################
    #hist=plt.hist(distanceSet,50)
    #print (distanceSet)
    
    #fig1 = plt.scatter(result[0],result[1])
    #fig2 = plt.scatter(comparisonSet[0],comparisonSet[1], c='green')
    #fig3 = plt.scatter(data3[0],data3[1], c='blue')
    #plt.show()
    return distanceSet, shadeSet



  
 
filename1 = r"C:\Google Drive\SiCr_Digitization\Data\shadeData_for_analysis\boiseRiver_shade_50nodes_centerLine1.txt"
filename2 = r"C:\Google Drive\SiCr_Digitization\Data\shadeData_for_analysis\luke_ShadeData.txt"
output = r"C:\Google Drive\SiCr_Digitization\Data\shadeData_for_analysis\result.txt"

distanceSet, shadeSet = distances(filename1, filename2, output)
   
plt.hist(distanceSet) 
plt.hist(shadeSet)  
    