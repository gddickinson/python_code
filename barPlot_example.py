# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 14:03:11 2017

@author: George
"""

import matplotlib.pylab as py

# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

y = [3, 10, 7, 5, 3, 4.5, 6, 8.1]
N = len(y)
x = range(N)
width = 1/1.5
py.plt.bar(x, y, width, color="blue")


