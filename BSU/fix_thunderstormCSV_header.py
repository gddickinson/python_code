# -*- coding: utf-8 -*-
"""
Created on Sun May  5 15:43:13 2019

@author: George
"""

import pandas as pd


filePath =r"Y:\8_NAM (Nucleic-Acid Memory)_Sep2017_InProgress\11_Super-Resolution\George_D_DATA\2020-02-11\2020-01-31_dNAM_LS_mhPS37_repreat-locs.csv"
savePath = filePath.split('.')[0] + '_fixed.csv'

df = pd.read_csv(filePath)

colNames = list(df.columns) 
print(colNames)

df.rename(index=str, columns={"uncertainty [nm]": "uncertainty_xy [nm]"}, inplace=True)

colNames2 = list(df.columns) 


df.to_csv(savePath, index=False)

print('Done')