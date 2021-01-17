# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 11:32:30 2018

@author: George
"""

import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs
import numpy as np
#import h5py
import matplotlib.pyplot as plt
from PIL import Image
from scipy import ndimage
import copy
import glob, os
from math import sqrt
#from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray


resultsPath = r"C:\\Google Drive\\code\\python_code\\tensorFlow\\buildingIdentification\\results\\kerasModel_results\\"
#resultsPath = r"C:\\Google Drive\\code\\python_code\\tensorFlow\\buildingIdentification\\results\\test\\"
mapPath = r"C:\Users\George\Desktop\testImages\\test5.jpg"

def displayResults(folderPath):
    os.chdir(folderPath)
    fileList = []
    for file in glob.glob("*.txt"):
        fileList.append(file)


    array0 = np.genfromtxt(fileList[0],delimiter=",")
    for i in range(1,5):
        array = np.genfromtxt(fileList[i],delimiter=",")
        array0 = np.hstack((array,array0))

    array1 = np.genfromtxt(fileList[5],delimiter=",")
    for i in range(6,10):
        array = np.genfromtxt(fileList[i],delimiter=",")
        array1 = np.hstack((array1,array))

    array2 = np.genfromtxt(fileList[10],delimiter=",")
    for i in range(11,15):
        array = np.genfromtxt(fileList[i],delimiter=",")
        array2 = np.hstack((array2,array))

    array3 = np.genfromtxt(fileList[15],delimiter=",")
    for i in range(16,20):
        array = np.genfromtxt(fileList[i],delimiter=",")
        array3 = np.hstack((array3,array))

    array4 = np.genfromtxt(fileList[20],delimiter=",")
    for i in range(21,25):
        array = np.genfromtxt(fileList[i],delimiter=",")
        array4 = np.hstack((array4,array))

    imageArray = np.vstack((array0,array1,array2,array3,array4))
    
    img = Image.fromarray(imageArray)
#    plt.figure()
#    plt.imshow(img)
    return img, imageArray



##reduce map size for large map
#startX = 200
#endX = startX + 200
#startY = 600
#endY = startY + 200


### Uncomment to display results
piece, pieceArray = displayResults(resultsPath)

startX = 200
endX = startX + (6 * 100)
startY = 500
endY = startY + (6 * 100)

num_px = 100


#img = Image.open(mapPath)
mapArray = np.array(ndimage.imread(mapPath, flatten=False))
mapArray = mapArray[startX:endX,startY:endY]
img = Image.fromarray(mapArray)

img2 = copy.deepcopy(img)

img2.paste(piece,(int(num_px/2),int(num_px/2)))


fig1 = plt.figure(1)
plt.title("Input image")
plt.imshow(img)
fig1.show()

fig2, ax1 = plt.subplots(1)
plt.title("Neural Net Output")
ax1.imshow(img)
fig2.show()


#get pixels that are white
data = piece.getdata()
height = 500
width = 500
pixelList = []

for i in range(height):
    for j in range(width):
        stride = (width*i) + j
        pixelList.append((j, i, data[stride]))

whites = []
for pixel in pixelList:
    if pixel[2] > 0:
        whites.append(pixel[0:2])


whites = [list(elem) for elem in whites]

x_values = [x[0]+50 for x in whites]
y_values = [y[1]+50 for y in whites]

plt.scatter(x_values,y_values,1)

X = np.array(whites)
rec = plt.Rectangle((50,50),500,500,linewidth=1,edgecolor='r',facecolor='none')
ax1.add_patch(rec)


##image = data.hubble_deep_field()[0:500, 0:500]
#image = pieceArray
#image_gray = pieceArray/255
#
#blobs_log = blob_log(image_gray, max_sigma=30, num_sigma=10, threshold=.1)
#
## Compute radii in the 3rd column.
#blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
#
#blobs_dog = blob_dog(image_gray, max_sigma=30, threshold=.1)
#blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)
#
#blobs_doh = blob_doh(image_gray, max_sigma=30, threshold=.01)
#
#blobs_list = [blobs_log, blobs_dog, blobs_doh]
#colors = ['yellow', 'lime', 'red']
#titles = ['Laplacian of Gaussian', 'Difference of Gaussian',
#          'Determinant of Hessian']
#sequence = zip(blobs_list, colors, titles)
#
#fig3, axes = plt.subplots(1, 3, figsize=(9, 3), sharex=True, sharey=True,
#                         subplot_kw={'adjustable': 'box-forced'})
#ax = axes.ravel()
#
#for idx, (blobs, color, title) in enumerate(sequence):
#    ax[idx].set_title(title)
#    ax[idx].imshow(image, interpolation='nearest')
#    for blob in blobs:
#        y, x, r = blob
#        if r > 10:
#            c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
#            ax[idx].add_patch(c)
#    ax[idx].set_axis_off()


#image = pieceArray
image_gray = pieceArray/255

blobs_dog = blob_dog(image_gray, max_sigma=30, threshold=.05)
blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)

fig4,ax2 = plt.subplots(1, sharex=True, sharey=True)
plt.title("Blob Detection Centeroids")
#ax2 = axes.ravel()
ax2.imshow(img, interpolation='nearest')


for item in blobs_dog:
    if item[2] > 10:
        c = plt.Circle((item[1]+50, item[0]+50), item[2], color='lime', linewidth=2, fill=False)
        c# = plt.Circle((item[1]+50, item[0]+50), 5, color='lime', linewidth=2, fill=True)
        ax2.add_patch(c)

rec = plt.Rectangle((50,50),500,500,linewidth=1,edgecolor='r',facecolor='none')
ax2.add_patch(rec)

ax2.set_axis_off()



#plt.tight_layout()
plt.show()


