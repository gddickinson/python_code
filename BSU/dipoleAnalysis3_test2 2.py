# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 14:33:43 2019

@author: GEORGEDICKINSON
"""

from __future__ import division                 #to avoid integer devision problem
import numpy as np
from skimage.color import rgb2gray
from skimage.io import imread, imshow
from skimage.filters import gaussian, threshold_otsu
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

from flika import *
from flika.process.file_ import *
from flika.process.filters import *
from flika.window import *
start_flika()

###################     helper functions    ########################################
rad = lambda ang: ang*pi/180 

def best_fit_slope_and_intercept(xs,ys):
    '''returns regression line'''
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))  
    b = mean(ys) - m*mean(xs) 
    return m, b

def Rotate2D(pts,cnt,ang=pi/4):
    '''pts = {} Rotates points(nx2) about center cnt(2) by angle ang(1) in radian'''
    return (dot(pts-cnt,np.array([[cos(ang),sin(ang)],[-sin(ang),cos(ang)]]))+cnt).T

######################################################################################

#get all cropped tiff paths
path = r"C:\Users\georgedickinson\Documents\BSU_work\Brett - analysis for automation\tiffs\results\*.tif"
fileList = glob.glob(path)
#open file
file = open_file(fileName)

#laptop
#file = open_file(r'C:\Users\George\Dropbox\BSU\brettsAnalysis\tiffs\crop_5.tif')


#####################################################################################

####### Rotate cropped image so blue up #############################################

#create colour masks
blue_mask = file.imageview.getProcessedImage()[:,:,2] > 5
notBlue_mask = file.imageview.getProcessedImage()[:,:,2] < 5
red_mask = file.imageview.getProcessedImage()[:,:,0] > 5
red_mask = np.logical_and(red_mask,notBlue_mask)

#show mask
#Window(blue_mask, 'blue_mask') 
#Window(red_mask, 'red_mask')

#get blue blob props
blue_labels = measure.label(blue_mask)
blue_props = measure.regionprops(blue_labels)

blueCenteroids = []

for prop in blue_props:
	print('Blue-label: {} >> Object size: {}, Object position: {}'.format(prop.label, prop.area, prop.centroid))
	blueCenteroids.append(prop.centroid)
	#exportList.append([prop.label, prop.area, prop.centroid[0],prop.centroid[1]])

#get orange blob props
orange_labels = measure.label(red_mask)
orange_props = measure.regionprops(orange_labels)

orangeCenteroids = []

for prop in orange_props:
	print('Orange-label: {} >> Object size: {}, Object position: {}'.format(prop.label, prop.area, prop.centroid))
	orangeCenteroids.append(prop.centroid)
	#exportList.append([prop.label, prop.area, prop.centroid[0],prop.centroid[1]])

#rotate image so orange blobs above blue blobs
#fit line through all centeroids
allCenteroids = np.array(orangeCenteroids+blueCenteroids) 
allCenteroids_xs = allCenteroids[:,0]
allCenteroids_ys = allCenteroids[:,1]

#get slope + fit
allCenteroids_m, allCenteroids_b = best_fit_slope_and_intercept(allCenteroids_xs,allCenteroids_ys)

#generate regression line
regression_line = [(allCenteroids_m*allCenteroids_x)+allCenteroids_b for allCenteroids_x in allCenteroids_xs]

#get center point
mean_y = mean(regression_line)
mean_x = mean(allCenteroids_xs)

#generate intersect line
pts = np.array([list(zip(regression_line,allCenteroids_xs))])
intersectLine = Rotate2D(pts,np.array([mean_x,mean_y]),(90*pi/180))  

#rotate image to horizontal
rotatedImg = scipy.ndimage.rotate(file.imageview.getProcessedImage(),-regression_line[0])

#if blue blobs below then rotate 180 degrees
blue_mask_rotated = rotatedImg[:,:,2] > 5
aboveBlueCount = np.count_nonzero(blue_mask_rotated[0:int(rotatedImg.shape[0]/2),:])
belowBlueCount = np.count_nonzero(blue_mask_rotated[int(rotatedImg.shape[0]/2):-1,:])

if aboveBlueCount < belowBlueCount:
    rotatedImg = scipy.ndimage.rotate(file.imageview.getProcessedImage(),180-regression_line[0])
#Window(rotatedImg, 'rotated')


######################################################################################

######## Analyse blue up image ######################################################

#to avoid confusion - recalculate props for rotated image
#create colour masks
blue_mask_rotated = rotatedImg[:,:,2] > 5
notBlue_mask_rotated = rotatedImg[:,:,2] < 5
red_mask_rotated = rotatedImg[:,:,0] > 5
red_mask_rotated = np.logical_and(red_mask_rotated,notBlue_mask_rotated)

#show mask
#Window(blue_mask_rotated, 'blue_mask_rotated') 
#Window(red_mask_rotated, 'red_mask_rotated')

#create list to store all props
allProps = []

#get blue blob props
blue_labels_rotated = measure.label(blue_mask_rotated)
blue_props_rotated = measure.regionprops(blue_labels_rotated)

blueCenteroids_rotated = []

for prop in blue_props_rotated:
	print('Blue-label: {} >> Object size: {}, Object position: {}'.format(prop.label, prop.area, prop.centroid))
	blueCenteroids_rotated.append(prop.centroid)
	allProps.append(['blue', prop.label, prop.area, prop.centroid[0],prop.centroid[1]])

#get orange blob props
orange_labels_rotated = measure.label(red_mask_rotated)
orange_props_rotated = measure.regionprops(orange_labels_rotated)

orangeCenteroids_rotated = []

for prop in orange_props_rotated:
	print('Orange-label: {} >> Object size: {}, Object position: {}'.format(prop.label, prop.area, prop.centroid))
	orangeCenteroids.append(prop.centroid)
	allProps.append(['orange', prop.label, prop.area, prop.centroid[0],prop.centroid[1]])


#plot data
fig, ax = plt.subplots()
ax.imshow(rotatedImg)

for prop in blue_props_rotated:
    y0, x0 = prop.centroid
    ax.plot(x0, y0, '.g', markersize=15)

    minr, minc, maxr, maxc = prop.bbox
    bx = (minc, maxc, maxc, minc, minc)
    by = (minr, minr, maxr, maxr, minr)
    ax.plot(bx, by, '-b', linewidth=2.5)

for prop in orange_props_rotated:
    y0, x0 = prop.centroid
    ax.plot(x0, y0, '.g', markersize=15)

    minr, minc, maxr, maxc = prop.bbox
    bx = (minc, maxc, maxc, minc, minc)
    by = (minr, minr, maxr, maxr, minr)
    ax.plot(bx, by, '-y', linewidth=2.5)

#determine blob positions (1-6) for 'butter-side up' or 'butter-side down'
#create data frame for easier searching/filtering
allPropsDF = pd.DataFrame(allProps,columns=['colour','label','area','centeroid-y','centeroid-x'])
allPropsDF['position'] = 0

#p1
allPropsDF.at[allPropsDF['centeroid-x'].argmin(), 'position'] = 1
#p2
allPropsDF.at[allPropsDF[(allPropsDF.colour == 'blue') & (allPropsDF.position  == 0)]['centeroid-x'].argmin(), 'position'] = 2
#p3
allPropsDF.at[allPropsDF[(allPropsDF.colour == 'blue') & (allPropsDF.position  == 0)]['centeroid-x'].argmin(), 'position'] = 3
#p4
allPropsDF.at[allPropsDF['centeroid-x'].argmax(), 'position'] = 4
#p5
allPropsDF.at[allPropsDF[(allPropsDF.colour == 'orange') & (allPropsDF.position  == 0)]['centeroid-x'].argmax(), 'position'] = 5
#p6
allPropsDF.at[allPropsDF[(allPropsDF.colour == 'orange') & (allPropsDF.position  == 0)]['centeroid-x'].argmax(), 'position'] = 6

#line1
line1_start_x = float(allPropsDF[(allPropsDF.position  == 1)]['centeroid-x'])
line1_start_y = float(allPropsDF[(allPropsDF.position  == 1)]['centeroid-y'])

line1_end_x = float(allPropsDF[(allPropsDF.position  == 4)]['centeroid-x'])
line1_end_y = float(allPropsDF[(allPropsDF.position  == 4)]['centeroid-y'])

ax.plot([line1_start_x,line1_end_x], [line1_start_y,line1_end_y], '-g')

#line2
line2_start_x = float(allPropsDF[(allPropsDF.position  == 6)]['centeroid-x'])
line2_start_y = float(allPropsDF[(allPropsDF.position  == 6)]['centeroid-y'])

line2_end_x = float(allPropsDF[(allPropsDF.position  == 2)]['centeroid-x'])
line2_end_y = float(allPropsDF[(allPropsDF.position  == 2)]['centeroid-y'])

ax.plot([line2_start_x,line2_end_x], [line2_start_y,line2_end_y], '-g')

#line3
line3_start_x = float(allPropsDF[(allPropsDF.position  == 5)]['centeroid-x'])
line3_start_y = float(allPropsDF[(allPropsDF.position  == 5)]['centeroid-y'])

line3_end_x = float(allPropsDF[(allPropsDF.position  == 3)]['centeroid-x'])
line3_end_y = float(allPropsDF[(allPropsDF.position  == 3)]['centeroid-y'])

ax.plot([line3_start_x,line3_end_x], [line3_start_y,line3_end_y], '-g')



#ax.axis((0, 600, 600, 0))
plt.show()