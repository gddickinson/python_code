# -*- coding: utf-8 -*-
"""
Created on Thu May 24 11:51:31 2018

@author: George
"""

import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

fileName_1 = r"C:\Users\George\Desktop\buildingClassifier\detectedBuildings.csv"
fileName_2 = r"C:\Users\George\Desktop\buildingClassifier\points_cropped_private.csv"
df1 = pd.read_csv(fileName_1)
df2 = pd.read_csv(fileName_2)

#YOLO detected
detected_X = df1['POINT_X'].tolist()
detected_Y = df1['POINT_Y'].tolist()

detected = list(zip(detected_X,detected_Y))

#found by me
found_X = df2['POINT_X'].tolist()
found_Y = df2['POINT_Y'].tolist()

found = list(zip(found_X, found_Y))

#calculate nearest neighbours
print("Working on distance calculation...")
distances = np.array(euclidean_distances(found, detected))
min_distances = np.amin(distances, axis=1)
print("Done with calculating distances!")

#plot histograms
fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(8, 4))

fig.suptitle('Histogram of distances from manually-identified location to nearest YOLO-identified location')
ax0.hist(min_distances,25)
ax0.set_xlabel('distance (m)')
ax0.set_ylabel('# of observations')
ax0.set_title('All data')

ax1.hist(min_distances,200, range=(0,1000))
ax1.set_xlabel('distance (m)')
ax1.set_ylabel('# of observations')
ax1.set_title('Zoom to 1000m')



#number of observations 100m or less
numOb = sum(i < 100 for i in min_distances)
percent = round((numOb/len(min_distances))*100,2)

print("Total number of observations: " + str(len(min_distances)))
print("Number less than 100m from center of nearest building: " + str(numOb))
print(str(percent) + " %")