# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 10:48:14 2020

@author: GEORGEDICKINSON
"""

import os
from shutil import copyfile

folderPath = r"Y:\8_NAM (Nucleic-Acid Memory)_Sep2017_InProgress\11_Super-Resolution\George_D_DATA"
destinationPath = r"Y:\8_NAM (Nucleic-Acid Memory)_Sep2017_InProgress\11_Super-Resolution\All_Data"

os.chdir(folderPath)

fileList = []
destinationList = []

for root, dirs, files in os.walk(folderPath):
    for file in files:
        if file.endswith(".csv"):
             fileList.append(os.path.join(root, file))

for root, dirs, files in os.walk(destinationPath):
    for file in files:
        if file.endswith(".csv"):
             destinationList.append(os.path.join(root, file))


#fileList = fileList[80:] #filter
             
#print(fileList)

for file in fileList:
    src = file
    dst = os.path.join(destinationPath, file.split('\\')[-1])
    
    if dst in destinationList:
        print('skipping')
        pass
    else:
        print('copying to: ', dst)
        try:
            copyfile(src,dst)
            print('finished')
        except:
            print('failed: ', src)
    
print('done!')    