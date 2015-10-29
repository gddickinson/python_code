# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 20:05:39 2015

@author: robot
"""
import pylab
import random
def dist1():
    return random.random() * 2 - 1

def dist2():
    if random.random() > 0.5:
        return random.random()
    else:
        return random.random() - 1 

x1 = []
x2 = []
for i in range(10000):
    x1.append(dist1())
    x2.append(dist2())

pylab.plt.figure('Figure1')
pylab.plt.subplot(211)
fig1 = pylab.hist(x1)
pylab.plt.subplot(212)
fig2 = pylab.hist(x2)    