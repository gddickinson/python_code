# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 13:53:33 2015

@author: George
"""
from __future__ import (absolute_import, division,print_function, unicode_literals)
from future.builtins import (bytes, dict, int, list, object, range, str, ascii, chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
import matplotlib.cm as cm
import win32com.client
from win32com.client import constants
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn.neighbors import KernelDensity


filename = "C:\\Users\\George\\Desktop\\Amplitudes_001.txt"


data = np.loadtxt(filename,skiprows=0,usecols=(0,))
X = data[:,np.newaxis]


N = len(X)

X_plot = np.linspace(-5, 10, N)[:, np.newaxis]



fig, ax = plt.subplots()
#==============================================================================
# ax.fill(X_plot[:, 0], true_dens, fc='black', alpha=0.2,
#         label='input distribution')
#==============================================================================

for kernel in ['gaussian', 'tophat', 'epanechnikov']:
    kde = KernelDensity(kernel=kernel, bandwidth=0.2).fit(X)
    log_dens = kde.score_samples(X_plot)
    ax.plot(X_plot[:, 0], np.exp(log_dens), '-',
            label="kernel = '{0}'".format(kernel))

ax.text(6, 0.38, "N={0} points".format(N))

ax.legend(loc='upper right')
ax.plot(X[:, 0], -0.005 - 0.01 * np.random.random(X.shape[0]), '.')


ax.set_ylabel('Normalized Density')
ax.set_xlabel('Normalised Amplitude')
ax.set_title(filename)
ax.set_xlim(0, 4)
ax.set_ylim(-0.02, 1)
plt.show()