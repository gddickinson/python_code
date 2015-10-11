# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/george/.spyder2/.temp.py
"""
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from oct2py import octave

filename = "/home/george/Desktop/pwctools/singlePuff1.txt"
y = np.loadtxt(filename,skiprows=0,usecols=(0,))

octave.addpath('/home/george/Desktop/pwctools')

bilateralFilter = octave.pwc_bilateral(y,1,200.0,5)

fig = plt.plot(y)
fig2 = plt.plot(bilateralFilter)

