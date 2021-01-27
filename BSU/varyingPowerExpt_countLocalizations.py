# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 11:06:06 2019

@author: GEORGEDICKINSON
"""

import pandas as pd
import glob
import matplotlib.pyplot as plt

#get all csv files in folder
#path = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-04-05\*.csv"
path = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-04-10\*.csv"

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
    
    ax1 = counts.plot.scatter(x='frame', y='counts', c='DarkBlue', ylim=(0,1000), title=name)
    #ax2 = counts.plot.scatter(x='frame', y='counts', c='DarkBlue', ylim=(0,2000), xlim=(0,100), title=name)

    totalCounts.append(counts.sum()['counts'])
    power.append(filePath.split('\\')[-1].split('_')[12].split('power')[-1])


d = {'counts':totalCounts,'power':power}
powerDF = pd.DataFrame(data=d)     



result = powerDF.groupby(['power']).agg({'counts':['mean','std']})
result.index.name = 'power'
result.reset_index(inplace=True)
result['power'] = (result['power']).astype(int)

x= result['power']
y= result['counts']['mean']
std = result['counts']['std']

plt.errorbar(x,y,std)
plt.title("total counts v power")
plt.xlabel("power")
plt.ylabel("total counts")

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
    
    ax3 = photons.plot.scatter(x='frame', y='photons', c='DarkBlue',ylim=(0,4000000),  title=name)
    #ax4 = photonsplot.scatter(x='frame', y='phtons', c='DarkBlue', ylim=(0,2000), xlim=(0,100), title=name)

    totalPhotons.append(photons.sum()['photons'])
    power.append(filePath.split('\\')[-1].split('_')[12].split('power')[-1])





d = {'photons':totalPhotons,'power':power}
powerDF = pd.DataFrame(data=d)     

result = powerDF.groupby(['power']).agg({'photons':['mean','std']})
result.index.name = 'power'
result.reset_index(inplace=True)
result['power'] = (result['power']).astype(int)

x= result['power']
y= result['photons']['mean']
std = result['photons']['std']

plt.errorbar(x,y,std)
plt.title("total photons v power")
plt.xlabel("power")
plt.ylabel("total photons")

