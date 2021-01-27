# -*- coding: utf-8 -*-
"""
Created on Sun May  5 15:43:13 2019

@author: George
"""

import pandas as pd


filePath =r"C:\Users\g_dic\OneDrive\Desktop\BSU_DATA\2020-09-11_EdNAMfull4_W1_.csv"
savePath = filePath.split('.')[0] + '_fixed2.csv'

df = pd.read_csv(filePath)

colNames = list(df.columns)

print(colNames) 

df.rename(index=str, columns={'x [nm]': 'x_nm',
                              'y [nm]': 'y_nm',
                              'sigma [nm]': 'sigma_nm',
                              'intensity [photon]': 'intensity_photon',
                              'offset [photon]':'offset_photon',
                              'bkgstd [photon]':'bkgstd_photon',
                              'uncertainty [nm]': 'uncertainty_xy_nm'}, inplace=True)

colNames2 = list(df.columns) 

df.to_csv(savePath, index=False)

print('Done')