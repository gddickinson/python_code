# -*- coding: utf-8 -*-
"""
Created on Thu May 30 11:01:24 2019

@author: GEORGEDICKINSON
"""

import pandas as pd

#open picasso hdf5 file as DF
filePath = r"D:\data\2019-05-24\fromKestrel\20190524_Chris_Triangles_ANDJRectangle_ASCII_SRC-locs_fixed_frames1-25000_locs_rectangles-picked_avg.hdf5"

locs = pd.read_hdf(filePath, '/locs')
headers = locs.dtypes.index