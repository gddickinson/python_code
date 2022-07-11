# -*- coding: utf-8 -*-
"""
Created on Thu May 30 11:01:24 2019

@author: GEORGEDICKINSON
"""

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import h5py
import os
import shutil
import pandasql as ps
from itertools import groupby
from operator import itemgetter
from tqdm import tqdm

#picasso hdf5 format (without averaging): ['frame', 'x', 'y', 'photons', 'sx', 'sy', 'bg', 'lpx', 'lpy']
#Column Name       |	Description                                                                                                                      |	C Data Type
#frame	            |The frame in which the localization occurred, starting with zero for the first frame.	                                                |unsigned long
#x                |The subpixel x coordinate in camera pixels	                                                                                          |float
#y	              |The subpixel y coordinate in camera pixels	                                                                                          |float
#photons	       |The total number of detected photons from this event, not including background or camera offset	                                      |float
#sx	             |The Point Spread Function width in camera pixels                                                                                       |	float
#sy	             |The Point Spread Function height in camera pixels                                                                                      |	float
#bg	             |The number of background photons per pixel, not including the camera offset                                                            |	float
#lpx	         |The localization precision in x direction, in camera pixels, as estimated by the Cramer-Rao Lower Bound of the Maximum Likelihood fit.  |	float
#lpy	         |The localization precision in y direction, in camera pixels, as estimated by the Cramer-Rao Lower Bound of the Maximum Likelihood fit.  |	float


#set filepath
filePath = r"L:\Nano\Projects\NAM LAB\George D\DATA bright dark times\Length+_7_Picked\20210312_Cal1site_LPS3+7_3nm_20ms__fixed_PICKED500.hdf5"

#open picasso hdf5 file as DF
locs = pd.read_hdf(filePath, '/locs')
#check header
headers = locs.dtypes.index
#print(headers)
#print(locs.head(n=1))

#scatter plot
#locs.plot.scatter(x='x',y='y',s=1)


#plot all binding sites against time
#all origami
#locs.plot.scatter(x='frame',y='photons',c='group',colormap='tab20b',s=0.5)

amplitudes = []
maxAmplitudes = []
ONtimes = []
OFFtimes = []
nPeaks = []

print('getting peak attributes')
# loop through all origami
for origamiIndex in tqdm(range(max(locs['group']))):
    #filter by origami group
    origamiDF = locs.loc[locs['group'] == origamiIndex]
    #plot
    #origamiDF.plot.scatter(x='frame',y='photons')
    

        
    #generate list of consecutive frames (peaks)
    indexes = origamiDF['frame']
    consecutiveFrames = []
    for k,g in groupby(enumerate(indexes),lambda x:x[0]-x[1]):
        group = (map(itemgetter(1),g))
        group = list(map(int,group))
        consecutiveFrames.append(group)
    
    #append number of peaks seen at each site for each origami    
    nPeaks.append([origamiIndex, len(consecutiveFrames)])
    
    # calculate peak attributes and append to lists         
    # loop through peaks
    for i in range(len(consecutiveFrames)):
        peakDF = origamiDF.loc[origamiDF['frame'].isin(consecutiveFrames[i])]
        #append every peaks amplitude and ON time to lists, include origami and site index
        amplitudes.append([origamiIndex, np.mean(peakDF['photons'])])
        maxAmplitudes.append([origamiIndex, np.max(peakDF['photons'])])
        ONtimes.append([origamiIndex, len(peakDF['frame'])])
    
    # seperate loop to get OFF times
    OFFtimes.append([origamiIndex, consecutiveFrames[0][0]])
    for i in range(1,len(consecutiveFrames)):
        OFFtimes.append([origamiIndex, consecutiveFrames[i][0]-consecutiveFrames[i-1][-1]])

    
print('ROI analysis finished')


# experiment stats- all sites combined
amplitudes_ALL_mean = np.mean(np.array(amplitudes)[:,1])
amplitudes_ALL_std = np.std(np.array(amplitudes)[:,1])
maxAmplitudes_ALL_mean = np.mean(np.array(maxAmplitudes)[:,1])
maxAmplitudes_ALL_std = np.std(np.array(maxAmplitudes)[:,1])
ONtimes_ALL_mean = np.mean(np.array(ONtimes)[:,1])
ONtimes_ALL_std = np.std(np.array(ONtimes)[:,1])
OFFtimes_ALL_mean = np.mean(np.array(OFFtimes)[:,1])
OFFtimes_ALL_std = np.std(np.array(OFFtimes)[:,1])
nPeaks_ALL_mean = np.mean(np.array(nPeaks)[:,1])
nPeaks_ALL_std = np.std(np.array(nPeaks)[:,1])
ONtimes_ALL_median = np.median(np.array(ONtimes)[:,1])
OFFtimes_ALL_median = np.median(np.array(OFFtimes)[:,1])

# print out results
print('----------')
print('All results combined')
print('mean amplitude: {0:.2f} photons +/- {1:.2f} std'.format(amplitudes_ALL_mean,amplitudes_ALL_std))
print('mean MAX amplitude: {0:.2f} photons +/- {1:.2f} std'.format(maxAmplitudes_ALL_mean,maxAmplitudes_ALL_std))
print('mean ON time: {0:.2f} frames +/- {1:.2f} std'.format(ONtimes_ALL_mean,ONtimes_ALL_std))
print('median ON times: {0:.2f} frames +/- {1:.2f} std'.format(ONtimes_ALL_median,ONtimes_ALL_std))
print('mean OFF time: {0:.2f} frames +/- {1:.2f} std'.format(OFFtimes_ALL_mean,OFFtimes_ALL_std))
print('median OFF times: {0:.2f} frames +/- {1:.2f} std'.format(OFFtimes_ALL_median,OFFtimes_ALL_std))
print('mean number of peaks: {0:.2f} +/- {0:.2f} std'.format(nPeaks_ALL_mean,nPeaks_ALL_std)) 
print('total number of peaks: {}'.format(len(np.array(amplitudes)[:,1])))  
print('number of ROIs: {}'.format(max(locs['group'])))  

# plot histograms
#mean amp
ampHist = plt.figure(7)
plt.hist(np.array(amplitudes)[:,1],50)
plt.title('Mean Amplitudes')
plt.xlabel('amplitude')
plt.ylabel('number observed')

#max amp
ampHist = plt.figure(8)
plt.hist(np.array(maxAmplitudes)[:,1],50)
plt.title('Max Amplitudes')
plt.xlabel('amplitude')
plt.ylabel('number observed')

#ON
ONHist = plt.figure(9)
plt.hist(np.array(ONtimes)[:,1],50)
plt.title('ON times')
plt.xlabel('ON time (frames)')
plt.ylabel('number observed')

#OFF
OFFHist = plt.figure(10)
plt.hist(np.array(OFFtimes)[:,1],50)
plt.title('OFF times')
plt.xlabel('OFF time (frames)')
plt.ylabel('number observed')

#ON log
ONHist = plt.figure(9)
plt.hist(np.array(ONtimes)[:,1],50)
plt.title('ON times')
plt.xlabel('ON time (frames)')
plt.ylabel('number observed')
plt.xscale('log')

#OFF log
OFFHist = plt.figure(10)
plt.hist(np.array(OFFtimes)[:,1],100)
plt.title('OFF times')
plt.xlabel('OFF time (frames)')
plt.ylabel('number observed')
plt.xscale('log')


#export 
import pandas as pd
peakTable = pd.DataFrame(nPeaks)      # number of peaks at each site
ONtimeTable = pd.DataFrame(ONtimes)   # ON times for each peak, indexed by origami and site
OFFtimeTable = pd.DataFrame(OFFtimes) # OFF times for each peak, indexed by origami and site

savePath = filePath.split('.')[0]
peakTable.to_csv(savePath + '_peakTable.csv')
ONtimeTable.to_csv(savePath + '_ONtimeTable.csv')
OFFtimeTable.to_csv(savePath + '_OFFtimeTable.csv')
