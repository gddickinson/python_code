# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 23:00:26 2015

@author: george
"""

import scipy as sp
import numpy as np
from matplotlib import pyplot as plt

data = sp.genfromtxt('sampleText.txt', delimiter=',')

print data

x= data[:,0]
y = data[:,1]
plt.plot(x,y)

