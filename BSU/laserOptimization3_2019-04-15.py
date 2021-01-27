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
path = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-04-15\*.csv"


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
    
    ax1 = counts.plot.scatter(x='frame', y='counts', c='DarkBlue', ylim=(0,2000), title=name)
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
    
    ax3 = photons.plot.scatter(x='frame', y='photons', c='DarkBlue',ylim=(0,10000000),  title=name)
    #ax4 = photonsplot.scatter(x='frame', y='phtons', c='DarkBlue', ylim=(0,2000), xlim=(0,100), title=name)

    ccccc.append(photons.sum()['photons'])
    power.append(filePath.split('\\')[-1].split('_')[12].split('power')[-1])



#plot localizations v time
x=[0,135,180,40,60]
y=[totalCounts[0:5],[totalCounts[5:10]],[totalCounts[10:15]],[totalCounts[15:20]],[totalCounts[20:25],]]
labels = [15,30,40,60,75]
colors=['r','g','b','y','o']

for y_arr, label in zip(y, labels):
    plt.scatter(x, y_arr, label=label)

plt.xlabel('time (min)')
plt.ylabel('total number of localizations')
plt.ylim(0, 1600000)
plt.title('localizations over time')
plt.legend()
plt.show()

#plot photons v time
x=[0,135,180,40,60]
y=[totalPhotons[0:5],[totalPhotons[5:10]],[totalPhotons[10:15]],[totalPhotons[15:20]],[totalPhotons[20:25],]]
labels = [15,30,40,60,75]
colors=['r','g','b','y','o']

for y_arr, label in zip(y, labels):
    plt.scatter(x, y_arr, label=label)

plt.xlabel('time (min)')
plt.ylabel('total number of hotons')
plt.ylim(0, 7000000000)
plt.title('photons over time')
plt.legend()
plt.show()

#total counts v power
plt.scatter(power,totalCounts)
plt.xlabel('power')
plt.ylabel('total number of localizations')
plt.ylim(1100000, 1600000)
plt.title('localizations v power')
plt.show()

#total photons v power
plt.scatter(power,totalPhotons)
plt.xlabel('power')
plt.ylabel('total number of photons')
plt.ylim(0, 7000000000)
plt.title('photons v power')
plt.show()

