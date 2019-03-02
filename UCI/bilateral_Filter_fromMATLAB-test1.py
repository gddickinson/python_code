# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 16:17:57 2015

@author: George
"""
from __future__ import (absolute_import, division,print_function, unicode_literals)
import numpy as np
from scipy import stats
import matplotlib
from matplotlib import pyplot as plt
import math

filename="C:\\Users\\George\\Documents\\MATLAB\\pwctools\\singlePuff1.txt" 

y=np.loadtxt(filename,skiprows=0,usecols=(0,))
soft=1
beta=200.5
width=5
display=1
stoptol=1e-3
maxiter=50

y = np.array(y[:])
N = np.size(y, 0)

# Construct bilateral sequence kernel
w = np.zeros((N,N))
j = np.array(np.arange(1,N+1))
for i in range(N):
    w(i[:]).lvalue = (abs(i - j) <= width)
    

xold = y     # Initial guess using input signal
d = np.zeros((N, N))

if (display):
    if (soft):
        print('Soft kernel\\n')
    else:
        print('Hard kernel\\n')
        
    print('Kernel parameters beta=%7.2e, W=%7.2e\\n', beta, width)
    print('Iter# Change\\n')
        

# Iterate
iter = 1
gap = Inf
while (iter < maxiter):
    if (display):
        print('%5d %7.2e\\n', iter, gap)
        

# Compute pairwise distances between all samples
for i in range(N):
    d(i[:]).lvalue = 0.5 * (xold - xold(i)) **elpow** 2
    

# Compute kernels
if (soft):
    W = exp(-beta * d) *elmul* w                                        # Gaussian (soft) kernel
else:
    W = (d <= beta ** 2) *elmul* w                                        # Characteristic (hard) kernel
    

# Do kernel weighted mean shift update step
xnew = sum(W.cT * xold, 2) /eldiv/ sum(W, 2)

gap = sum((xold - xnew) **elpow** 2)

# Check for convergence
if (gap < stoptol):
    if (display):
        print('Converged in %d iterations\\n', iter)
        
        break
        

xold = xnew
iter = iter + 1


if (display):
    if (iter == maxiter):
        print('Maximum iterations exceeded\\n')
        
        

x = xnew