# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 14:05:45 2019

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
from sklearn.preprocessing import StandardScaler
from scipy.ndimage import gaussian_filter
from skimage.filters import threshold_local
from skimage.color import rgb2gray
from skimage import measure
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandasql as ps


#original locs
filePath = r"D:\data\2019-05-29\20190529_FlowCell_Chris_Triangles_ANDJRectangle_ASCII__300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_12mM_PCD_TROLOX_1mM_11_27_40-raw-locs_fixed_frames1-35000_centerSection_locs_render_DRIFT-4_picked_FOR-FILTERING_avg.hdf5"

#filtered locs
filePath1 = r"D:\data\2019-05-29\20190529_FlowCell_Chris_Triangles_ANDJRectangle_ASCII__300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_12mM_PCD_TROLOX_1mM_11_27_40-raw-locs_fixed_frames1-35000_centerSection_locs_render_DRIFT-4_picked_FOR-FILTERING_avg_analysisResult.csv"
#centeroids
filePath2 = r"D:\data\2019-05-29\20190529_FlowCell_Chris_Triangles_ANDJRectangle_ASCII__300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_12mM_PCD_TROLOX_1mM_11_27_40-raw-locs_fixed_frames1-35000_centerSection_locs_render_DRIFT-4_picked_FOR-FILTERING_avg_analysisCenteroids.csv"

searchArea = 0.035 * 0.035


#open picasso hdf5 file as DF
locs = pd.read_hdf(filePath, '/locs')
#check header
headers = locs.dtypes.index
print(headers)
print(locs.shape)
print(locs.head(n=5))


#open saved filteredLocs csv
filteredLocs = pd.read_csv(filePath1)
#check header
headers = filteredLocs.dtypes.index
print(headers)
print(filteredLocs.shape)
print(filteredLocs.head(n=5))

#load centeroids

centeroids = np.loadtxt(filePath2,delimiter=',')

fig4, ax2 = plt.subplots()
ax2.scatter(x=filteredLocs.x, y=filteredLocs.y, s=0.1, color='blue')
ax2.scatter(centeroids[:,0],centeroids[:,1], color='red')


#get background from manually selected locations
backgroundCenteroids = np.array([[256.079,220.281],[256.337,220.108], [256.121,219.952]])

backGroundLocs = pd.DataFrame()

for i in range(len(backgroundCenteroids)):
    query = "SELECT * FROM locs WHERE (((locs.x - {})*(locs.x - {})) + ((locs.y - {})*(locs.y - {}))) <= ({})".format(backgroundCenteroids[i][0], backgroundCenteroids[i][0], backgroundCenteroids[i][1], backgroundCenteroids[i][1], searchArea)
    filtered = ps.sqldf(query,locals())
    filtered['bindingSite'] = i
    backGroundLocs = backGroundLocs.append(filtered)
    print(i)

ax2.scatter(x=backGroundLocs.x, y=backGroundLocs.y, s=0.1, color='green')
ax2.scatter(backgroundCenteroids[:,0],backgroundCenteroids[:,1], color='yellow')    

#plot all binding sites against time
filteredLocs.plot.scatter(x='frame',y='photons_normalized',c='bindingSite',colormap='tab20b',s=0.5)
filteredLocs.plot.scatter(x='frame',y='photons',c='bindingSite',colormap='tab20b',s=0.5)

filteredLocs.hist('photons_normalized',bins=1000)
filteredLocs.hist('photons',bins=1000)

backGroundLocs.hist('photons_normalized',bins=1000)
backGroundLocs.hist('photons',bins=1000)

#plot by binding site
def createPlot(df, groupNumber = [0], bindingSite = 0, filterByGroup = True, normalized = True):
    #if filter by group true:
    if filterByGroup:
        group = df.loc[(df.group.isin(groupNumber)) & (df.bindingSite == bindingSite)]
    else:
        group = df.loc[df.bindingSite == bindingSite]
  
    #plot group histogram photons
    if normalized:
        group.hist(column='photons_normalized',bins=40)
    else:
        group.hist(column='photons',bins=40)

    #plot histo frames
    group.hist(column='frame', bins=40)
    
    #plot group photons / frame
    if normalized:
        group.plot.scatter(x='frame', y='photons_normalized')
    else:
       group.plot.scatter(x='frame', y='photons') 
    
    return


createPlot(filteredLocs, groupNumber = [0], bindingSite = 0, normalized=True)
createPlot(filteredLocs, bindingSite = 12, filterByGroup = False)
createPlot(filteredLocs, bindingSite = 0, filterByGroup = False, normalized = False)

#plot all binding sites seperately
#for i in range(max(filteredLocs['bindingSite'])):
#    createPlot(filteredLocs, bindingSite = i, filterByGroup = False, normalized = False)
#    print(i)


#get number of binding sites per object

def bindingSitePlot(df, groupNumber = 0, numberOfBindingSites = numberOfBindingSites):
    group = df.loc[df.group == groupNumber]
    bindingSites = group.groupby('bindingSite',as_index=False).count().drop(['x', 'y', 'photons', 'sx', 'sy', 'bg', 'lpx', 'lpy', 
                                        'meanPHOTONS', 'photons_normalized'],axis=1)
    #bindingSites['group'] = groupNumber
    #bindingSites.rename(index=str,columns={'frame':'numberOfLocalizations'},inplace=True)
    #print(bindingSites)
    #group.hist(column='bindingSite',bins=numberOfBindingSites)
    count,division = np.histogram(group['bindingSite'], bins=numberOfBindingSites)
    return count

#binding sites
numberOfBindingSites = len(filteredLocs['bindingSite'].unique())    
bindingSiteDF = pd.DataFrame(columns=list(range(numberOfBindingSites))).astype(int)   
for i in range(len(filteredLocs['group'].unique())):
    bindingSiteDF.loc[i] = bindingSitePlot(filteredLocs, groupNumber = i)
    
#background
numberOfBackgroundSites = len(backGroundLocs['bindingSite'].unique())  
backgroundDF = pd.DataFrame(columns=list(range(numberOfBackgroundSites))).astype(int)    
for i in range(len(backGroundLocs['group'].unique())):
    backgroundDF.loc[i] = bindingSitePlot(backGroundLocs, groupNumber = i, numberOfBindingSites = numberOfBackgroundSites)


backgroundStats = backgroundDF.describe()
backgroundMean = np.mean(backgroundStats.loc['mean'].values)

bindingSiteStatDF = pd.DataFrame()

bindingSiteStatDF['zeros'] = (bindingSiteDF < backgroundMean).astype(int).sum(axis=1)
bindingSiteStatDF['numberOfBindingSites'] = (numberOfBindingSites - bindingSiteDF['zeros'])

#fig5, ax3 = plt.subplots()
fig5 = bindingSiteStatDF.hist(column='numberOfBindingSites', bins=numberOfBindingSites+1)
fig5.flatten()[0].set_xlabel('number of binding sites per origami')
fig5.flatten()[0].set_ylabel('number of origami')

stats = bindingSiteDF.describe()
ind = np.arange(numberOfBindingSites)
siteMean = stats.loc['mean'].values
siteStd = stats.loc['std'].values

fig6, ax4 = plt.subplots()
ax4= plt.bar(ind,siteMean, width=0.5, yerr = siteStd)


siteMap = bindingSiteDF > backgroundMean
siteMap_stats = siteMap.describe()
siteFrequency = siteMap_stats.loc['freq'].values

fig7, ax5 = plt.subplots()
ax5= plt.bar(ind,siteFrequency, width=0.5)

