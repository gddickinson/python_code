# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 11:59:10 2019

@author: GEORGEDICKINSON
"""

import pandas as pd

#import thuderStorm loc file
#filePath = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-03-22\20193022_Chris_Triangles_ANDJRectangle_WReg__300msExp_Mid-9nt-3nM_MgCl2_18mM_003_2019_March_22_14_48_37-raw-locs.csv"
#filePath = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-03-26\20193026_Chris_Triangles_ANDRezaSideAPurified__300msExp_Mid-9nt-3nM_MgCl2_18mM_001 2019 March 26 16_10_13-raw-locs.csv"
#filePath = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-03-26\20193026_Chris_Triangles_ANDRezaSideAPurified__300msExp_Mid-9nt-3nM_MgCl2_18mM_002 2019 March 26 16_10_13-raw-locs.csv"

#filePath = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-03-28\20193028_Chris_Triangles_ANDJRectangle_WReg_300msExp_Mid-9nt-3nM_MgCl2_18mM_001 2019 March 28 11_56_20-raw-locs.csv"
#filePath = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-03-28\20193028_Chris_Triangles_ANDJRectangle_WReg_300msExp_Mid-9nt-3nM_MgCl2_18mM_002 2019 March 28 11_56_20-raw-locs.csv"
#filePath = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-03-28\20193028_Chris_Triangles_ANDJRectangle_WReg_300msExp_Mid-9nt-3nM_MgCl2_18mM_003 2019 March 28 13_36_36-raw-locs.csv"
filePath = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-04-01\20190401_Chris_Triangles_ANDReza-SideA-unPurified_300msExp_Mid-9nt-3nM_MgCl2_18mM_001 2019 April 01 11_12_29-raw-locs.csv"


#get data
locs = pd.read_csv(filePath)

#see head
print(locs.head(n=5))

#count number of localizations / frame
counts = locs.groupby(['frame']).size().reset_index(name='counts')

ax1 = counts.plot.scatter(x='frame', y='counts', c='DarkBlue', ylim=(0,500))
ax2 = counts.plot.scatter(x='frame', y='counts', c='DarkBlue', ylim=(0,500), xlim=(0,100))



#import thuderStorm loc file
#filePath2 = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-03-22\20193022_Chris_Triangles_ANDJRectangle_WReg__300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_PCD_TROLOX_004_2019_March_22_16_11_11-raw-locs.csv"
#filePath2 = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-03-26\20193026_Chris_Triangles_ANDRezaSideAPurified__300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_PCD_TROLOX_003 2019 March 26 16_52_27-raw-locs.csv"
#filePath2 = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-03-26\20193026_Chris_Triangles_ANDRezaSideAPurified__300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_PCD_TROLOX_004 2019 March 26 16_52_27-raw-locs.csv"

#filePath2 = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-03-28\20193028_Chris_Triangles_ANDJRectangle_WReg_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_PCD_TROLOX_004 2019 March 28 14_48_17-raw-locs.csv"
#filePath2 = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-03-28\20193028_Chris_Triangles_ANDJRectangle_WReg_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_PCD_TROLOX_005 2019 March 28 14_53_43-raw-locs.csv"
#filePath2 = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-03-28\20193028_Chris_Triangles_ANDJRectangle_WReg_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_PCD_TROLOX_006 2019 March 28 15_56_43-raw-locs.csv"
#filePath2 = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-04-01\20190401_Chris_Triangles_ANDReza-SideA-unPurified_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_PCD_TROLOX_002 2019 April 01 13_09_02-raw-locs.csv"
#filePath2 = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-04-03\20190403_Chris_Triangles_ANDJRectangle_WReg_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_PCD_TROLOX_001_2019_April_03_10_37_59-raw-locs.csv"
filePath2 = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-04-04\20190404_Chris_Triangles_ANDJRectangle_WReg_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_PCD_TROLOX_001 2019 April 04 13_18_02-raw-locs.csv"

#get data
locs2 = pd.read_csv(filePath2)

#see head
print(locs2.head(n=5))

#count number of localizations / frame
counts2 = locs2.groupby(['frame']).size().reset_index(name='counts')

ax3 = counts2.plot.scatter(x='frame', y='counts', c='DarkBlue', ylim=(0,2000))
ax4 = counts2.plot.scatter(x='frame', y='counts', c='DarkBlue', ylim=(0,2000),xlim=(0,5000))



#count number of photons / frame

#TOTAL PHOTONS


#count number of localizations / frame
photons = locs2.groupby(['frame']).sum()['intensity [photon]'].reset_index(name='photons')

ax5 = photons.plot.scatter(x='frame', y='photons', c='DarkBlue',ylim=(0,25000000))
#ax6 = photonsplot.scatter(x='frame', y='phtons', c='DarkBlue', ylim=(0,2000), xlim=(0,100), title=name)


