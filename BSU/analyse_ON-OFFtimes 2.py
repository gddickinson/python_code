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

from itertools import groupby
from operator import itemgetter

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


#set filepaths
#filePath = r"C:\Users\g_dic\Documents\BSU_DATA\luca_cal1site\2020-10-28_Cal1site_20ms_locs_fixed_render_DRIFT_2_picked_triangles.hdf5"
#filePath = r"C:\Users\g_dic\Documents\BSU_DATA\luca_cal1site\2020-10-16_Cal1site_50ms_locs_fixed_render_DRIFT_4_picked_triangles.hdf5"
filePath = r"C:\Users\g_dic\Documents\BSU_DATA\luca_cal1site\2020-10-16_Cal1site_200ms_locs_fixed_render_DRIFT_2_picked_triangles.hdf5"

#get exposure time from filename
exposure = int(filePath.split('ms')[0].split('_')[-1])

#info data in yaml
yamlPath = filePath.split('.')[0] + '.yaml'

#open picasso hdf5 file as DF
locs = pd.read_hdf(filePath, '/locs')

#check header
headers = locs.dtypes.index
print(headers)
#print(locs.shape)
#print(locs.head(n=100))
#print(locs.tail(n=100))

#create empty dataframe to store stats for all sites
allSitesStats = pd.DataFrame()

#get number of sites to iterate through
n_sites = max(locs['group'])

for pickedSite in range(n_sites):
    
    #filter by group
    groupDF = locs[locs['group']==pickedSite]
    
    #plot intensity/frame
    #fig1, ax1 = plt.subplots()
    #ax1.scatter(x=groupDF.frame, y=groupDF.photons, s=0.1, color='black')
    
    blinks_frames = []
    
    #cluster blink events based on gaps between consecutive events
    for k, g in groupby(enumerate(groupDF['frame']), lambda i_x: i_x[0] - i_x[1]):
        #print(list(map(itemgetter(1), g)))
        events = list(map(itemgetter(1), g))
        blinks_frames.append(events)
    
    #set label names for each blink event
    blinks_labels = []    
    for k, blink in enumerate(blinks_frames):
        for frame in blink:
            blinks_labels.append(k)
    
    #add labels to dataframe
    groupDF['blink'] = blinks_labels
    
    #get length of blink events
    blinkStats = groupDF.groupby(['blink']).size().reset_index(name='length_ON')
    
    #get mean blink times
    blinkTimes = groupDF.groupby(['blink']).mean()['frame'].reset_index(name='meanFrame')
    blinkStats['meanFrame'] = blinkTimes ['meanFrame']
    
    #add picked site number
    blinkStats['group'] = pickedSite
    
    #remove single frame blink events
    #blinkStats = blinkStats[blinkStats['length_ON']!=1]
    
    #get differences in mean times as estimate of OFF times
    blinkStats['dark_OFF'] = blinkStats.meanFrame.diff()
    
    #append results to final table
    allSitesStats = allSitesStats.append(blinkStats)
    
    print(pickedSite, ' finished')
 
#plot histograms
#allSitesStats.hist(['length_ON'],grid=False,bins=50)
#allSitesStats.hist(['dark_OFF'],grid=False,bins=50)   
 
mean_ON = np.mean(allSitesStats['length_ON']) * exposure
std_ON = np.std(allSitesStats['length_ON']) * exposure

mean_OFF = np.mean(allSitesStats['dark_OFF']) * exposure
std_OFF = np.std(allSitesStats['dark_OFF']) * exposure

print('mean ON time: ', mean_ON, '+/-', std_ON )
print('mean OFF time: ', mean_OFF, '+/-', std_OFF )
