# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 13:14:24 2019

@author: GEORGEDICKINSON
"""

import pandas as pd
import glob

path = r"C:\Users\georgedickinson\Desktop\forConcatonation\*.csv"
savePath = r"C:\Users\georgedickinson\Desktop\forConcatonation"

fileList = glob.glob(path)

for i in range(len(fileList)):
    filePath = fileList[i]
    locs = pd.read_csv(filePath)
    
    locs['x [nm]'] = locs['x [nm]'] + (i * 1000)
    
    saveName = savePath + '\\' + 'average_' + str(i) + '.csv'
    
    locs.to_csv(saveName, index=False)