# -*- coding: utf-8 -*-
"""
Created on Fri May 13 11:09:30 2016

@author: kyle
"""

from __future__ import (absolute_import, division,print_function)
import os, sys
from os import chdir
from os.path import expanduser, join
import bz2
if sys.version_info.major==2:
    import cPickle as pickle # pickle serializes python objects so they can be saved persistantly.  It converts a python object into a savable data structure
else:
    import pickle
chdir(join(expanduser('~'), 'Documents','GitHub','flika'))
from flika import *
from plugins.detect_puffs.threshold_cluster import threshold_cluster
import numpy as np
import pylab as plt

allPoints = []
chdir(join(expanduser('~'), 'Desktop'))

path = 'C:\\Users\\George\\Desktop\\Nocodazole\\flika_files\\data\\'
savePath = 'C:\\Users\\George\\Desktop\\Nocodazole\\flika_files\\'
files = os.listdir(path)

for filename in files:
    #print(filename)
    fileName= path + filename
    with bz2.BZ2File(fileName, 'rb') as f:
        flika_file=pickle.load(f)
    
    puffs = [puff for puff in flika_file.puffs.values() if puff['trashed']==False]
    traces = []
    for puff in puffs:
        trace = puff['trace'] - puff['kinetics']['baseline']
        traces.append(trace)
    
    
    for trace in traces:
        for i in range(len(trace)):
            if trace[i] > 0.055:
            #if trace[i] > 0.2:                
                allPoints.append(trace[i])



outputFilename = savePath + "allPoints_over0-2_result.txt"
np.savetxt(outputFilename, np.transpose(allPoints), delimiter=',')
print("Result File Saved")

plt.hist(allPoints,10000)