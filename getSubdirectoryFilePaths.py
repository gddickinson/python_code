# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 20:39:37 2019

@author: George
"""

import os

dirName = r"C:\Users\George\Desktop\testRun\results\top"

listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk(dirName):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]

print(listOfFiles)