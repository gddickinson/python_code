# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 12:21:52 2019

@author: GEORGEDICKINSON
"""

import h5py

filePath = r"D:\data\2019-05-29\20190529_FlowCell_Chris_Triangles_ANDJRectangle_ASCII__300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_12mM_PCD_TROLOX_1mM_11_27_40-raw-locs_fixed_frames1-35000_centerSection_locs_render_DRIFT-4_picked_FOR-FILTERING.hdf5"

filePath2 = filePath.split('.')[0] + '_filtered.hdf5'

#read file
f = h5py.File(filePath, 'r')

#see what data sets are stored in the file (file acts like python dict)
keys = list(f.keys())
print(keys)

#see what is in the dataset
dset = f[keys[0]]

print(dset.shape)
print(dset.dtype)


#read file2
f2 = h5py.File(filePath2, 'r')

#see what data sets are stored in the file (file acts like python dict)
keys2 = list(f2.keys())
print(keys2)

#see what is in the dataset
dset2 = f2[keys2[0]]

print(dset2.shape)
print(dset2.dtype)