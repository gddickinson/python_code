#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 11:12:17 2022

Analysis of Gabby's data

@author: george
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools

%matplotlib qt 

#filepaths
pointFile = '/Users/george/Desktop/from_Gabby/GB_132_2021_08_11_HTEndothelial_BAPTA_plate1_6_denoised_dataexcel.xlsx'
trackFile = '/Users/george/Desktop/from_Gabby/GB_132_2021_08_11_HTEndothelial_BAPTA_plate1_6_denoised_trackexcel.xlsx'

#load data into DF
pointsDF = pd.read_excel(pointFile)
tracksDF = pd.read_excel(trackFile)

#get Col names
pointsColNames = list(pointsDF.columns)
tracksColNames = list(tracksDF.columns)

#get point x,y,track data
points = pointsDF[['PositionX [µm]', 'PositionY [µm]', 'Tree ID', 'Time [s]']]
points  = points.rename(columns={"PositionX [µm]": "x", "PositionY [µm]": "y", "Tree ID": "ID", "Time [s]": "time"})

print('--- Points Columns ---')
print(pointsColNames)
print('--- Tracks Columns ---')
print(tracksColNames)

#show headers
#print(tracksDF.head(n=5))

#plot some track data
plt.figure(1)
fig1 = plt.plot(tracksDF['Mean Sq. Displacement [µm²]'], marker='.', linestyle='None')
plt.xlabel('track #')
plt.ylabel('Mean Sq. Displacement [µm²]')

plt.figure(2)
fig2 = plt.hist(tracksDF['Mean Sq. Displacement [µm²]'], bins=100, range = (0,0.6))
plt.xlabel('Mean Sq. Displacement [µm²]')
plt.ylabel('# of observations')

plt.figure(3)


#plot some point data
groups = points.groupby('ID')
for name, group in groups:
    plt.plot(group.x, group.y, marker='.', linestyle='-', markersize=3, label=name)


#plot 1 frame of points with differnt sized blobs
#fig3 = plt.scatter()





