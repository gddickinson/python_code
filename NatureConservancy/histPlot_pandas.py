# -*- coding: utf-8 -*-
"""
Created on Tue May 22 14:41:22 2018

@author: George
"""

import pandas as pd
from matplotlib import pyplot as plt


fileName = r"C:\Google Drive\PioneersCraters_Project\buildingDetection\random500.csv"
df = pd.read_csv(fileName)

distances = df['distToBuil'].tolist()

fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(8, 4))

fig.suptitle('Histogram of distances from YOLO-identified location to center of nearest building\n(for 500 randomly sampled locations)')
ax0.hist(distances,25)
ax0.set_xlabel('distance (m)')
ax0.set_ylabel('# of observations')
ax0.set_title('All data')

ax1.hist(distances,100, range=(0,100))
ax1.set_xlabel('distance (m)')
ax1.set_ylabel('# of observations')
ax1.set_title('Zoom to 100m')

#number of observations 100m or less
numOb = sum(i < 100 for i in distances)
percent = round((numOb/len(distances))*100,2)

print("Total number of observations: " + str(len(distances)))
print("Number less than 100m from center of nearest building: " + str(numOb))
print(str(percent) + " %")