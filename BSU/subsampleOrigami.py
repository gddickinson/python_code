# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 16:06:24 2019

@author: GEORGEDICKINSON
"""

import numpy as np

#fname = r"C:\Users\georgedickinson\Desktop\golamsCode\NewWillsCode\ALL\20190913_10_38_52_substack_driftCorrected_bin_7668"
#fname = r"C:\Users\georgedickinson\Desktop\golamsCode\NewWillsCode\ALL\20190913_13_42_03_driftCorrected_bin_8015"
#fname = r"C:\Users\georgedickinson\Desktop\golamsCode\NewWillsCode\ALL\20191015_driftCorrected_bin_5860"
fname = r"C:\Users\georgedickinson\Desktop\golamsCode\NewWillsCode_output\syn2_threeImagingRuns\20190913_10_38_52_substack_driftCorrected_bin_7668_RUN1"
#fname = r"C:\Users\georgedickinson\Desktop\golamsCode\NewWillsCode_output\syn2_threeImagingRuns\20190913_13_42_03_driftCorrected_bin_8015_RUN2"
#fname = r"C:\Users\georgedickinson\Desktop\golamsCode\NewWillsCode_output\syn2_threeImagingRuns\20191015_driftCorrected_bin_5860_RUN3"

data = np.loadtxt(fname,dtype=str)

sampleSizes = [25,50,100,250,500,1000,1500,2000,2500,3000,3500,4000,5000]
#sampleSizes = [50,100,500,750,1000]
#sampleSizes = [250,1500,2000,2500,3000,3500,4000,5000]
sampleSizes = [750]

for size in sampleSizes:
    sample = np.random.choice(data,size=size,replace=False)
    sname = fname + '_' + str(size)
    np.savetxt(sname,sample,fmt='%s')