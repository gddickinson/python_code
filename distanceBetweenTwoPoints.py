# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 13:35:02 2016

@author: George
"""

import math


result = []
#inputXY1 =[(0,	0), (-640, -1600), (-640, -2560), (-1600, -3840), (-2080, -4800), (-2080, -6080), (-1920, -7840)]
inputXY2 = [(0, 0), (0, -2), (1, -3), (0, -5), (0, -8), (0, -10)]
try:
    for i in range(len(inputXY2)):
        x1 = inputXY2[i][0]
        y1 = inputXY2[i][1]
        x2 = inputXY2[i+1][0]
        y2 = inputXY2[i+1][1]
        dist = math.hypot(x2 - x1, y2 - y1)
        print dist
        result.append(dist)
except:
    pass
print result

