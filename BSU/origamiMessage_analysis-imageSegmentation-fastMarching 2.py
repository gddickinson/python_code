# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 15:14:07 2019

@author: GEORGEDICKINSON
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 13:21:54 2019

@author: GEORGEDICKINSON
"""

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import h5py
import os
import shutil
from sklearn import cluster, datasets, mixture
from sklearn.neighbors import kneighbors_graph
from itertools import cycle, islice
from sklearn.preprocessing import StandardScaler, scale
from scipy.ndimage import gaussian_filter, distance_transform_edt, label
from skimage.filters import threshold_local
from skimage.color import rgb2gray
from skimage import measure
from skimage.feature import peak_local_max
from skimage.morphology import watershed
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandasql as ps
import scipy.misc
import skfmm

#picasso hdf5 format (with averaging): ['frame', 'x', 'y', 'photons', 'sx', 'sy', 'bg', 'lpx', 'lpy', 'group']
#Column Name       |	Description                                                                                                                      |	C Data Type
#frame	            |The frame in which the localization occurred, starting with zero for the first frame.	                                                |unsigned long
#x                |The subpixel x coordinate in camera pixels	                                                                                          |float
#y	              |The subpixel y coordinate in camera pixels	                                                                                          |float
#photons	       |The total number of detected photons from this event, not including background or camera offset	                                      |float
#sx	             |The Point Spread Function width in camera pixels                                                                                       |	float
#sy	             |The Point Spread Function height in camera pixels                                                                                      |	float
#bg	             |The number of background photons per pixel, not including the camera offset                                                            |	float
#lpx	         |The localization precision in x direction, in camera pixels, as estimated by the Cramer-Rao Lower Bound of the Maximum Likelihood fit.  |	float
#lpy	         |The localization precision in y direction, in camera pixels, as estimated by the Cramer-Rao Lower Bound of the Maximum Likelihood fit.  |	float


#set filepath

#filtered by photons averaged dataset
filePath = r"Y:\George_D_DATA\2019-09-05\from_Iapetus\20190905_Matrix2_syn2_pure_Triangles_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_12mM_PCD_TROLOX_1mM_14_16_10_fixed_locs_picked_avg_filtered.hdf5"
backgroundCenteroids = np.array([[255.772,256.08],[256.251,255.994], [255.743,255.843]])


savePath = filePath.split('.')[0] + '_analysisResult.csv'

#open picasso hdf5 file as DF
locs = pd.read_hdf(filePath, '/locs')
#check header
headers = locs.dtypes.index
print(headers)
print(locs.shape)
print(locs.head(n=5))

#scatter plot
#locs.plot.scatter(x='x',y='y', s=1, c='photons')
locs.plot.scatter(x='x',y='y', s=0.1, c='lpx', colormap='hot')
x = locs['x']
y = locs['y']
photons=locs['photons']
lpx = locs['lpx']
lpy = locs['lpy']


#group by 'group' - get mean values
groupedLocs = locs.groupby('group',as_index=False).mean().drop(['frame', 'x', 'y', 'sx', 'sy', 'bg', 'lpx', 'lpy'],axis=1)
#groupedLocs.rename(index=str,columns={'x':'meanX', 'y':'meanY', 'photons':'meanPHOTONS', 'sx':'meanSX', 'sy':'meanSY', 'bg':'meanBG', 'lpx':'meanLPX', 'lpy':'meanLPY'},inplace=True)
groupedLocs.rename(index=str,columns={'photons':'meanPHOTONS'},inplace=True)

#merge locs and groupedLocs based on group
locs = locs.merge(groupedLocs, on='group', how='outer')

#add normalized photon count (photons normalized by group mean photons)
locs['photons_normalized'] = np.divide(locs['photons'],locs['meanPHOTONS'])

#plt.figure(1)
#plt.scatter(x,y, s=1,c=photons)
#plt.scatter(x,y, s=1,c=lpx)

#guassian blur
nBins = 750
H, xedges, yedges = np.histogram2d(x,y,bins=nBins )
H_guass = gaussian_filter(H, sigma=5)

H_guassMask = H_guass < 5
H_guass[H_guassMask] = [0] 


fig2, ax0 = plt.subplots()
ax0.imshow(np.rot90(H_guass))
X, Y = np.meshgrid(xedges, yedges)
ax0.pcolormesh(X, Y, H_guass)

scipy.misc.imsave('averagedOrigami.png', H_guass)

#fast marching
D = skfmm.distance(H_guass)
T = skfmm.travel_time(H_guass, speed = 3.0 *np.ones_like(H_guass))

localMax = peak_local_max(D, indices=False,min_distance=5)
# perform a connected component analysis on the local peaks,
# using 8-connectivity, then appy the Watershed algorithm
markers = label(localMax, structure=np.ones((3, 3)))[0]
labels = watershed(-D, markers, mask=binary_adaptive)
print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))


fig3, ax = plt.subplots()
#ax.pcolormesh(X, Y, D)
ax.pcolormesh(X, Y, T)
#ax.pcolormesh(X, Y, labels)
#ax.pcolormesh(X, Y, mask)

