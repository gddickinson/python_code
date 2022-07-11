# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 11:52:27 2019

@author: George
"""

import numpy as np

arr1 = np.zeros(100)
arr2 = np.ones(100)
arr_tuple = (arr1, arr2)
interleaved = np.vstack(arr_tuple).reshape((-1,), order='F')