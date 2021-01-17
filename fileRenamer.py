#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 07:47:05 2017

@author: george
"""

import os
import sys
from shutil import copy2

path = r"/Users/george/Desktop/tarot/Colman-Smith/"

files_in_dir = os.listdir(path)

searchTerm = 'P.'
newTerm = '.'

for file in files_in_dir:
        try:
            if searchTerm in file:
                print(file)
                newFileName = file.replace(searchTerm,newTerm)
                newFileName = 'pe'+newFileName
                resultsPath = os.path.join(path,"results")
                copy2(os.path.join(path,file), os.path.join(resultsPath,newFileName))

        except:
            print('miss')
            #resultsPath = os.path.join(path,"results")
            #copy2(os.path.join(path,file), os.path.join(resultsPath,file))
            