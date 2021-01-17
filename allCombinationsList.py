# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 07:20:18 2019

@author: George
"""

# A Python program to print all  
# permutations using library function 
from itertools import permutations 
  
# Get all permutations 
perm = permutations([0, 1, 2, 3]) 
  
# Print the obtained permutations 
for i in list(perm): 
    i = str(i).replace('(','[').replace(')',']')
    print ("'" +i+"': "+i+',')