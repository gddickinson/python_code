# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 17:42:56 2018

@author: George
"""
from __future__ import print_function
import numpy as np
from numpy import moveaxis
#from scipy.ndimage.interpolation import zoom
from skimage.transform import rescale
from skimage import transform as tf
from matplotlib import pyplot as plt
import tifffile
from scipy import ndimage

fileName = r'C:\Users\George\Dropbox\UCI\lightSheet\testFrame.tif'
#fileName = r'C:\Users\George\Dropbox\UCI\lightSheet\testforGeorge.tif'

Tiff = tifffile.TiffFile(fileName)
A = Tiff.asarray()
Tiff.close()

#A = A.swapaxes(0,1)

def get_transformation_matrix(theta=45):
    """
    theta is the angle of the light sheet
    Look at the pdf in this folder.
    """

    theta = theta/360 * 2 * np.pi # in radians
    hx = np.tan(theta)

    S = np.array([[1, hx, 0],
                  [0, 1, 0],
                  [0, 0, 1]])
    #S_inv = np.linalg.inv(S)
    #old_coords = np.array([[2, 2, 1], [6, 6, 1]]).T
    #new_coords = np.matmul(S, old_coords)
    #recovered_coords = np.matmul(S_inv, new_coords)
    #print('new coords: ', new_coords)
    #print('recovered coords: ', recovered_coords)
    return S

tForm = get_transformation_matrix(30)

B = tf.warp(A, tForm)

plt.imshow(A)
plt.figure()
plt.imshow(B)
plt.show()