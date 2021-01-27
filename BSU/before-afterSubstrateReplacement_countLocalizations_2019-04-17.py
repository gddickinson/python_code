# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 11:06:06 2019

@author: GEORGEDICKINSON
"""

import pandas as pd
import glob
import matplotlib.pyplot as plt

#get all csv files in folder
path = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-04-17\*.csv"


fileList = glob.glob(path)

fileList = ['C:\\Users\\georgedickinson\\Documents\\BSU_work\\thunderStorm analysis\\2019-04-17\\20190417_Chris_Triangles_ANDJRectangle_WReg_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_PCD_TROLOX_power40_afterPCA 2019 April 17 14_07_53-raw-locs.csv',
 'C:\\Users\\georgedickinson\\Documents\\BSU_work\\thunderStorm analysis\\2019-04-17\\20190417_Chris_Triangles_ANDJRectangle_WReg_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_PCD_TROLOX_power40_afterPCD 2019 April 17 14_14_52-raw-locs.csv',
 'C:\\Users\\georgedickinson\\Documents\\BSU_work\\thunderStorm analysis\\2019-04-17\\20190417_Chris_Triangles_ANDJRectangle_WReg_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_PCD_TROLOX_power40_beforePCA 2019 April 17 13_59_35-raw-locs.csv']


fileList = ['C:\\Users\\georgedickinson\\Documents\\BSU_work\\thunderStorm analysis\\2019-04-17\\20190417_Chris_Triangles_ANDJRectangle_WReg_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_PCD_TROLOX_power40_2019_April_17_11_25_34-raw-locs.csv']

fileList = ['C:\\Users\\georgedickinson\\Documents\\BSU_work\\thunderStorm analysis\\2019-04-17\\20190417_Chris_Triangles_ANDJRectangle_WReg_300msExp_Mid-9nt-3...8mM_PCA_PCD_TROLOX_power40_Run2_2019_April_17_14_33_09-raw-locs.csv']

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
    
    ax1 = counts.plot.scatter(x='frame', y='counts', c='DarkBlue', ylim=(0,3000), title=name)
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
    
    ax3 = photons.plot.scatter(x='frame', y='photons', c='DarkBlue',ylim=(0,17000000),  title=name)
    #ax4 = photonsplot.scatter(x='frame', y='phtons', c='DarkBlue', ylim=(0,2000), xlim=(0,100), title=name)

    totalPhotons.append(photons.sum()['photons'])
    power.append(filePath.split('\\')[-1].split('_')[12].split('power')[-1])



