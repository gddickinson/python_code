# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 19:26:22 2015

@author: robot
"""
import pylab
import random
def genEven():
    '''
    Returns a random even number x, where 0 <= x < 100
    '''
    evenNumber = 1
    while evenNumber%2 != 0:
        evenNumber = random.randint(0,100)
    
    return evenNumber

x = []
for i in range(1000000):
    x.append(genEven())

pylab.hist(x, bins=100)