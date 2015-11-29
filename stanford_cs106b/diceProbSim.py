# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 15:18:49 2015

@author: george
"""
import random
import numpy as np


def prob(dice=6, number = 6, numberOfRoles=3, numberOfTrials=10000):
    ans =[]    
    for i in range(numberOfTrials):
        hits = 0
        for i in range(numberOfRoles):    
            roll = random.randint(1,dice)
            if roll == number:
                hits +=1
        ans.append(hits)

    probability = 0
    for i in range(len(ans)):
        #print (ans[i])
        if ans[i] >=2:
            probability +=1
            print(probability)
    return float(probability/numberOfTrials)
    
print prob()