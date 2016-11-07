# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 10:55:15 2016

@author: George
"""

a = [1,2,3,4,5]
b = [10,20,30,40,50]
c = [100,200,300,400,500]

test = list(map(lambda x,y,z: x+y+z, a,b,c))

test2 = list(zip(a,b))

print(test)
print(test2)