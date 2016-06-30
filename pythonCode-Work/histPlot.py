# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 11:28:12 2016

@author: George
"""

from __future__ import (absolute_import, division,print_function, unicode_literals)
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

filename = r'J:\WORK_IN_PROGRESS\STORM\Files for cluster analysis\IP3R1\AB5882\130903_001\distances_allLocalizations\result_allDistances130903_SY5Y_IP3R1_561_3D_001_cropped_XY.txt'
    
data = np.loadtxt(filename,skiprows=1,usecols=(0,))

hist=plt.hist(data,500)

    