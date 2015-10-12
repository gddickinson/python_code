# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 12:17:25 2015

@author: george
"""

def selSort(L):
    for i in range(len(L) - 1):
        minIndx = i
        minVal = L[i]
        j = i+1
        while j < len(L):
            if minVal > L[j]:
                minIndx = j
                minVal = L[j]
            j += 1
        if minIndx != i:
            temp = L[i]
            L[i] = L[minIndx]
            L[minIndx] = temp
            print L
    return L

def newSort(L):
    for i in range(len(L) - 1):
        j=i+1
        while j < len(L):
            if L[i] > L[j]:
                temp = L[i]
                L[i] = L[j]
                L[j] = temp
            j += 1
            print L
    return L

def mySort(L):
    clear = False
    while not clear:
        clear = True
        for j in range(1, len(L)):
            if L[j-1] > L[j]:
                clear = False
                temp = L[j]
                L[j] = L[j-1]
                L[j-1] = temp
        print L
    return L

L = [7,3,9,1,5,2,8,10,34,22,77,3,12,765,3,1,88,4,99,678,43,2]
print selSort(L)
#print newSort(L)
#print mySort(L)