# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 13:55:57 2017

@author: George
"""

import numpy as np
from matplotlib import pyplot as plt

def getBeta1 ():
    r = np.random.rand()
    beta = 1-10**(- r - 1) 
    return beta

def getBeta2 ():
    r = np.random.rand()
    beta = 1-10**(- r + 1)   
    return beta

def getBeta3 ():
    r = np.random.rand()
    beta = r*0.09 + 0.9   
    return beta

def getBeta4 ():
    r = np.random.rand()
    beta = r*0.9 + 0.09 
    return beta


dist1 = []
dist2 = []
dist3 = []
dist4 = []

for i in range(10000):
    dist1.append(getBeta1())
    dist2.append(getBeta2())
    dist3.append(getBeta3())
    dist4.append(getBeta4())

     
fig1 =plt.figure(1)
plt.subplot(411)
plt.hist(dist1)
plt.subplot(412)
plt.hist(dist2)
plt.subplot(413)
plt.hist(dist3)    
plt.subplot(414)
plt.hist(dist4)  