# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 11:06:06 2019

@author: GEORGEDICKINSON
"""

import pandas as pd
import glob
import matplotlib.pyplot as plt

#get all csv files in folder
#time=0
#path = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-04-10\*.csv"
#time=5
#path = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-04-10\time_5h\*.csv"
#path = r"D:\data\2019-04-24\20190424_Chris_Triangles_ANDJRectangle_WReg_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_25mM_PCD_TROLOX_1mM_001 2019 April 24 10_42_36-raw-locs.csv"
path = r"D:\data\2019-04-25\20190425_Chris_Triangles_ANDJRectangle_WReg_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_25mM_PCD_TROLOX_1mM_001_2019_April_25_11_23_39-raw-locs.csv"

path = r"D:\data\2019-04-25\nanoJ_analysis\20190425_Chris_Triangles_ANDJRectangle_WReg_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_25mM_PCD_TROLOX_1mM_001_2019_April_25_11_23_39-raw-drift_corrected-locs.csv"

fileList = glob.glob(path)

#TOTAL COUNTS

totalCounts = []
power = []

for i in range(len(fileList)):
    #import thuderStorm loc file
    filePath = fileList[i]
    
    name = filePath.split('\\')[-1].split('_')[13].split(' ')[0] + ": " + filePath.split('\\')[-1].split('_')[12]
      
    #get data
    locs = pd.read_csv(filePath)
    
    #see head
    #print(locs.head(n=5))
    
    #count number of localizations / frame
    counts = locs.groupby(['frame']).size().reset_index(name='counts')
    
    ax1 = counts.plot.scatter(x='frame', y='counts', c='DarkBlue', ylim=(0,1750))
    #ax2 = counts.plot.scatter(x='frame', y='counts', c='DarkBlue', ylim=(0,2000), xlim=(0,100), title=name)

    totalCounts.append(counts.sum()['counts'])
    power.append(filePath.split('\\')[-1].split('_')[12].split('power')[-1])


d = {'counts':totalCounts,'power':power}
powerDF = pd.DataFrame(data=d)     



#TOTAL PHOTONS

totalPhotons = []
power = []

for i in range(len(fileList)):
    #import thuderStorm loc file
    filePath = fileList[i]
    
    name = filePath.split('\\')[-1].split('_')[13].split(' ')[0] + ": " + filePath.split('\\')[-1].split('_')[12]
      
    #get data
    locs = pd.read_csv(filePath)
    
    #see head
    #print(locs.head(n=5))
    
    #count number of localizations / frame
    photons = locs.groupby(['frame']).sum()['intensity [photon]'].reset_index(name='photons')
    
    ax3 = photons.plot.scatter(x='frame', y='photons', c='DarkBlue',ylim=(0,20000000))
    #ax4 = photonsplot.scatter(x='frame', y='phtons', c='DarkBlue', ylim=(0,2000), xlim=(0,100), title=name)

    totalPhotons.append(photons.sum()['photons'])
    power.append(filePath.split('\\')[-1].split('_')[12].split('power')[-1])



