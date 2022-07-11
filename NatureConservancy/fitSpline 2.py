# -*- coding: utf-8 -*-
"""
Created on Fri May 11 10:14:13 2018

@author: George
"""

import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

#raw data
x = [3454, 3433, 3559, 3903, 3970, 4282, 4649, 4901]
y = [12546611, 9481327, 7132256, 3900473, 3287550, 2418038, 2235571, 2105149]


def logistic4(x, A, B, C, D):
    """4PL lgoistic equation."""
    return ((A-D)/(1.0+((x/C)**B))) + D

def residuals(p, y, x):
    """Deviations of data from fitted 4PL curve"""
    A,B,C,D = p
    err = y-logistic4(x, A, B, C, D)
    return err

def peval(x, p):
    """Evaluated value at x with current parameters."""
    A,B,C,D = p
    return logistic4(x, A, B, C, D)


# Initial guess for parameters [min, slope, inflection, max]
p0 = [0.1, 1, 0.2, 1.2]

# Fit equation using least squares optimization
plsq = leastsq(residuals, p0, args=(y, x))

# Plot results
plt.plot(x,peval(x,plsq[0]),x,y,'o',x,y)
plt.title('Least-squares 4PL fit to noisy data')


plt.plot(x,y, '+')

