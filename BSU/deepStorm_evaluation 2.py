# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 09:52:08 2020

@author: g_dic
"""

import pandas as pd
import glob
import matplotlib.pyplot as plt
import os

#get thunderstorm locs
filePath = r"C:\Users\g_dic\Google Drive\deepSTORM_training\QC_data\2020-09-4_EdNAMfull3_nostrands_crop.csv"
name = os.path.basename(filePath)
locs = pd.read_csv(filePath)

columnNames = locs.columns.values.tolist()
print(columnNames)

#get deepstorm predicted locs
filePath2 = r"C:\Users\g_dic\Google Drive\deepSTORM_training\result\Localizations_2020-09-4_EdNAMfull3_nostrands_crop_avg.csv"
name2 = os.path.basename(filePath2)
locs_deepstorm = pd.read_csv(filePath2)

columnNames2 = locs_deepstorm.columns.values.tolist()
print(columnNames2)

#plot
ax = locs.plot.scatter(x='x [nm]', y='y [nm]', c='DarkBlue', s=3)
locs_deepstorm.plot.scatter(x='x [nm]', y='y [nm]', c='red', s=3, ax=ax)

#save thunderstorm/picasso compatible csv
# locs_deepstorm.rename(index=str, columns={'x [nm]': 'x_nm',
#                               'y [nm]': 'y_nm',
#                               'confidence [a.u]': 'uncertainty_xy_nm'}, inplace=True)

# locs_deepstorm['uncertainty_xy_nm'] = locs_deepstorm['uncertainty_xy_nm'] * 0.05292
# colsToAdd = ['sigma_nm','intensity_photon','offset_photon','bkgstd_photon']

# for name in colsToAdd:
#     locs_deepstorm[name]=0

# colNames3 = list(locs_deepstorm.columns) 

# savePath = filePath2.split('.')[0] + '_fixed.csv'
# locs_deepstorm.to_csv(savePath, index=False)

# print('Done')

