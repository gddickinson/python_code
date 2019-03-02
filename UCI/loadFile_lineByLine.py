# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 10:05:25 2015

@author: George
"""
import numpy as np
FileName = "J:\\WORK_IN_PROGRESS\\Files for cluster analysis\\IP3R1\\UCDavis_Primary_labelled_Ab\\140107_UCDavis_primary_1-8000_dilution_001_result"
output = FileName+'2'
f = open(FileName+'.txt')
i = 0
ans = []

for line in iter(f):
    ans.append(line)
    i+=1
    print (i)
    if i > 500000:
        break
f.close()

outF = open(output+'.txt', 'w')
for line in ans:
    outF.write(line)
    outF.write(',')
outF.close()
print("Result File Saved")