# -*- coding: utf-8 -*-
"""
Created on Thu May 23 09:21:53 2019

@author: GEORGEDICKINSON
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 11:06:06 2019

@author: GEORGEDICKINSON
"""

import pandas as pd
import glob
import matplotlib.pyplot as plt
import os

#get all csv files in folder
filePath = r"C:\Users\g_dic\OneDrive\Desktop\BSU_DATA\2020-09-11_EdNAMfull4_W0__fixed2.csv"
name = os.path.basename(filePath)

#get data
locs = pd.read_csv(filePath)

#see head
#print(locs.head(n=5))
columnNames = locs.columns.values.tolist()
print(columnNames)

#count number of localizations / frame
counts = locs.groupby(['frame']).size().reset_index(name='counts')
#plot
ax1 = counts.plot.scatter(x='frame', y='counts', c='DarkBlue', ylim=(0,1200), title=name)


#count number of localizations / frame
#photons = locs.groupby(['frame']).sum()['intensity [photon]'].reset_index(name='photons')
photons = locs.groupby(['frame']).sum()['intensity_photon'].reset_index(name='photons')
#plot
ax2 = photons.plot.scatter(x='frame', y='photons', c='DarkBlue',ylim=(0,4000000),  title=name)

#export counts and photons
dirname = os.path.dirname(filePath)
name1 = name.split('.')[0] + '_counts.csv'
name2 = name.split('.')[0] + '_photons.csv'

savename1 = os.path.join(dirname, name1)
savename2 = os.path.join(dirname, name2)

counts.to_csv(savename1)
photons.to_csv(savename2)


