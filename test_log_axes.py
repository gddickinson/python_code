# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 22:56:36 2015

@author: george
"""

from pylab import *
import matplotlib.pyplot  as pyplot
a = [ pow(10,i) for i in range(10) ]
fig = pyplot.figure()
ax = fig.add_subplot(2,1,1)

line, = ax.plot(a, color='blue', lw=2)

ax.set_yscale('log')

show()