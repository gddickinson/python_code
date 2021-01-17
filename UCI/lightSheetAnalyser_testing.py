# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 10:59:23 2018

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


#fileName = r'C:\Users\George\Dropbox\UCI\lightSheet\testFrame3.tif'
fileName = r'C:\Users\George\Dropbox\UCI\lightSheet\testforGeorge.tif'

Tiff = tifffile.TiffFile(fileName)
A = Tiff.asarray()
Tiff.close()

#A = A.swapaxes(1,2)

def get_transformation_matrix(theta=45):
    """
    theta is the angle of the light sheet
    Look at the pdf in this folder.
    """

    theta = theta/360 * 2 * np.pi # in radians
    hx = np.cos(theta)
    sy = np.sin(theta)

    S = np.array([[1, hx, 0],
                  [0, sy, 0],
                  [0, 0, 1]])
    #S_inv = np.linalg.inv(S)
    #old_coords = np.array([[2, 2, 1], [6, 6, 1]]).T
    #new_coords = np.matmul(S, old_coords)
    #recovered_coords = np.matmul(S_inv, new_coords)
    #print('new coords: ', new_coords)
    #print('recovered coords: ', recovered_coords)
    return S


def get_transformation_coordinates(I, theta):
    negative_new_max = False
    S = get_transformation_matrix(theta)
    S_inv = np.linalg.inv(S)
    mx, my = I.shape

    four_corners = np.matmul(S, np.array([[0, 0, mx, mx],
                                          [0, my, 0, my],
                                          [1, 1, 1, 1]]))[:-1,:]
    range_x = np.round(np.array([np.min(four_corners[0]), np.max(four_corners[0])])).astype(np.int)
    range_y = np.round(np.array([np.min(four_corners[1]), np.max(four_corners[1])])).astype(np.int)
    all_new_coords = np.meshgrid(np.arange(range_x[0], range_x[1]), np.arange(range_y[0], range_y[1]))
    new_coords = [all_new_coords[0].flatten(), all_new_coords[1].flatten()]
    new_homog_coords = np.stack([new_coords[0], new_coords[1], np.ones(len(new_coords[0]))])
    old_coords = np.matmul(S_inv, new_homog_coords)
    old_coords = old_coords[:-1, :]
    old_coords = old_coords
    old_coords[0, old_coords[0, :] >= mx-1] = -1
    old_coords[1, old_coords[1, :] >= my-1] = -1
    old_coords[0, old_coords[0, :] < 1] = -1
    old_coords[1, old_coords[1, :] < 1] = -1
    new_coords[0] -= np.min(new_coords[0])
    keep_coords = np.logical_not(np.logical_or(old_coords[0] == -1, old_coords[1] == -1))
    new_coords = [new_coords[0][keep_coords], new_coords[1][keep_coords]]
    old_coords = [old_coords[0][keep_coords], old_coords[1][keep_coords]]
    return old_coords, new_coords


def setup_test(A):
    ##A = g.win.image ##GD-EDIT (A inputed instead)
    mt, mx, my = A.shape
    nSteps = 128
    shift_factor = 2
    mv = mt // nSteps  # number of volumes
    A = A[:mv * nSteps]
    B = np.reshape(A, (mv, nSteps, mx, my))

def perform_shear_transform(A, shift_factor, interpolate, datatype, theta):
    A = moveaxis(A, [1, 3, 2, 0], [0, 1, 2, 3])
    m1, m2, m3, m4 = A.shape
    if interpolate:
        A_rescaled = np.zeros((m1*int(shift_factor), m2, m3, m4))
        for v in np.arange(m4):
            print('Upsampling Volume #{}/{}'.format(v+1, m4))
            A_rescaled[:, :, :, v] = rescale(A[:, :, :, v], (shift_factor, 1.), mode='constant', preserve_range=True)
    else:
        A_rescaled = np.repeat(A, shift_factor, axis=0)
    mx, my, mz, mt = A_rescaled.shape
    I = A_rescaled[:, :, 0, 0]
    old_coords, new_coords = get_transformation_coordinates(I, theta)
    old_coords = np.round(old_coords).astype(np.int)
    new_mx, new_my = np.max(new_coords[0]) + 1, np.max(new_coords[1]) + 1
    # I_transformed = np.zeros((new_mx, new_my))
    # I_transformed[new_coords[0], new_coords[1]] = I[old_coords[0], old_coords[1]]
    # Window(I_transformed)
    D = np.zeros((new_mx, new_my, mz, mt))
    D[new_coords[0], new_coords[1], :, :] = A_rescaled[old_coords[0], old_coords[1], :, :]
    E = moveaxis(D, [0, 1, 2, 3], [3, 1, 2, 0])
    E = np.flip(E, 1)
    #Window(E[0, :, :, :])
    E = E.astype(datatype)
    return E


theta = 30
#setup_test(A)
nSteps = 219
shift_factor = 100
interpolate = False

mt, mx, my = A.shape
mv = mt // nSteps  # number of volumes
A = A[:mv * nSteps]
B = np.reshape(A, (mv, nSteps, mx, my))

D = perform_shear_transform(B, shift_factor, interpolate, A.dtype, theta)

#plt.imshow(B[0][0])
#plt.imshow(D[0][0])
#plt.show()


class IndexTracker(object):
    def __init__(self, ax, X):
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')

        self.X = X
        rows, cols, self.slices = X.shape
        self.ind = self.slices//2

        self.im = ax.imshow(self.X[:, :, self.ind])
        self.update()

    def onscroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = np.clip(self.ind + 1, 0, self.slices - 1)
        else:
            self.ind = np.clip(self.ind - 1, 0, self.slices - 1)
        self.update()

    def update(self):
        self.im.set_data(self.X[:, :, self.ind])
        ax.set_ylabel('slice %s' % self.ind)
        self.im.axes.figure.canvas.draw()


fig, ax = plt.subplots(1, 1)

#X = np.random.rand(20, 20, 40)

tracker = IndexTracker(ax, D[0])


fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
plt.show()