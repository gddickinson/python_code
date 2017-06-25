# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 13:41:25 2017

@author: George
"""

import os
import sys
import glob
import numpy as np

fileList = []
codeList = []
numberFiles = []

path = r'C:\Users\George\Dropbox\LCR_webpages\mass_download\Reports'
output = path + r'\fileList_result.txt'
output2 = path + r'\codeList_result.txt'
path = path + r'\**\*.pdf'

for filename in glob.iglob(path, recursive=True):
    fileList.append(str(os.path.split(filename)[1]))


for file in fileList:
    if file.split("_")[0] not in codeList:
        codeList.append(file.split("_")[0])
    

np.savetxt(output, fileList, delimiter=',', fmt="%s")
np.savetxt(output2, codeList, delimiter=',', fmt="%s")