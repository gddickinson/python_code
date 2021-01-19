# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 13:42:43 2015

@author: George
"""
from __future__ import (absolute_import, division,print_function, unicode_literals)
from future.builtins import (bytes, dict, int, list, object, range, str, ascii, chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)

from sklearn.neighbors.kde import KernelDensity
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import win32com.client
from win32com.client import constants

X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X)
kde.score_samples(X)

plt.scatter(X[:,0],X[:,1])