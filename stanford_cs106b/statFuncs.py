# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 19:21:40 2015

@author: robot
"""

def Mean(X):
    mean = sum(X)/float(len(X))
    return mean

def stDev(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    return (tot/len(X))**0.5


def coefficVar(X):
    return stDev(X)/Mean(X)
    

X = [10, 4, 12, 15, 20, 5] 

print(Mean(X), stDev(X), coefficVar(X))