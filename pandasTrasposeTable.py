# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 14:28:10 2020

@author: g_dic
"""

import pandas as pd

filename = r"C:\Users\g_dic\OneDrive\Desktop\vegClass_2020\histo.txt"
savename = r"C:\Users\g_dic\OneDrive\Desktop\vegClass_2020\histo_transpose.txt"

df = pd.read_csv(filename)

df_T = df.transpose()

new_header = df_T. iloc[1]

df_T = df_T.iloc[2:]

df_T.columns = new_header

df_T['OBJECTID'] = df_T.index.str.extract('(\d+)', expand=False)

df_T = df_T.set_index('OBJECTID')

df_T = df_T.rename(columns={"NoData": "EXCLUDED",
                    "Cottonwood-Willow": "CW_W",
                    "Tamarisk": "TAM",
                    "Mesquite": "MQ",
                    "Other (sparse)": "SPARSE",
                    "Marsh-Herbaceous": "MARSH_H",
                    "Bare Ground": "BG",
                    "Water": "WATER",                     
                    "Other (Dense)": "DENSE"                      
                     })

df_T.to_csv(savename)
