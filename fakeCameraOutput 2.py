# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 10:00:55 2019

@author: George
"""
import os, time
import numpy as np
from flika.process.file_ import get_permutation_tuple
#from flika.utils.io import tifffile
import tifffile_local as tifffile

class Load_tiff ():
    """ load_tiff()
    This function loads tiff files from lightsheet experiments with multiple channels and volumes.

    """

    def __init__(self):
        pass
  
            
    def openTiff(self, filename):
        Tiff = tifffile.TiffFile(str(filename))
        A = Tiff.asarray()
        Tiff.close()
        axes = [tifffile.AXES_LABELS[ax] for ax in Tiff.series[0].axes]

        if set(axes) == set(['time', 'depth', 'height', 'width']):  # single channel, multi-volume
            target_axes = ['time', 'depth', 'width', 'height']
            perm = get_permutation_tuple(axes, target_axes)
            A = np.transpose(A, perm)
            nScans, nFrames, x, y = A.shape

            A = A.reshape(nScans*nFrames,x,y)
            #newWindow = Window(A,'Loaded Tiff')
            return A
            
        elif set(axes) == set(['series', 'height', 'width']):  # single channel, single-volume
            target_axes = ['series', 'width', 'height']
            perm = get_permutation_tuple(axes, target_axes)
            A = np.transpose(A, perm)
            nFrames, x, y = A.shape
            A = A.reshape(nFrames,x,y)
            #newWindow = Window(A,'Loaded Tiff')
            return A
            
        elif set(axes) == set(['time', 'height', 'width']):  # single channel, single-volume
            target_axes = ['time', 'width', 'height']
            perm = get_permutation_tuple(axes, target_axes)
            A = np.transpose(A, perm)
            nFrames, x, y = A.shape
            A = A.reshape(nFrames,x,y)
            #newWindow = Window(A,'Loaded Tiff')
            return A
            
        elif set(axes) == set(['time', 'depth', 'channel', 'height', 'width']):  # multi-channel, multi-volume
            target_axes = ['channel','time','depth', 'width', 'height']
            perm = get_permutation_tuple(axes, target_axes)
            A = np.transpose(A, perm)
            B = A[0]
            C = A[1]

            n1Scans, n1Frames, x1, y1 = B.shape
            n2Scans, n2Frames, x2, y2 = C.shape

            B = B.reshape(n1Scans*n1Frames,x1,y1)
            C = C.reshape(n2Scans*n2Frames,x2,y2)

            #channel_1 = Window(B,'Channel 1')
            #channel_2 = Window(C,'Channel 2')
            return B
            
        elif set(axes) == set(['depth', 'channel', 'height', 'width']):  # multi-channel, single volume
            target_axes = ['channel','depth', 'width', 'height']
            perm = get_permutation_tuple(axes, target_axes)
            A = np.transpose(A, perm)
            B = A[0]
            C = A[1]

            #channel_1 = Window(B,'Channel 1')
            #channel_2 = Window(C,'Channel 2')
            return B
        
load_tiff = Load_tiff()  

#1-colour
#filename = r"C:\Users\George\Desktop\UCI\testStacks\from_IanP\stackforGeorge_150slice_step2_1channel.tif"
filename = r"C:\Users\George\Desktop\UCI\testStacks\from_IanS\1color\200vol_22slicestep_100msecexp_MMStack_Pos0.ome.tif"
savepath = r"C:\Users\George\Desktop\testRun\george_1color"

#2-colour
#filename = r"C:\Users\George\Desktop\UCI\testStacks\from_IanS\2color\200vol_22slicestep_100msecexp_1\200vol_22slicestep_100msecexp_1_MMStack_Pos0.ome.tif"
#savepath = r"C:\Users\George\Desktop\testRun\george_2color"

img = load_tiff.openTiff(filename)
slices,x,y = img.shape


volumeSize = 200

for loop in np.arange(0,200):
    for i in np.arange(0,slices/volumeSize,dtype=int):
        vol = img[i*volumeSize:i*volumeSize+volumeSize,:,:]
        newFolder = r'\vol_' + str(i)
        newDirectory = savepath + newFolder
        os.mkdir(newDirectory)
        savefile = newDirectory + r"\vol_" + str(i) + ".tif"
        tifffile.imsave(savefile, vol)
        time.sleep(5)
        print(i)