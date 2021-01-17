# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 17:59:54 2018

@author: George
"""

import os, glob

path = r'C:\Users\George\Desktop\idahoBuildings'

os.chdir(path)

fileList = []
for file in glob.glob("*.jpg"):
    fileList.append(file)


for i in range(len(fileList)):
    os.rename(fileList[i], str(i) + '_' + fileList[i].split('_')[0] + '.jpg')
    print(i)