# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 11:31:38 2019

@author: George
"""

import numpy as np
import matplotlib.pyplot as plt

from sklearn import cluster, datasets, mixture
from sklearn.neighbors import kneighbors_graph
from itertools import cycle, islice
from sklearn.preprocessing import StandardScaler
from scipy.ndimage import gaussian_filter
from skimage.filters import threshold_local
from skimage.color import rgb2gray
from skimage import measure
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

np.random.seed(0)
n_samples = 1500

# Anisotropicly distributed data
random_state = 170
X, y = datasets.make_blobs(n_samples=n_samples, random_state=random_state, centers=10, cluster_std=0.1)
transformation = [[0.6, -0.6], [-0.4, 0.8]]
X_aniso = np.dot(X, transformation)
aniso = (X_aniso, y)

x = X[:,0]
y = X[:,1]

# normalize dataset for easier parameter selection
X_stand = StandardScaler().fit_transform(X)

dbscan = cluster.DBSCAN(eps=0.01, min_samples = 10)
clusters = dbscan.fit_predict(X_stand)

plt.figure(1)
fig1 = plt.scatter(x,y, c=clusters, cmap="plasma")

#guassian blur
H, xedges, yedges = np.histogram2d(x,y,bins=1000)
H_guass = gaussian_filter(H, sigma=10)

plt.figure(2)
fig2 = plt.imshow(np.rot90(H_guass))

#threshold
#gray = rgb2gray(H_guass)
thresholded = threshold_local(H_guass, 31)            
binary_adaptive = H_guass > thresholded

fig3, ax = plt.subplots()
ax.imshow(binary_adaptive)

#blob detection
labels = measure.label(binary_adaptive)

centeroids = []

for region in measure.regionprops(labels):
    # take regions with large enough areas
    if region.area >= 0.1:
	
        # draw rectangle around segmented objects
        minr, minc, maxr, maxc = region.bbox
        
        #get centeroid
        (cent_x,cent_y) = region.centroid 
        centeroids.append([cent_x,cent_y]) 

        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
												fill=False, edgecolor='red', linewidth=2)
        ax.add_patch(rect)

centeroids = np.array(centeroids)

plt.figure(4)
fig4 = plt.scatter(centeroids[:,0],centeroids[:,1])