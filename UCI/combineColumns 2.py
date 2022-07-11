# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 12:13:15 2016

@author: George
"""
import numpy as np


filename = r"J:\WORK_IN_PROGRESS\STORM\CALCIUM_STORM\temp.txt"
output = r"J:\WORK_IN_PROGRESS\STORM\CALCIUM_STORM\result.txt"

data = np.fromstring(','.join(open(filename, 'r').read().splitlines()),sep=",")

np.savetxt(output, data, delimiter=',')