# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 17:23:42 2016

@author: George
"""

from math import *
import numpy as np
import matplotlib.pyplot as plt

def pdf(mu, sigma2, x):
    #probability density function
    #mu = mean, sigma2 = variance
    ans = 1/sqrt(2.*pi*sigma2) * exp(-.5*(x-mu)**2 / sigma2)
    return ans


# Write a program that will iteratively update and
# predict based on the location measurements 
# and inferred motions shown below. 

def update(mean1, var1, mean2, var2):
    #combine 2 gaussians
    new_mean = float(var2 * mean1 + var1 * mean2) / (var1 + var2)
    new_var = 1./(1./var1 + 1./var2)
    return [new_mean, new_var]

def predict(mean1, var1, mean2, var2):
    #add mean and variance from 2 gaussians
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]

measurements = [5., 6., 7., 9., 10.]
motion = [1., 1., 2., 1., 1.]
measurement_sig = 4.
motion_sig = 2.
mu = 0.
sig = 10000.

#Please print out ONLY the final values of the mean
#and the variance in a list [mu, sig]. 

# Insert code here

for i in range(len(measurements)):
     mu,sig = update (mu, sig, measurements[i], measurement_sig)
     mu,sig = predict(mu, sig, motion[i], motion_sig)

print ([mu, sig])


print(update(0,1,0,1))

