# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:53:52 2015

@author: George
"""

from __future__ import (absolute_import, division,print_function, unicode_literals)
import numpy as np
from scipy import stats
import matplotlib
from matplotlib import pyplot as plt
import math

Fs=8000
f=500
sample = 100
x = np.arange(sample)
y = np.sin(2 * np.pi * f * x / Fs)

fig1 = plt.plot(x,y)