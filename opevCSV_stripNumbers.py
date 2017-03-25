# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 11:52:06 2017

@author: George
"""

import csv
import sys
import numpy as np
from PyPDF2 import PdfFileReader
from collections import Counter
from collections import OrderedDict

path = r'C:\Users\George\Desktop\report_no_dir'
filename = path + r'\words.csv'

result = path + r"\words.txt"

wordlist = []

words = np.loadtxt(filename, delimiter = ',', dtype = type(str))

for word in words:
    newword = (word.split("'")[1])
    wordlist.append(newword.split(' ')[0])


np.savetxt(result,wordlist,delimiter = ',', fmt="%s")