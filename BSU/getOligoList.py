# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 15:51:33 2019

@author: GEORGEDICKINSON
"""

import pandas as pd
import numpy as np


filename = r"C:\Users\georgedickinson\Desktop\bricks\oligos.txt"
savename = r"C:\Users\georgedickinson\Desktop\bricks\oligoMasterList_10x10x10.csv"
savename2 = r"C:\Users\georgedickinson\Desktop\bricks\cubeList.csv"
structureFile = r"C:\Users\georgedickinson\Desktop\bricks\structure1_list.csv"

df = pd.read_csv(filename, sep='\t', lineterminator='\r', header=None, names=['oligo'])


df2 = df.oligo.str.split("[",expand=True,)
df2 = df2.rename(columns={0: "oligo", 1: "voxel"})
df2 = df2.drop(df.index[-1])

df2['oligo'] = df2['oligo'].map(lambda x: x.lstrip('\n"'))
df2['voxel'] = df2.voxel.apply(lambda x: x.strip('"'))
df2['oligo'] = df2['oligo'].str.replace('\d+', '')
df2['oligo'] = df2['oligo'].str.replace(' ', '')

df2.to_csv(savename)

oligoList = np.loadtxt(structureFile,delimiter=',', dtype='int')

filteredDF = df2.iloc[oligoList]

filteredDF.to_csv(savename2)