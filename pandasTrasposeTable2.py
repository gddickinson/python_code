# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 14:28:10 2020

@author: g_dic
"""

import pandas as pd

filename = r"C:\Users\g_dic\Dropbox\SoundScience\vegClassification_FINAL\vegClass_2020\histo_lidar.txt"
savename = r"C:\Users\g_dic\Dropbox\SoundScience\vegClassification_FINAL\vegClass_2020\histo_lidar_transpose.txt"

df = pd.read_csv(filename)

df_T = df.transpose()

new_header = df_T. iloc[1]

df_T = df_T.iloc[2:]

df_T.columns = new_header

df_T['OBJECTID'] = df_T.index.str.extract('(\d+)', expand=False)

df_T = df_T.set_index('OBJECTID')


df_T.to_csv(savename)
