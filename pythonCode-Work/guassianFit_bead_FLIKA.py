# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 14:21:04 2016

@author: George
"""


import os, sys
import numpy

path_to_github = 'C:\\Users\\George\\Documents\\GitHub'

sys.path.insert(1,os.path.join(path_to_github,'Flika'));
from FLIKA import *
#app = QApplication(sys.argv); initializeMainGui()


from plugins.detect_puffs.gaussianFitting import fitGaussian

# cutout bead 
# subtract background
I_whole=g.m.currentWindow.image

xorigin=14
yorigin=6
sigma=2
amplitude=1000
p0=[xorigin, yorigin, sigma,amplitude]
bounds=[(xorigin-5,xorigin+5), (yorigin-5,yorigin+5),(sigma-1, sigma+2), (amplitude-500, amplitude+500)]


answer = []

for i in range(len(I_whole)):
    I=I_whole[i]
    p, I_fit, I_fit = fitGaussian(I, p0, bounds)
    answer.append(p)

filename = 'J:\\WORK_IN_PROGRESS\\CellLights_AND_FIXATION\\cellLights_beads_100nm_result.txt'
#np.savetxt(filename, answer, delimiter=',')
#print("Result File Saved")