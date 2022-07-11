# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 11:11:09 2018

@author: George
"""

import re
import numpy as np
from tqdm import tqdm

fileName = r"C:\Users\George\Desktop\SoundScience\CEM_forSearch\searchDoc.txt"
saveFile = r"C:\Users\George\Desktop\SoundScience\CEM_forSearch\result.txt"

searchFile = open(fileName, "r")
text = searchFile.read()
searchFile.close()

#find all occurences of text within parentheses
result = re.findall('\(.*?\)',text)

result2 = re.findall(r'(.*?)\(.*?\)',text)

result3 = []

for i in tqdm(range(len(result))):
    if re.search('\d+',result[i]) and len(result[i]) > 4:
        result[i] = result[i].encode('ascii', 'replace').decode('ascii')
        result2[i] = result2[i].encode('ascii', 'replace').decode('ascii')
        try:
            result3.append([result2[i][-30:],result[i]])
        except:
            result3.append([result2[i],result[i]])
    
np.savetxt(saveFile, result3,fmt ="%s")
