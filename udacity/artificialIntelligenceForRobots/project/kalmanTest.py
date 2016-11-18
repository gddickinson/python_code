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

############################################
### use the code below to test your filter!
############################################

measurements = [3.2618187593136714, 4.229518090705041, 4.970144154070997, 5.4584758171066685, 5.677883530716649, 5.620895628364498, 5.289452764715364, 4.694841828968918, 3.857311583384793, 2.8053831159695455]
dt = 1


x = matrix([[0.], [0.]]) # initial state (location and velocity)
P = matrix([[1000., 0.], [0., 1000.]]) # initial uncertainty
u = matrix([[0.], [0.]]) # external motion
F = matrix([[1., dt], [0, 1.]]) # next state function
H = matrix([[1., 0.]]) # measurement function
R = matrix([[1.]]) # measurement uncertainty
I = matrix([[1., 0.], [0., 1.]]) # identity matrix

print (kalman_filter(x, P))