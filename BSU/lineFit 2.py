# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 12:05:21 2019

@author: GEORGEDICKINSON
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
from statistics import mean

centList = [(29.24778761061947, 82.3598820058997),
 (53.75316455696203, 81.83544303797468),
 (92.0679012345679, 68.97736625514403)]



A = np.array(centList)
xs = A[:,0]
ys = A[:,1]


def best_fit_slope_and_intercept(xs,ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))
    
    b = mean(ys) - m*mean(xs)
    
    return m, b

m, b = best_fit_slope_and_intercept(xs,ys)

regression_line = [(m*x)+b for x in xs]

plt.scatter(xs,ys,color='#003F72')
plt.plot(xs, regression_line)
plt.show()
