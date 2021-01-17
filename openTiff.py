# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 12:47:58 2019

@author: George
"""

import numpy as np
import tifffile
import os
from os import listdir
from os.path import expanduser, isfile, join
from matplotlib import pyplot as plt

volume_path = r'C:\Users\George\Dropbox\UCI\shared\volume\light_sheet_vols0'

def get_permutation_tuple(src, dst):
    """get_permtation_tuple(src, dst)

    Parameters:
        src (list): The original ordering of the axes in the tiff.
        dst (list): The desired ordering of the axes in the tiff.

    Returns:
        result (tuple): The required permutation so the axes are ordered as desired.
    """
    result = []
    for i in dst:
        result.append(src.index(i))
    result = tuple(result)
    return result

def openTiff(filename):
    Tiff = tifffile.TiffFile(str(filename))
    A = Tiff.asarray()
    Tiff.close()
    axes = [tifffile.AXES_LABELS[ax] for ax in Tiff.series[0].axes]
    if set(axes) == set(['series', 'height', 'width']):  # single channel, multi-volume
        target_axes = ['series', 'width', 'height']
        perm = get_permutation_tuple(axes, target_axes)
        A = np.transpose(A, perm)
    return A

A_list = []

#get volume files in folder
vols = [f for f in listdir(volume_path) if isfile(join(volume_path, f))]
#add volumes to volume list
for i in range(len(vols)):
    file = join(volume_path, vols[i])
    A_list.append(openTiff(file))
    
filename =r'C:\Users\George\Desktop\UCI\stackforGeorge_150slice_step2.tif'
original = openTiff(filename)

test = A_list[0]

test1 = A_list[0][0,::]
test2 = A_list[0][10,::]

newdisplayImage = A_list[0][0,::]

for i in np.arange(1,len(A_list)):
    newdisplayImage = np.dstack((newdisplayImage, A_list[i][0,::]))






#plt.figure(1)
#fig1 = plt.imshow(test1)
#plt.figure(2)
#fig2 = plt.imshow(test2)
#plt.show()










