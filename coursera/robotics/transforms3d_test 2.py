# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 12:31:51 2018

@author: George
"""

import numpy as np
import math
from transforms3d import euler

mat1 = np.array([[0.6927, -0.7146, 0.0978],
               [0.7165, 0.6973, 0.0198],
               [-0.0824, 0.0564, 0.995]])

mat2 = np.array([[0.2919, 0.643, -7.081],
               [-0.643, -0.4161, -0.643],
               [-0.7081, 0.643, 0.2919]])   


mat3 = np.array([[-1/3,2/3,-2/3],
                [2/3, -1/3, -2/3],
                [-2/3,-2/3,-1/3]])

ang1 = np.array([-1.7320508075688772/3, 1.7320508075688772/3,-1.7320508075688772/3])



euler.mat2euler(mat1,axes='rzyz')

test1 = euler.euler2mat(0.2,0.1,0.6,'rzyz') #this works!

test2 = euler.mat2euler(test1)

#4
u = np.array([math.sqrt(2)/2, 0, -math.sqrt(2)/2])
theta = 2

test3 = euler.axangle2euler(u,theta,'rzyz')
euler.euler2mat(test3[0],test3[1],test3[2],'rzyz')


u2 = np.array([math.sqrt(3)/3, math.sqrt(3)/3, -math.sqrt(3)/3])
theta2 = math.pi
test4 = euler.axangle2euler(u2,theta2,'rzyz')
euler.euler2mat(test4[0],test4[1],test4[2],'rzyz')



R1 = np.array([[0.3835,0.5730,0.9287],[0.5710,0.5919,-0.4119],[-1.3954,0.0217,1.1105]])
isRotationMatrix(R1)

R2 = np.array([[0.212,0.7743,0.5963],[0.212,-0.6321,0.7454],[0.954,-0.0316,-0.2981]])
isRotationMatrix(R2)

R3 = np.array([[math.cos(0.2),-math.sin(0.2)],[math.sin(0.2), math.cos(0.2)]])
isRotationMatrix(R3)

R4 = np.array([[math.sqrt(2)/2,0,math.sqrt(2)/2],[0,1,0],[-math.sqrt(2)/2,0,math.sqrt(2)/2]])
isRotationMatrix(R4)




