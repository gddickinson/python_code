# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 19:18:31 2017

@author: George
"""
import numpy as np

layer_dims = np.array([4,3,2,1])
layers = np.array([1,1,1,1])
parameter = {'W':5,'b':1}

for i in range(1, int(len(layer_dims)/2)):
    parameter['W' + str(i)] = np.random.randn(layers[i], layers[i-1]) * 0.01
    parameter['b' + str(i)] = np.random.randn(layers[i], 1) * 0.01
    