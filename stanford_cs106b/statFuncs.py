# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 19:21:40 2015

@author: robot
"""

def Mean(X):
    mean = sum(X)/float(len(X))
    return mean

def stDev(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    return (tot/len(X))**0.5


def coefficVar(X):
    return stDev(X)/Mean(X)
    
def possible_mean(L):
    return sum(L)/len(L)

def possible_variance(L):
    mu = possible_mean(L)
    temp = 0
    for e in L:
        temp += (e-mu)**2
    return temp / len(L)



A = [0,1,2,3,4,5,6,7,8]
B = [5,10,10,10,15]
C = [0,1,2,4,6,8]
D = [6,7,11,12,13,15]
E = [9,0,0,3,3,3,6,6]

print('A', Mean(A), stDev(A), coefficVar(A))
print('B', Mean(B), stDev(B), coefficVar(B))
print('C', Mean(C), stDev(C), coefficVar(C))
print('D', Mean(D), stDev(D), coefficVar(D))
print('E', Mean(E), stDev(E), coefficVar(E))

print('A', possible_mean(A), possible_variance(A))
print('B', possible_mean(B), possible_variance(B))
print('C', possible_mean(C), possible_variance(C))
print('D', possible_mean(D), possible_variance(D))
print('E', possible_mean(E), possible_variance(E))