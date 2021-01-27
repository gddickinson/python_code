# -*- coding: utf-8 -*-
"""
Created on Sun May  5 15:43:13 2019

@author: George
"""

import pandas as pd


filePath =r"C:\Users\g_dic\OneDrive\Desktop\data_BSU\2020-08-28_EdNAMfull3_W1_locs.csv"
savePath = filePath.split('.')[0] + '_fixed.csv'

df = pd.read_csv(filePath)

colNames = list(df.columns)

print(colNames) 

df.rename(index=str, columns={'x [nm]': 'x_nm [nm]',
                              'y [nm]': 'y_nm [nm]',
                              'sigma [nm]': 'sigma_nm [nm]',
                              'intensity [photon]': 'intensity_photon [photon]',
                              'offset [photon]':'offset_photon [photon]',
                              'bkgstd [photon]':'bkgstd_photon [photon]',
                              'uncertainty [nm]': 'uncertainty_xy_nm [nm]'}, inplace=True)

colNames2 = list(df.columns) 

df.to_csv(savePath, index=False)

print('Done')