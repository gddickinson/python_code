#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 10:11:11 2022

@author: george
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.widgets import Slider
import random
from tqdm import tqdm
import os

%matplotlib qt 

#filepaths
# Non-BAPTA DATA

msdFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_Denoised_trackMSD.xlsx'
#msdFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_yoda1_3_Denoised_trackMSD.xlsx'
#msdFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_2_Denoised_trackMSD.xlsx'
#msdFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_yoda1_2_Denoised_trackMSD.xlsx'

#set savepath
savePath = os.path.splitext(msdFile)[0]

#load data into DF
msd_DF = pd.read_excel(msdFile)

#drop uneeded cols
msd_DF = msd_DF.drop(columns=['ID','#', 'FileName', 'Type', 'Bin.ID','ND.M','No.Segments'])

#rename segments
cols = list(range(0,len(msd_DF.columns)))
msd_DF.set_axis(cols, axis=1, inplace=True)

#get Col names
#msdColNames = list(msd_DF.columns)
#print('--- MSD Columns ---')
#print(msdColNames)

#transpose df
msd_T = msd_DF.transpose()

#add column for segment number
#msd_T['Segment'] = np.arange(msd_T.shape[0])

#plot msd scatter
title = savePath.split('/')[-1]
fig = msd_T.plot(xlabel='Segment #', ylabel='Mean Sq. Displacement [µm²]', legend=False)
plt.title(title)
#plt.yscale('log')
# plt.xscale('log')
#plt.show()

#plot mean values
msd_mean = msd_T.mean(axis=1).to_list()
msd_sd = msd_T.std(axis=1).to_list()

plt.figure(2, figsize=(10,8))
fig1 = plt.scatter(cols,msd_mean)
#fig1 = plt.errorbar(cols,msd_mean, yerr=msd_sd, fmt="o")
#plt.yscale('log')
# plt.xscale('log')

plt.title(title)
plt.ylim([0,0.9])
plt.ylabel("Mean Sq. Displacement [µm²]")
plt.xlabel("Segment #")
plt.show()

saveName = savePath + '_msd_mean.png'
plt.savefig(saveName)








