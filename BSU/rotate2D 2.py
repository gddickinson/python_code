# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 17:01:00 2019

@author: GEORGEDICKINSON
"""

from __future__ import division                 #to avoid integer devision problem
import scipy
import pylab
import numpy as np


#just for fun making further development easier and with joy
pi     = scipy.pi
dot    = scipy.dot
sin    = scipy.sin
cos    = scipy.cos
ar     = scipy.array
rand   = scipy.rand
arange = scipy.arange
plot   = pylab.plot
show   = pylab.show
axis   = pylab.axis
grid   = pylab.grid
title  = pylab.title
rad    = lambda ang: ang*pi/180                 #lovely lambda: degree to radian

#the function
def Rotate2D(pts,cnt,ang=pi/4):
    '''pts = {} Rotates points(nx2) about center cnt(2) by angle ang(1) in radian'''
    return (dot(pts-cnt,ar([[cos(ang),sin(ang)],[-sin(ang),cos(ang)]]))+cnt).T

#the code for test
pts = ar([[0,0],[1,0],[1,1],[0.5,1.5],[0,1]])
plot(*pts.T,lw=5,color='k')                     #points (poly) to be rotated
for ang in arange(0,2*pi,pi/8):
    ots = Rotate2D(pts,ar([0.5,0.5]),ang)       #the results
    plot(*ots)
axis('image')
grid(True)
title('Rotate2D about a point')
show()



regressionLine = [66.64695071191093,
 62.49020295074318,
 55.991029473301936,
 66.27544348628739,
 60.60680008238775,
 55.73750674293719]

xs = [29.248, 53.753, 92.068, 31.438, 64.856, 93.562]

pts = np.array([list(zip(regressionLine,xs))])


pts = ar([[0,0],[1,0],[1,1],[0.5,1.5],[0,1]])
plot(*pts,lw=5,color='k')  

for ang in arange(0,2*pi,pi/8):
    ots = Rotate2D(pts,ar([60.820955384687515,61.2913222412614]),ang)       #the results
    plot(*ots)

ots = Rotate2D(pts,ar([60.820955384687515,61.2913222412614]),(90*pi/180))  
plot(*ots)


