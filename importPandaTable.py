# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 11:17:37 2020

@author: g_dic
"""


import pandas as pd
import numpy as np
import h5py


filePath =r"C:\Users\g_dic\Documents\Ian_S\george_simple_export.txt"
df = pd.read_csv(filePath, sep='\t', skiprows=[0],  encoding='UTF-16')

colNames = list(df.columns)
print(colNames) 

filePath2 =r"C:\Users\g_dic\Documents\Ian_S\george_STORM_export.txt"
df2 = pd.read_csv(filePath2, sep='\t')

colNames2 = list(df2.columns)
print(colNames2) 

df.head(2)