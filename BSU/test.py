from __future__ import division                 #to avoid integer devision problem
import numpy as np
import math
import pylab

import glob
from flika import *
from flika.process.file_ import *
from flika.process.filters import *
from flika.window import *
from skimage.color import rgb2gray, label2rgb

start_flika()


#get all cropped tiff paths
path = r"C:\Users\georgedickinson\Documents\BSU_work\Brett - analysis for automation\tiffs\results\*.tif"
#path = r"C:\Users\George\Dropbox\BSU\brettsAnalysis\tiffs\results\*.tif"
fileList = glob.glob(path)

fileName= fileList[3]

#open file
file = open_file(fileName)
im = file.imageview.getProcessedImage()
gray_im = rgb2gray(im)

Window(gray_im)

thresholded = gray_im > 0.02

Window(thresholded)