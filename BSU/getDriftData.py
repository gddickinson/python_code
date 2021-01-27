# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 14:24:38 2019

@author: GEORGEDICKINSON
"""

import pandas as pd


#get x y drift data
fileName = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-03-26\drift_plotData_004.csv"

driftData = pd.read_csv(fileName)

#get mean values for each fiduciary marker
meanData = driftData.groupby('X0').mean()

xDriftData = meanData['Y0'].tolist()
yDriftData = meanData['Y1'].tolist()




