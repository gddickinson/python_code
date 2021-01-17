# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 10:29:16 2018

@author: George
"""
import re
import numpy as np

fileName = r"C:\Users\George\Desktop\CEM_forSearch\searchDoc.txt"
saveFile = r"C:\Users\George\Desktop\CEM_forSearch\result.txt"

searchFile = open(fileName, "r")
text = searchFile.read()
searchFile.close()

#find all occurences of text within parentheses
result = re.findall('\(.*?\)',text)
resultClipped = []

#remove numbers and correct unicode problem
for row in result:
    if re.search('\d+',row) and len(row) > 4:
        row = row.encode('ascii', 'replace').decode('ascii')
        resultClipped.append(row)
    

np.savetxt(saveFile, resultClipped,fmt ="%s")


