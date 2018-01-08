# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 11:56:30 2017

@author: George
"""

import os
import sys
import numpy as np
from PyPDF2 import PdfFileReader
from collections import Counter
from collections import OrderedDict
from matplotlib import pyplot as plt
import glob
from collections import Counter
from shutil import copy2

#path = r"/Users/george/Dropbox/SoundScience/LCR_webpages/CRAB-CRTR_powerpoints/CRTR"
path = r"C:\Users\George\Dropbox\SoundScience\LCR_webpages\CRAB-CRTR_powerpoints\CRAB"
#test path
#path = r"/Users/george/Desktop/testing"
files_in_dir = os.listdir(path)

def addYearPDF(filename):
    
    f = open(filename, 'rb')
    reader = PdfFileReader(f)
    #pages = reader.numPages
    docInfo = reader.getDocumentInfo()
    title = docInfo.title
    creationDate = docInfo.get('/CreationDate')
    modDate = docInfo.get('/ModDate')
    print(title)
    #print(modDate)
    year = creationDate[2:6]
    print(year)
    #print(pages)    

    f.close()
    
    return year

i = 0
while i < 1:    
    for file in files_in_dir:
        try:
            print(file)
            year = addYearPDF(os.path.join(path,file))

            #newFileName = titleTags+'--'+bodyTags+'---'+file
            newFileName = 'CRAB_'+year+'---'+file
            resultsPath = os.path.join(path,"results")
            copy2(os.path.join(path,file), os.path.join(resultsPath,newFileName))

        except:
            print('miss')
            try:
                resultsPath = os.path.join(path,"results")
                copy2(os.path.join(path,file), os.path.join(resultsPath,file))
            except:
                print('write error')
            
        i+=1

