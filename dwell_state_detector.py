# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/george/.spyder2/.temp.py
"""

import numpy as np
from scipy import stats
import matplotlib
from matplotlib import pyplot as plt

pointsToFit = 5
noiseAmp = 3

#### fake data ########
n = 500
x = np.arange(1,n+1)
y = np.random.rand(n,)
y = y*noiseAmp
z = [100,20,50,30,10,60,100,30,100]
z1 = [0,25,20,10,5,7,15,2,0]

data = []
for i in range(len(z)):
    for t in range(z[i]):
        data.append(z1[i])
        
data = np.array(data)        
y = data + y

############################

fitsToKeep_X =[]
fitsToKeep_Y =[]

for i in range(np.size(x)-pointsToFit):
    x1 = x[i:i+pointsToFit]
    y1 = y[i:i+pointsToFit]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x1,y1)
    if slope < 1.1 and slope > -0.9 and std_err <0.2:
        fitsToKeep_X.append(x1)
        fitsToKeep_Y.append(y1)


fig1 = plt.plot(x,y)
#fig2 = plt.scatter(fitsToKeep_X,fitsToKeep_Y, c='r')