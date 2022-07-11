# -*- coding: utf-8 -*-
"""
Created on Wed May 22 15:35:36 2019

@author: GEORGEDICKINSON
"""
from __future__ import division 
import numpy as np


def triangleAngles(A,B,C):
    pi = 3.14159265358979
    
    def lengthSquare(p1,p2):
        #returns square of distance b/w two points
        xDiff = p1[0] - p2[0]
        yDiff = p1[1] - p2[1]
        return (xDiff*xDiff) + (yDiff*yDiff)   
        
    # Square of lengths a2, b2, c2 
    a2 = float(lengthSquare(B,C)) 
    b2 = float(lengthSquare(A,C)) 
    c2 = float(lengthSquare(A,B)) 
      
    #length of sides a, b, c 
    a = np.sqrt(a2) 
    b = np.sqrt(b2)
    c = np.sqrt(c2)
      
    #From Cosine law   
    alpha = np.arccos((b2 + c2 - a2)/(2*b*c)) 
    beta = np.arccos((a2 + c2 - b2)/(2*a*c)) 
    gamma = np.arccos((a2 + b2 - c2)/(2*a*b)) 
      
    # Converting to degree 
    alpha = alpha * 180 / pi 
    beta = beta * 180 / pi 
    gamma = gamma * 180 / pi 
    
    return (alpha, beta, gamma)

A = (0,0)
B = (0,1)
C = (1,0)

threeAngles = triangleAngles(A,B,C)
print(threeAngles)

print(np.sum(threeAngles))
