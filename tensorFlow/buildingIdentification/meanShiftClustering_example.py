# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 10:55:16 2018

@author: George
"""

#print(__doc__)

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

# #############################################################################
# Generate sample data
#centers = [[1, 1], [-1, -1], [1, -1]]
#X, _ = make_blobs(n_samples=10000, centers=centers, cluster_std=0.6)

resultsPath = r"C:\\Google Drive\\code\\python_code\\tensorFlow\\buildingIdentification\\results\\kerasModel_results\\"
mapPath = r"J:\AerialImageDataset\AerialImageDataset\test\images\bloomington23.tif"

def displayResults(folderPath):
    os.chdir(folderPath)
    fileList = []
    for file in glob.glob("*.txt"):
        fileList.append(file)


    array0 = np.genfromtxt(fileList[0],delimiter=",")
    for i in range(1,5):
        array = np.genfromtxt(fileList[i],delimiter=",")
        array0 = np.hstack((array0,array))

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
    return img



#reduce map size for large map
startX = 1275
endX = startX + 200
startY = 1275
endY = startY + 200


### Uncomment to display results
piece = displayResults(resultsPath)

startX = 1275
endX = startX + (6 * 100)
startY = 1275
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

fig2 = plt.figure(2)
plt.title("Neural Net Output")
plt.imshow(img2)
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

plt.scatter(x_values,y_values)

X = np.array(whites)

# #############################################################################
# Compute clustering with MeanShift

# The following bandwidth can be automatically detected using
bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=28000)

ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(X)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

print("number of estimated clusters : %d" % n_clusters_)

# #############################################################################
# Plot result
import matplotlib.pyplot as plt
from itertools import cycle

plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    my_members = labels == k
    cluster_center = cluster_centers[k]
    plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)
plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()