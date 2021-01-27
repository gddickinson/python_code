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

#get all csv files in folder
#filePath = r"D:\data\2019-05-22\20190522_Chris_Triangles_ANDJRectangle_ASCII_NAM-HD-locs.csv"
#name = '20190522_Chris_Triangles_ANDJRectangle_ASCII_NAM-HD'
  
#filePath = r"D:\data\2019-05-13\20190510_Chris_Triangles_ANDJRectangle_ASCII-NAM-locs.csv"
#name = '20190510_Chris_Triangles_ANDJRectangle_ASCII-NAM-locs'

#filePath = r"D:\data\2019-05-24\fromKestrel\20190524_Chris_Triangles_ANDJRectangle_ASCII_SRC-locs_fixed.csv"
#name = '20190524_Chris_Triangles_ANDJRectangle_ASCII_SRC-locs'

#filePath = r"D:\data\2019-05-29\fromKestrel\20190529_FlowCell_Chris_Triangles_ANDJRectangle_ASCII__300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_12mM_PCD_TROLOX_1mM 11_27_40-raw-locs_fixed.csv"
#name = '20190529_FlowCell_Chris_Triangles_ANDJRectangle_ASCII_SRC-locs'

#filePath = r"D:\data\2019-07-12\20190712_Concatonated-locs.csv"
#name = r"20190712_Concatonated-locs"

filePath = r"Y:\George_D_DATA\2019-10-25\noUV\20191025_Tile7_NO_UV_002-locs.csv"
name = r"20191025_Tile7_NO_UV_002"

#get data
locs = pd.read_csv(filePath)

#see head
#print(locs.head(n=5))

#count number of localizations / frame
counts = locs.groupby(['frame']).size().reset_index(name='counts')
#plot
ax1 = counts.plot.scatter(x='frame', y='counts', c='DarkBlue', ylim=(0,600), title=name)
#ax1.set_yscale('log')
#ax1.set_xscale('log')


#count number of localizations / frame
photons = locs.groupby(['frame']).sum()['intensity [photon]'].reset_index(name='photons')
#plot
ax2 = photons.plot.scatter(x='frame', y='photons', c='DarkBlue',ylim=(0,1400000),  title=name)



#filter dataframe by frame
#locs_filtered = locs.loc[locs['frame'] <=25000]
#savePath = r"D:\data\2019-05-24\fromKestrel\20190524_Chris_Triangles_ANDJRectangle_ASCII_SRC-locs_fixed_frames1-250000.csv"
#locs_filtered.to_csv(savePath, index=False)