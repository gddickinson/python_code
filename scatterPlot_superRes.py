# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 18:22:11 2018

@author: George
"""

import numpy as np
from matplotlib import pyplot as plt

fileName = r'C:\Users\George\Desktop\trial_2.txt'

Xc = np.loadtxt(fileName,skiprows=1,usecols=(3,))
Yc = np.loadtxt(fileName,skiprows=1,usecols=(4,))
channelList = np.loadtxt(fileName,skiprows=1,usecols=(0,), dtype=str)

colourMap = []

Al561 = []
Al647 = []

for i in range(len(channelList)):
    if channelList[i] == 'Alexa561':
        colourMap.append('red')
        Al561.append([Xc[i],Yc[i]])
        
    if channelList[i] == 'Alexa647':
        colourMap.append('blue')
        Al647.append([Xc[i],Yc[i]])

#plt.scatter(Xc,Yc,c=colourMap)
x,y = zip(*Al561)
#plt.scatter (x,y)

#### cluster Al561
from sklearn.cluster import DBSCAN
#clustering is dependent on epsilon value (eps)
dbscan = DBSCAN(eps=30).fit(Al561)
#get all clustering labels - labels indicate the cluster the points has been assigned to
labels = dbscan.labels_
#work out unique labels for colours
unique_labels = set(labels)
print ('Number of clusters assigned = ' + str(len(unique_labels)))
#assign colours to labels
colours = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
#create dictionary of labels and colours
colourIndex = dict(zip(unique_labels, colours))
#create list of colours, indexed the same as x,y position, for plotting
clusterColourMap = []
for label in labels:
    clusterColourMap.append(colourIndex[label])

#plot x,y coordinates with cluster colours
plt.scatter (x, y, c=clusterColourMap)
