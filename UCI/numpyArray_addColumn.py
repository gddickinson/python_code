# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 15:54:30 2015

@author: George
"""

import numpy as np
N = 10
a = np.random.rand(N,N)
b = np.zeros((N,N+1))
b[:,:-1] = a
