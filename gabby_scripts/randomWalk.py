#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 20:32:36 2022

@author: george
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.widgets import Slider
from sklearn.neighbors import KDTree
import random
from tqdm import tqdm
import os
from skimage import io
from skimage.transform import resize

%matplotlib qt 

#Load starting points
#filepaths
# BAPTA DATA
#pointFile = '/Users/george/Desktop/from_Gabby/BAPTA/GB_132_2021_08_11_HTEndothelial_BAPTA_plate1_6_denoised_dataexcel.xlsx'
#xMin,xMax,yMin,yMax = [20,30,30,40]
#trackFile = '/Users/george/Desktop/from_Gabby/BAPTA/GB_132_2021_08_11_HTEndothelial_BAPTA_plate1_6_denoised_trackexcel.xlsx'

# NON-BAPTA DATA
pointFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_Denoisedai_trackdata.xlsx'
tiffFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_MMStack_Default.ome - Denoised.tif'

xMin,xMax,yMin,yMax = [20,30,30,40]
#pointFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_yoda1_3_Denoisedai_trackdata.xlsx'
#pointFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_2_Denoisedai_trackdata.xlsx'
#pointFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_yoda1_2_Denoisedai_trackdata.xlsx'

#set savepath
savePath = os.path.splitext(pointFile)[0]

#load data into DF
pointsDF = pd.read_excel(pointFile)
#tracksDF = pd.read_excel(trackFile)

#load image data
img = io.imread(tiffFile)
#reshape to x,y,t
img = np.transpose(img,(1,2,0))

#srecording options
pixelSize = 0.11

#get Col names
pointsColNames = list(pointsDF.columns)
#tracksColNames = list(tracksDF.columns)

print('--- Points Columns ---')
print(pointsColNames)
#print('--- Tracks Columns ---')
#print(tracksColNames)


#CROP FOR ALL DISTANCES ANALYSIS
pointsDF = pointsDF[(pointsDF['PositionX [µm]'] > xMin) & (pointsDF['PositionX [µm]'] < xMax)]
pointsDF = pointsDF[(pointsDF['PositionY [µm]'] > yMin) & (pointsDF['PositionY [µm]'] < yMax)]

#crop image data
img = img[int(xMin/pixelSize) : int(xMax/pixelSize), int(yMin/pixelSize) : int(yMax/pixelSize), :]

#get number of tracks
nTracks = np.max(pointsDF['Tree ID'])

#keep x,y,time values
points = pointsDF[['PositionX [µm]', 'PositionY [µm]', 'Time [s]', 'Tree ID']]

#convert time to ms (frame)
#points['Time [s]'] = points['Time [s]'] * 100
#points['Time [s]'] = points['Time [s]'].astype(int)

#get distribution of segment length from tracks
segLengths = pointsDF['Seg.Length [µm]'].tolist()
#remove nans
segLengths = [x for x in segLengths if np.isnan(x) == False]

fig0, ax0 = plt.subplots(figsize=(12,4),)
ax0.hist(segLengths, bins = 100)
ax0.set_title("Segment Lengths")

ax0.set(ylabel='# of observations')
ax0.set(xlabel='length [µm]')


#tracksDF['average track length'] = tracksDF['Length [µm]']/tracksDF['No.Segments']
#distances = tracksDF['average track length']

#fig0, ax0 = plt.subplots(1, 2, figsize=(12,4), sharex=False, sharey=False)
#ax0[0].hist(distances, bins = 50)

#filter df for points at time 0
minTime = np.min(points['Time [s]'])
pointsTime_0 = points[points['Time [s]'] == minTime] 

#plt.scatter(pointsTime_0['PositionX [µm]'], pointsTime_0['PositionY [µm]'])

###### RANDOM WALK SIMULATION #####

#define random walk point generator
def getPoint(x, y, radius):
    #generating random points
    #theta=np.random.uniform(0,2*np.pi,1)
    #get x and y
    #x=radius*np.cos(theta)+x
    #y=radius*np.sin(theta)+y
    
    #just up, down, left, right
    directions = ["UP", "DOWN", "LEFT", "RIGHT"]
    step = random.choice(directions)
    
    # Move the object according to the direction
    if step == "RIGHT":
        x = x + radius
        y= y
    elif step == "LEFT":
        x = x - radius
        y = y
    elif step == "UP":
        x = x
        y = y + radius
    elif step == "DOWN":
        x = x
        y = y - radius  
    
    return float(x),float(y)


#FOR TESTING - just one point
#pointsTime_0 = pointsTime_0.head(1)

# get distance mean and SD
#mu = np.mean(distances)
#sigma = np.std(distances)
n = len(pointsTime_0['PositionX [µm]'])

#plot hist of sample distribution
#distancesForHist = np.random.normal(mu,sigma,n)
#ax0[1].hist(distancesForHist, bins = 50)
#ax0[1].set_title("Random Distribution")
#ax0[0].set_title("Point data")
#ax0[0].set(xlabel="distances (µm)", ylabel = "# of observations")
#ax0[1].set(xlabel="distances (µm)", ylabel = "# of observations")

#get number of frames
maxTime = np.max(pointsDF['ND.T'])

#create list of IDs
ID_list = list(range(0,n))

#get new position for each point, starting at time 0
timeSteps = range(1,maxTime)
for i in tqdm(timeSteps):
    #getrandom distances from normal diostribution based on mean distance
    #randomDistances = np.random.normal(mu,sigma,n)
    randomDistances = random.sample(segLengths,n)
    #initiate
    if i == 1:      
        newPositions = map(getPoint, pointsTime_0['PositionX [µm]'],pointsTime_0['PositionY [µm]'],randomDistances)
        newPositions_list = np.array(list(newPositions))
        d = {'PositionX [µm]' : newPositions_list[:,0].tolist(),
             'PositionY [µm]' : newPositions_list[:,1].tolist(),
             'ID' : ID_list}
        #append to pointsTime_0 df
        newDF = pd.DataFrame(data=d)
        newDF['Time [s]'] = i
        pointsTime_0 = pointsTime_0.append(newDF)
    else:
        newPositions = map(getPoint, newDF['PositionX [µm]'],newDF['PositionY [µm]'],randomDistances)
        newPositions_list = np.array(list(newPositions))
        d = {'PositionX [µm]' : newPositions_list[:,0].tolist(),
             'PositionY [µm]' : newPositions_list[:,1].tolist(),
             'ID' : ID_list}
        #append to pointsTime_0 df
        newDF = pd.DataFrame(data=d)
        newDF['Time [s]'] = i
        pointsTime_0 = pointsTime_0.append(newDF)


#plot all points    
#plt.scatter(pointsTime_0['PositionX [µm]'], pointsTime_0['PositionY [µm]'])
#plot some point data

fig1, (ax1,ax2,axImg) = plt.subplots(1, 3, figsize=(12,4), sharex=True, sharey=True)
points_rw  = pointsTime_0.rename(columns={"PositionX [µm]": "x", "PositionY [µm]": "y", "Time [s]": "time"})
groups_rWalk = points_rw.groupby('ID')
for name, group in groups_rWalk:
    ax1.plot(group.x * (1/pixelSize), group.y * (1/pixelSize), marker='.', linestyle='-', markersize=3, label=name)

points_points  = points.rename(columns={"PositionX [µm]": "x", "PositionY [µm]": "y", "Tree ID": "ID", "Time [s]": "time"})
groups_points = points_points.groupby('ID')
for name, group in groups_points:
    ax2.plot(group.x * (1/pixelSize), group.y * (1/pixelSize), marker='.', linestyle='-', markersize=3, label=name)

img_max = np.max(img, axis=2)
axImg.imshow(img_max)

ax1.set_title("Random Walk")
ax2.set_title("Point data")
axImg.set_title("Image data")

axisMin = int(np.min([pointsDF['PositionX [µm]'], pointsDF['PositionY [µm]']])* (1/pixelSize))
axisMax = int(np.max([pointsDF['PositionX [µm]'], pointsDF['PositionY [µm]']])* (1/pixelSize))

ax1.set_xlim(axisMin,axisMax)
ax1.set_ylim(axisMin,axisMax)
ax2.set_xlim(axisMin,axisMax)
ax2.set_ylim(axisMin,axisMax)
axImg.set_xlim(axisMin,axisMax)
axImg.set_ylim(axisMin,axisMax)


ax1.set(xlabel='PositionX [pixels]')
ax1.set(ylabel='PositionY [pixels]')
ax2.set(xlabel='PositionX [pixels]')
ax2.set(ylabel='PositionY [pixels]')
axImg.set(xlabel='PositionX [pixels]')
axImg.set(ylabel='PositionY [pixels]')

#plt.show()




#=============================================================================
#plot updateable graph (woprks for 1 point, use groups to plot all points)
fig, axs = plt.subplots(1, 3, figsize=(10,4), sharex=True, sharey=True)
plt.subplots_adjust(left=0.25, bottom=0.25)

#points by time
points_byTime = points.groupby('Time [s]')
#RW by time
RW_byTime = pointsTime_0.groupby('Time [s]')

#get points index (times in s not frames)
RWGroupIndex = list(RW_byTime.groups)
pointsGroupIndex = list(points_byTime.groups)

#plot time 0
RW_time = RW_byTime.get_group(RWGroupIndex[0])
points_time = points_byTime.get_group(pointsGroupIndex[0])

axs[0].scatter(RW_time['PositionX [µm]']* (1/pixelSize), RW_time['PositionY [µm]']* (1/pixelSize))
axs[1].scatter(points_time['PositionX [µm]']* (1/pixelSize), points_time['PositionY [µm]']* (1/pixelSize))
axs[2].imshow(img[:,:,0])

t = RW_byTime.ngroups

axcolor = 'lightgoldenrodyellow'
axpos = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

spos = Slider(axpos, 'frame', 0, t-1, valstep=1)


axs[0].set_title("Random Walk")
axs[1].set_title("Point data")
axs[0].set(xlabel='PositionX [µm]')
axs[0].set(ylabel='PositionY [µm]')
axs[1].set(xlabel='PositionX [µm]')
axs[1].set(ylabel='PositionY [µm]')

def update(val):
    xlim = axs[0].get_xlim()
    ylim = axs[0].get_ylim()
    axs[0].cla()
    axs[1].cla()
    #get slider index
    ind = int(spos.val)
    #select group to plot
    RW_time = RW_byTime.get_group(RWGroupIndex[ind])
    points_time = points_byTime.get_group(pointsGroupIndex[ind])
    #plot
    axs[0].scatter(RW_time['PositionX [µm]']* (1/pixelSize), RW_time['PositionY [µm]']* (1/pixelSize))
    axs[1].scatter(points_time['PositionX [µm]']* (1/pixelSize), points_time['PositionY [µm]']* (1/pixelSize))
    axs[2].imshow(img[:,:,ind])
    
    axs[0].set_xlim(xlim[0],xlim[1])
    axs[0].set_ylim(ylim[0],ylim[1])
    axs[0].set_title("Random Walk")
    axs[1].set_title("Point data")
    axs[0].set(xlabel='PositionX [µm]')
    axs[0].set(ylabel='PositionY [µm]')
    axs[1].set(xlabel='PositionX [µm]')
    axs[1].set(ylabel='PositionY [µm]')
    fig.canvas.draw_idle()

spos.on_changed(update)

plt.show()
#=============================================================================
  


#plot updateable graph (woprks for 1 point, use groups to plot all points)
figI, axI = plt.subplots(figsize=(10,4), sharex=True, sharey=True)
plt.subplots_adjust(left=0.25, bottom=0.25)

#points by time
points_byTime = points.groupby('Time [s]')

#get points index (times in s not frames)
pointsGroupIndex = list(points_byTime.groups)

#plot time 0
points_time = points_byTime.get_group(pointsGroupIndex[0])

axI.imshow(img[:,:,0])
axI.scatter(points_time['PositionX [µm]']* (1/pixelSize), points_time['PositionY [µm]']* (1/pixelSize))

t = points_byTime.ngroups

axcolor = 'lightgoldenrodyellow'
axpos = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

spos = Slider(axpos, 'frame', 0, t-1, valstep=1)

axI.set(xlabel='PositionX [µm]')
axI.set(ylabel='PositionY [µm]')


def update(val):
    xlim = axI.get_xlim()
    ylim = axI.get_ylim()
    axI.cla()
    #get slider index
    ind = int(spos.val)
    #select group to plot
    points_time = points_byTime.get_group(pointsGroupIndex[ind])
    #plot
    axI.imshow(img[:,:,ind])    
    axI.scatter(points_time['PositionX [µm]']* (1/pixelSize), points_time['PositionY [µm]']* (1/pixelSize))

    
    axI.set_xlim(xlim[0],xlim[1])
    axI.set_ylim(ylim[0],ylim[1])

    fig.canvas.draw_idle()

spos.on_changed(update)

plt.show()








#get nearest neighbour distances for random walk simulation

#define funciton for NN
def getNearestNeighbors(train,test,k=2):
    tree = KDTree(train, leaf_size=5)   
    dist, ind = tree.query(test, k=k)
    #dist.reshape(np.size(dist),)     
    return dist, ind

def getAllDistances(train,test, k):
    tree = KDTree(train, leaf_size=5)   
    dist, ind = tree.query(test, k=k)
    #dist.reshape(np.size(dist),)     
    return dist, ind

# =============================================================================
# #select columns
# testData_df = pointsTime_0[['PositionX [µm]','PositionY [µm]']]
# trainData_df = pointsTime_0[['PositionX [µm]','PositionY [µm]']]
# 
# #nearest neighbour
# distances_RW, trainData_indexes_RW = getNearestNeighbors(trainData_df.to_numpy(),testData_df.to_numpy())
# 
# #get distances not to self
# nnDist_rWalk = distances_RW[:,1]
# #filter out zero distances
# mask = nnDist_rWalk > 0
# nnDist_rWalk_noZeros = nnDist_rWalk[mask] 
# 
# 
# ###### NEAREST NEIGHBOUR FOR DATASET ######
# 
# #select columns
# testData_df = points[['PositionX [µm]','PositionY [µm]']]
# trainData_df = points[['PositionX [µm]','PositionY [µm]']]
# 
# #nearest neighbour
# distances_points, trainData_indexes_points = getNearestNeighbors(trainData_df.to_numpy(),testData_df.to_numpy())
# 
# #get distances not to self
# nnDist_pointData = distances_points[:,1]
# #filter out zero distances
# mask = nnDist_pointData > 0
# nnDist_pointData_noZeros = nnDist_pointData[mask] 
# 
# 
# #plot histograms
# 
# nBins =100
# 
# fig2, (ax3,ax4) = plt.subplots(2, 1, figsize=(12,4), sharex=True)
# fig2.suptitle('Nearest Neighbour Distances')
# 
# ax3.hist(nnDist_rWalk, bins=nBins, label='Random Walk')
# ax4.hist(nnDist_pointData, bins=nBins, label='Point Data')
# 
# ax3.set_title("Random Walk")
# ax4.set_title("Point data")
# 
# ax3.set(ylabel = "# of observations")
# ax4.set(xlabel="distances (µm)", ylabel = "# of observations")
# 
# ax3.set_yscale('log')
# ax4.set_yscale('log')
# #ax4.set_ylim([0,300])
# 
# plt.show()
# 
# # plot the cumulative histogram
# fig3, (ax5,ax6) = plt.subplots(2,1, figsize=(12, 4), sharex=True)
# ax5.hist(nnDist_rWalk, bins=nBins, density=True, histtype='step',
#                            cumulative=True, label='Random Walk')
# 
# ax6.hist(nnDist_pointData, bins=nBins, density=True, histtype='step',
#                            cumulative=True, label='Random Walk')
# 
# ax5.set_title("Random Walk")
# ax6.set_title("Point data")
# 
# ax5.set(ylabel = "Likelihood of occurence")
# ax6.set(xlabel="distances (µm)", ylabel = "Likelihood of occurence")
# 
# #ax5.set_yscale('log')
# #ax6.set_yscale('log')
# 
# plt.show()
# =============================================================================



# =============================================================================
# #NO ZEROS DATA
# nBins =100
# 
# fig4, (ax7,ax8) = plt.subplots(2, 1, figsize=(12,4), sharex=True)
# fig2.suptitle('Nearest Neighbour Distances')
# 
# ax7.hist(nnDist_rWalk_noZeros, bins=nBins, label='Random Walk')
# ax8.hist(nnDist_pointData_noZeros, bins=nBins, label='Point Data')
# 
# ax7.set_title("Random Walk - no zeros")
# ax8.set_title("Point data - no zeros")
# 
# ax7.set(ylabel = "# of observations")
# ax8.set(xlabel="distances (µm)", ylabel = "# of observations")
# 
# #ax7.set_yscale('log')
# #ax8.set_yscale('log')
# #ax8.set_ylim([0,300])
# 
# plt.show()
# 
# # plot the cumulative histogram
# fig5, (ax9,ax10) = plt.subplots(2,1, figsize=(12, 4), sharex=True)
# ax9.hist(nnDist_rWalk_noZeros, bins=nBins, density=True, histtype='step',
#                            cumulative=True, label='Random Walk')
# 
# ax10.hist(nnDist_pointData_noZeros, bins=nBins, density=True, histtype='step',
#                            cumulative=True, label='Random Walk')
# 
# ax9.set_title("Random Walk - no zeros")
# ax10.set_title("Point data - no zeros")
# 
# ax9.set(ylabel = "Likelihood of occurence")
# ax10.set(xlabel="distances (µm)", ylabel = "Likelihood of occurence")
# 
# #ax9.set_yscale('log')
# #ax10.set_yscale('log')
# 
# plt.show()
# =============================================================================

# =============================================================================
# ###################### DISTANCES FROM FRAME 0 POSITIONS ##############################
# ###ALL POINTS IN RECORDING
# #Point Data
# pointsTime_0_forNN = points[points['Time [s]'] == 0] 
# #select columns
# testData_df = pointsTime_0_forNN[['PositionX [µm]','PositionY [µm]']]
# trainData_df = points[['PositionX [µm]','PositionY [µm]']]
# 
# #nearest neighbour
# distances_pointsTime_0, trainData_indexes_pointsTime_0 = getNearestNeighbors(trainData_df.to_numpy(),testData_df.to_numpy())
# 
# #get distances not to self
# nnDist_pointData_Time0 = distances_pointsTime_0[:,1]
# 
# 
# #Random Walk
# RW_Time_0_forNN = points[points['Time [s]'] == 0] 
# #select columns
# testData_df = RW_Time_0_forNN[['PositionX [µm]','PositionY [µm]']]
# trainData_df = pointsTime_0[['PositionX [µm]','PositionY [µm]']]
# 
# #nearest neighbour
# distances_pointsTime_0, trainData_indexes_pointsTime_0 = getNearestNeighbors(trainData_df.to_numpy(),testData_df.to_numpy())
# 
# #get distances not to self
# nnDist_RW_Time0 = distances_pointsTime_0[:,1]
# 
# #plot histograms
# nBins =20
# 
# fig6, (ax11,ax12) = plt.subplots(2, 1, figsize=(12,4), sharex=True, sharey=True)
# fig6.suptitle('Nearest Neighbour Distances - from time 0 to all points in all frames')
# 
# ax11.hist(nnDist_RW_Time0, bins=nBins, label='Random Walk')
# ax12.hist(nnDist_pointData_Time0, bins=nBins, label='Point Data')
# 
# ax11.set_title("Random Walk")
# ax12.set_title("Point data")
# 
# ax11.set(ylabel = "# of observations")
# ax12.set(xlabel="distances (µm)", ylabel = "# of observations")
# 
# #ax11.set_yscale('log')
# #ax12.set_yscale('log')
# #ax12.set_ylim([0,300])
# 
# plt.show()
# =============================================================================


# =============================================================================
# ####NN FOR EACH FRAME COMPARED TO TIME 0
# #point data
# pointsTime_0_forNN = points[points['Time [s]'] == 0] 
# 
# groups_pointsTime = points.groupby('Time [s]')
# 
# distances_pointsTime0_ALL = []
# 
# for time in tqdm(groups_pointsTime):
#     #plt.scatter(time[1]['PositionX [µm]'],time[1]['PositionY [µm]'])
#     testData_df = time[1][['PositionX [µm]','PositionY [µm]']]
#     trainData_df = points[['PositionX [µm]','PositionY [µm]']]
# 
#     #nearest neighbour
#     distances_pointsTime_0, trainData_indexes_pointsTime_0 = getNearestNeighbors(trainData_df.to_numpy(),testData_df.to_numpy())
# 
#     #get distances not to self
#     nnDist_pointData_Time0 = distances_pointsTime_0[:,1]
#     
#     distances_pointsTime0_ALL.extend(nnDist_pointData_Time0.tolist())
# 
# 
# #random walk
# pointsTime_0_forNN = points[points['Time [s]'] == 0] 
# 
# groups_RW_Time = pointsTime_0.groupby('Time [s]')
# 
# distances_RW_Time0_ALL = []
# 
# for time in tqdm(groups_RW_Time):
#     #plt.scatter(time[1]['PositionX [µm]'],time[1]['PositionY [µm]'])
#     testData_df = time[1][['PositionX [µm]','PositionY [µm]']]
#     trainData_df = pointsTime_0[['PositionX [µm]','PositionY [µm]']]
# 
#     #nearest neighbour
#     distances_pointsTime_0, trainData_indexes_pointsTime_0 = getNearestNeighbors(trainData_df.to_numpy(),testData_df.to_numpy())
# 
#     #get distances not to self
#     nnDist_pointData_Time0 = distances_pointsTime_0[:,1]
#     
#     distances_RW_Time0_ALL.extend(nnDist_pointData_Time0.tolist())
# 
# 
# #plot histograms
# nBins =100
# 
# fig7, (ax13,ax14) = plt.subplots(2, 1, figsize=(12,4), sharex=True, sharey=True)
# fig7.suptitle('Nearest Neighbour Distances - from time 0 to all points, frame by frame')
# 
# ax13.hist(distances_RW_Time0_ALL, bins=nBins, label='Random Walk')
# ax14.hist(distances_pointsTime0_ALL, bins=nBins, label='Point Data')
# 
# ax13.set_title("Random Walk")
# ax14.set_title("Point data")
# 
# ax13.set(ylabel = "# of observations")
# ax14.set(xlabel="distances (µm)", ylabel = "# of observations")
# 
# ax13.set_yscale('log')
# ax14.set_yscale('log')
# #ax14.set_ylim([0,300])
# 
# plt.show()
# =============================================================================

# =============================================================================
# 
# 
# ####NN FOR EACH FRAME Every Point
# #point data
# groups_pointsTime = points.groupby('Time [s]')
# 
# distances_points_ALL_ALL = []
# 
# for time in tqdm(groups_pointsTime):
#     #plt.scatter(time[1]['PositionX [µm]'],time[1]['PositionY [µm]'])
#     testData_df = time[1][['PositionX [µm]','PositionY [µm]']]
#     trainData_df = time[1][['PositionX [µm]','PositionY [µm]']]
# 
#     #nearest neighbour
#     distances_points_ALL, trainData_indexes_points_ALL= getNearestNeighbors(trainData_df.to_numpy(),testData_df.to_numpy())
# 
#     #get distances not to self
#     nnDist_pointData_ALL = distances_points_ALL[:,1]
#     
#     distances_points_ALL_ALL.extend(nnDist_pointData_ALL.tolist())
# 
# 
# #random walk
# groups_RW_Time = pointsTime_0.groupby('Time [s]')
# 
# distances_RW_ALL_ALL = []
# 
# for time in tqdm(groups_RW_Time):
#     #plt.scatter(time[1]['PositionX [µm]'],time[1]['PositionY [µm]'])
#     testData_df = time[1][['PositionX [µm]','PositionY [µm]']]
#     trainData_df = time[1][['PositionX [µm]','PositionY [µm]']]
# 
#     #nearest neighbour
#     distances_RW_ALL, trainData_indexes_RW_ALL = getNearestNeighbors(trainData_df.to_numpy(),testData_df.to_numpy())
# 
#     #get distances not to self
#     nnDist_RW_ALL = distances_RW_ALL[:,1]
#     
#     distances_RW_ALL_ALL.extend(nnDist_RW_ALL.tolist())
# 
# 
# #plot histograms
# nBins =200
# 
# fig8, (ax15,ax16) = plt.subplots(2, 1, figsize=(8,4), sharex=True, sharey=True)
# fig8.suptitle('Nearest Neighbour Distances - all points to all points, frame by frame')
# 
# ax15.hist(distances_RW_ALL_ALL, bins=nBins, label='Random Walk')
# ax16.hist(distances_points_ALL_ALL, bins=nBins, label='Point Data')
# 
# ax15.set_title("Random Walk")
# ax16.set_title("Point data")
# 
# ax15.set(ylabel = "# of observations")
# ax16.set(xlabel="distances (µm)", ylabel = "# of observations")
# 
# #ax15.set_yscale('log')
# #ax16.set_yscale('log')
# ax16.set_xlim([0,5])
# 
# plt.show()
# saveName = savePath + 'NN-hist.png'
# plt.savefig(saveName)
# # =============================================================================
# # # plot cumulative histogram
# # fig9 = plt.hist(distances_RW_ALL_ALL, bins=nBins, density=True, histtype='step',
# #                            cumulative=True, label='Random Walk', color='red')
# # 
# # plt.hist(distances_points_ALL_ALL, bins=nBins, density=True, histtype='step',
# #                            cumulative=True, label='Point Data', color='b')
# # 
# # 
# # 
# # plt.legend(loc='upper right')
# # 
# # plt.ylabel("Likelihood of occurence")
# # plt.xlabel("distances (µm)")
# # 
# # plt.yscale('log')
# # plt.xscale('log')
# # 
# # plt.show()
# # =============================================================================
# 
# 
# 
# 
# 
# 
# 
# #### ALL distances - all points, FOR EACH FRAME
# #point data
# groups_pointsTime = points.groupby('Time [s]')
# 
# distances_points_ALL_ALL = []
# 
# for time in tqdm(groups_pointsTime):
#     #plt.scatter(time[1]['PositionX [µm]'],time[1]['PositionY [µm]'])
#     testData_df = time[1][['PositionX [µm]','PositionY [µm]']]
#     trainData_df = time[1][['PositionX [µm]','PositionY [µm]']]
# 
#     #nearest neighbour
#     distances_points_ALL, trainData_indexes_points_ALL= getAllDistances(trainData_df.to_numpy(),testData_df.to_numpy(),len(testData_df))
# 
#     #get distances not to self
#     nnDist_pointData_ALL = distances_points_ALL[:,1:].flatten()
#     
#     distances_points_ALL_ALL.extend(nnDist_pointData_ALL.tolist())
# 
# 
# #random walk
# groups_RW_Time = pointsTime_0.groupby('Time [s]')
# 
# distances_RW_ALL_ALL = []
# 
# for time in tqdm(groups_RW_Time):
#     #plt.scatter(time[1]['PositionX [µm]'],time[1]['PositionY [µm]'])
#     testData_df = time[1][['PositionX [µm]','PositionY [µm]']]
#     trainData_df = time[1][['PositionX [µm]','PositionY [µm]']]
# 
#     #nearest neighbour
#     distances_RW_ALL, trainData_indexes_RW_ALL = getAllDistances(trainData_df.to_numpy(),testData_df.to_numpy(),len(testData_df))
# 
#     #get distances not to self
#     nnDist_RW_ALL = distances_RW_ALL[:,1:].flatten()
#     
#     distances_RW_ALL_ALL.extend(nnDist_RW_ALL.tolist())
# 
# 
# #plot histograms
# nBins =200
# 
# fig10, (ax17, ax18) = plt.subplots(2, 1, figsize=(8,4), sharex=True, sharey=True)
# fig10.suptitle('Nearest Neighbour Distances - all points to all points, frame by frame')
# 
# ax17.hist(distances_RW_ALL_ALL, bins=nBins, label='Random Walk')
# ax18.hist(distances_points_ALL_ALL, bins=nBins, label='Point Data')
# 
# ax17.set_title("Random Walk")
# ax18.set_title("Point data")
# 
# ax17.set(ylabel = "# of observations")
# ax18.set(xlabel="distances (µm)", ylabel = "# of observations")
# 
# #ax17.set_yscale('log')
# #ax18.set_yscale('log')
# ax18.set_xlim([0,5])
# 
# plt.show()
# saveName = savePath + 'ALL-Distances_hist.png'
# plt.savefig(saveName)
# # =============================================================================
# # # plot cumulative histogram
# # fig11 = plt.hist(distances_RW_ALL_ALL, bins=nBins, density=True, histtype='step',
# #                            cumulative=True, label='Random Walk', color='red')
# # 
# # plt.hist(distances_points_ALL_ALL, bins=nBins, density=True, histtype='step',
# #                            cumulative=True, label='Point Data', color='b')
# # 
# # 
# # 
# # plt.legend(loc='upper right')
# # 
# # plt.ylabel("Likelihood of occurence")
# # plt.xlabel("distances (µm)")
# # 
# # plt.yscale('log')
# # plt.xscale('log')
# # 
# # plt.show()
# # =============================================================================
# 
# 
# 
# =============================================================================






