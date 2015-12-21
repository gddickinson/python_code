# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 22:10:27 2015

@author: george
"""

import random
import pylab

ans = []

for i in range(1000000):
    x = random.gauss( 50,10) + random.gauss( 70, 10 )
    ans.append(x)

pylab.hist(ans,500)