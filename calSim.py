# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 18:44:07 2015

@author: robot
"""

import numpy as np

###make cytoplasm environment state,x,y,z
state = np.zeros(100)
x = y = z = np.arange(100)
cyto = np.vstack((state,x,y,z))

##Locate source###
source = 

