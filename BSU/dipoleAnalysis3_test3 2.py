from __future__ import division                 #to avoid integer devision problem
import numpy as np
from skimage.color import rgb2gray, label2rgb
from skimage.io import imread, imshow
from skimage.filters import gaussian, threshold_otsu, sobel, threshold_adaptive
from skimage import measure
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import glob
from skimage.draw import ellipse
from skimage.transform import rotate
import math
from statistics import mean, median
from scipy import pi, dot, sin, cos
import pandas as pd
import scipy
from skimage import util, color
from skimage.morphology import watershed
from skimage.measure import label
from skimage.segmentation import slic, join_segmentations

from flika import *
from flika.process.file_ import *
from flika.process.filters import *
from flika.window import *
from scipy import ndimage
from skimage.segmentation import random_walker

from skimage import feature, measure

from skimage.feature import peak_local_max
from skimage import morphology
from skimage.morphology import disk
from scipy import ndimage as ndi
from matplotlib.colors import ListedColormap
start_flika()

def my_imshow(im, title=None, **kwargs):
    if 'cmap' not in kwargs:
        kwargs['cmap'] = 'gray'
    plt.figure()
    plt.imshow(im, interpolation='none', **kwargs)
    if title:
        plt.title(title)
    plt.axis('off')
    

#get all cropped tiff paths
path = r"C:\Users\georgedickinson\Documents\BSU_work\Brett - analysis for automation\tiffs\results\*.tif"
#path = r"C:\Users\George\Dropbox\BSU\brettsAnalysis\tiffs\results\*.tif"
fileList = glob.glob(path)

fileName= fileList[41]

#open file
file = open_file(fileName)
file = gaussian_blur(4, norm_edges=False, keepSourceWindow=False)

im = file.imageview.getProcessedImage()
gray_im = rgb2gray(im)

Window(gray_im)

#threshVal = threshold_otsu(gray_im)
#threshVal = 15
#thresholded = gray_im >= threshVal

thresholded = threshold_adaptive(gray_im, 35)

Window(thresholded)

no_small = morphology.remove_small_objects(thresholded, min_size=5)

blobs = morphology.binary_closing(no_small,disk(4))
plt.figure()
plt.imshow(blobs, cmap='gray', interpolation='none')
plt.title('closed blobs with small objects removed')
plt.axis('off')

im[blobs==False] = 0
gray_im[blobs==False] = 0


plt.figure()
plt.imshow(im, cmap='gray', interpolation='none')
plt.title('masked image')
plt.axis('off')

plt.figure()
plt.imshow(gray_im, cmap='gray', interpolation='none')
plt.title('masked grayscale image')
plt.axis('off')

distance_im = ndi.distance_transform_edt(blobs)

Window(distance_im)

def imshow_overlay(im, mask, alpha=0.5, color='red', **kwargs):
    """Show semi-transparent red mask over an image"""
    mask = mask > 0
    mask = np.ma.masked_where(~mask, mask)        
    plt.imshow(im, **kwargs)
    plt.imshow(mask, alpha=alpha, cmap=ListedColormap([color]))


peaks_im = feature.peak_local_max(distance_im, indices=False)
Window(peaks_im)
blurred_im = gaussian_blur(3, norm_edges=False, keepSourceWindow=False)
peaks_im = feature.peak_local_max(blurred_im.imageview.getProcessedImage(), indices=False)

plt.figure()
imshow_overlay(distance_im, peaks_im, alpha=1, cmap='gray')

markers_im = measure.label(peaks_im)

labels_rw = random_walker(blobs, markers_im)

labelled_blobs = morphology.watershed(-distance_im, markers_im, mask=blobs)
num_blobs = len(np.unique(labelled_blobs))-1  # subtract 1 b/c background is labelled 0
print ('number of coins: %i' % num_blobs)

my_imshow(labelled_blobs, 'labelled blobs', cmap='jet')

my_imshow(labels_rw, 'labelled blobs random walker', cmap='jet')


