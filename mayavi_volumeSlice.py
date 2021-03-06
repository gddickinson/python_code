# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 17:15:39 2019

@author: George
"""

import numpy
from mayavi.mlab import *

def test_volume_slice():
    x, y, z = np.ogrid[-5:5:64j, -5:5:64j, -5:5:64j]

    scalars = x * x * 0.5 + y * y + z * z * 2.0

    obj = volume_slice(scalars, plane_orientation='x_axes')
    return obj