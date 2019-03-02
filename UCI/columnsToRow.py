# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 12:07:15 2015

@author: George
"""
import pandas
import numpy as np

path = "J:\\WORK\\Calcium_STORM\\150317\\"
file = "test"
filename = path + file + ".txt"
output = path + file + "_result.txt"

df = pandas.read_csv(filename)
ans=[]
for col in df.columns:
    vals=df[col].dropna()
    ans.extend(list(vals))
ans=np.array(ans,dtype=np.float)

np.savetxt(output, np.transpose(ans), delimiter=',')