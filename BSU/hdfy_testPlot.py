# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 16:10:39 2019

@author: GEORGEDICKINSON
"""

import pandas as pd
from matplotlib import pyplot as plt

filePath = r"Y:\George_D_DATA\2019-09-13\fromIAPETUS\run2\20190913_All-Matrices_syn2_pure_Triangles_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_12mM_PCD_TROLOX_1mM_13_42_03_fixed_locs_render_DRIFT_3_filter_picked_manual_avg.hdf5"
#open picasso hdf5 file as DF
locs = pd.read_hdf(filePath, '/locs')

#check header names etc
headers = locs.dtypes.index
print(headers)
print(locs.shape)
print(locs.head(n=5))

#filter for one origami
groupNumber = 0
locsFiltered = locs[locs['group']==groupNumber]

fig, ax = plt.subplots()
ax.scatter(locsFiltered['x'],locsFiltered['y'], s=1, color='black')