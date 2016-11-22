# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 14:52:51 2016

@author: george
"""
from robot import *
from math import *
from matrix import *
import random
import matplotlib.pyplot as plt

def kalman_filter(x, P):
    for n in range(len(measurements)):
        
        # measurement update
        y = matrix([[float(measurements[n])]]) - H*x
        S = H* P *H.transpose() + R
        K = P*H.transpose()*S.inverse() #Kalman gain matrix
        x = x + (K*y)
        P = (I-K*H)*P 
        
        # prediction
        x = F*x+u
        P = F*P*F.transpose()
        
    return x,P


def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

############################################
### use the code below to test your filter!
############################################


x = (3.2618187593136714, 4.229518090705041, 4.970144154070997, 5.4584758171066685, 5.677883530716649, 5.620895628364498, 5.289452764715364, 4.694841828968918, 3.857311583384793, 2.8053831159695455)
y = (5.248776670511476,6.394882252046046,7.699287493626686,9.117572439213015,10.601439096028392,12.10035616477686,13.563279822435065,14.940391958424991,16.18479667061946,17.25411724904363)


measurements = [3.2618187593136714, 4.229518090705041]#, 4.970144154070997, 5.4584758171066685, 5.677883530716649, 5.620895628364498, 5.289452764715364, 4.694841828968918, 3.857311583384793, 2.8053831159695455]
measurements = [5.248776670511476, 6.394882252046046]


dt = 1


x = matrix([[0.], [0.]]) # initial state (location and velocity)
P = matrix([[1000., 0.], [0., 1000.]]) # initial uncertainty
u = matrix([[0.], [0.]]) # external motion
F = matrix([[1., dt], [0, 1.]]) # next state function
H = matrix([[1., 0.]]) # measurement function
R = matrix([[1.]]) # measurement uncertainty
I = matrix([[1., 0.], [0., 1.]]) # identity matrix

result = (kalman_filter(x, P))