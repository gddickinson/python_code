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

from distutils.version import StrictVersion
import flika
from flika import global_vars as g
from flika.window import Window
from flika.process.file_ import save_file_gui, open_file_gui

from qtpy.QtGui import QColor

flika_version = flika.__version__
if StrictVersion(flika_version) < StrictVersion('0.2.23'):
    from flika.process.BaseProcess import BaseProcess, WindowSelector, SliderLabel, CheckBox
else:
    from flika.utils.BaseProcess import BaseProcess, WindowSelector, SliderLabel, CheckBox

from flika import *
%gui qt
start_flika()


def loadPointData(pointFile,xMin,xMax,yMin,yMax,crop=True, dataType='elements', lagFile=False):   
    #set savepath
    savePath = os.path.splitext(pointFile)[0]
    
    if dataType == 'elements':
        ######## load GABBY's data into DF #################
        pointsDF = pd.read_excel(pointFile)
        #tracksDF = pd.read_excel(trackFile)
        
        #rename ND.t to frame
        pointsDF = pointsDF.rename(columns={"ND.T": "frame"})
        #set first frame to zero to match image stack
        pointsDF["frame"] = pointsDF["frame"]-1
        

    elif dataType == 'thunderstorm':    
        ######### load ThunderSTORM data into DF ############
        pointsDF = pd.read_csv(pointFile)
        pointsDF['frame'] = pointsDF['frame'].astype(int) -1
        pointsDF['PositionX [µm]'] = pointsDF['x [nm]'] / 1000
        pointsDF['PositionY [µm]'] = pointsDF['y [nm]'] / 1000
        pointsDF['Tree ID'] = 0
        pointsDF['Seg.Length [µm]'] = 0

 
    elif dataType == 'flika':    
        ######### load FLIKA pyinsight data into DF ############
        pointsDF = pd.read_csv(pointFile)
        lagDF = pd.read_csv(lagFile,names=['lag'])
        pointsDF['frame'] = pointsDF['frame'].astype(int)
        pointsDF['PositionX [µm]'] = pointsDF['x'] * pixelSize
        pointsDF['PositionY [µm]'] = pointsDF['y'] * pixelSize
        pointsDF['Tree ID'] = pointsDF['track_number']
        pointsDF['Seg.Length [µm]'] = lagDF['lag']

    if crop == True:
        #CROP
        pointsDF = pointsDF[(pointsDF['PositionX [µm]'] > xMin) & (pointsDF['PositionX [µm]'] < xMax)]
        pointsDF = pointsDF[(pointsDF['PositionY [µm]'] > yMin) & (pointsDF['PositionY [µm]'] < yMax)]
        
    #get number of tracks
    nTracks = np.max(pointsDF['Tree ID'])
    
    #keep x,y,time values
    points = pointsDF[['PositionX [µm]', 'PositionY [µm]', 'frame', 'Tree ID']]

    #get distribution of segment length from tracks
    segLengths = pointsDF['Seg.Length [µm]'].tolist()
    #remove nans
    segLengths = [x for x in segLengths if np.isnan(x) == False]
    
    maxTime = np.max(pointsDF['frame'])

    return points, nTracks, segLengths, maxTime, savePath


def loadImgData(tiffFile, crop=True, transpose=False, rotateflip=True):
    #load image data
    img = io.imread(tiffFile) 
    
    if transpose == True:
        #reshape to x,y,t
        img = np.transpose(img,(1,2,0))
    
    if crop == True:
        #img = img[int(xMin/pixelSize) : int(xMax/pixelSize), int(yMin/pixelSize) : int(yMax/pixelSize), :]
        img = img[:, int(yMin/pixelSize) : int(yMax/pixelSize), int(xMin/pixelSize) : int(xMax/pixelSize)] 
    
    if rotateflip == True:
        #rotate and flip for flika
        img = img[:,:,::-1]
        img = np.rot90(img, k=1, axes=(1,2))
    
    return img


def plotLagHist(segLengths, bins=100, savePath = 'None', exptName = ''):
    #plot histogram of lag times
    fig0, ax0 = plt.subplots(figsize=(12,4),)
    ax0.hist(segLengths, bins = bins)
    ax0.set_title("Segment Lengths")    
    ax0.set(ylabel='# of observations')
    ax0.set(xlabel='length [µm]')
    
    #save analysis
    if savePath != "None":
        saveName = savePath + '_Lags_data.csv'
        df = pd.DataFrame(segLengths,
                       columns =[exptName + '_lags'])
        df.to_csv(saveName)
    return


#tracksDF['average track length'] = tracksDF['Length [µm]']/tracksDF['No.Segments']
#distances = tracksDF['average track length']

#fig0, ax0 = plt.subplots(1, 2, figsize=(12,4), sharex=False, sharey=False)
#ax0[0].hist(distances, bins = 50)



def randomWalkSim(points, maxTime):
    #filter df for points at time 0
    minTime = np.min(points['frame'])
    pointsTime_0 = points[points['frame'] == minTime] 
    
    #plt.scatter(pointsTime_0['PositionX [µm]'], pointsTime_0['PositionY [µm]'])
    
    ###### RANDOM WALK SIMULATION #####
    
    #define random walk point generator
    def getPoint(x, y, radius):
        #generating random points
        
        #360 degree move
        theta=np.random.uniform(0,2*np.pi,1)
        #get x and y
        x=radius*np.cos(theta)+x
        y=radius*np.sin(theta)+y
        
# =============================================================================
#         #just up, down, left, right
#         directions = ["UP", "DOWN", "LEFT", "RIGHT"]
#         step = random.choice(directions)
#         
#         # Move the object according to the direction
#         if step == "RIGHT":
#             x = x + radius
#             y= y
#         elif step == "LEFT":
#             x = x - radius
#             y = y
#         elif step == "UP":
#             x = x
#             y = y + radius
#         elif step == "DOWN":
#             x = x
#             y = y - radius  
# =============================================================================
        
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
            newDF['frame'] = i
            pointsTime_0 = pointsTime_0.append(newDF)
        else:
            newPositions = map(getPoint, newDF['PositionX [µm]'],newDF['PositionY [µm]'],randomDistances)
            newPositions_list = np.array(list(newPositions))
            d = {'PositionX [µm]' : newPositions_list[:,0].tolist(),
                 'PositionY [µm]' : newPositions_list[:,1].tolist(),
                 'ID' : ID_list}
            #append to pointsTime_0 df
            newDF = pd.DataFrame(data=d)
            newDF['frame'] = i
            pointsTime_0 = pointsTime_0.append(newDF)
    
    
    #plot all points    
    #plt.scatter(pointsTime_0['PositionX [µm]'], pointsTime_0['PositionY [µm]'])
    #plot some point data
    return pointsTime_0


def plotDataOnStack(img, points, pixelSize, crop=True):
    #plot point data on tiff stack
    
    pointWindow = Window(img)
        
    points_byFrame = points[['frame','PositionX [µm]','PositionY [µm]']]
    points_byFrame['PositionX [µm]'] = points_byFrame['PositionX [µm]'] * (1/pixelSize)
    points_byFrame['PositionY [µm]'] = points_byFrame['PositionY [µm]'] * (1/pixelSize)
    #points_byFrame['point_color'] = QColor(g.m.settings['point_color'])
    #points_byFrame['point_size'] = g.m.settings['point_size']
    pointArray = points_byFrame.to_numpy()
    
    pointWindow.scatterPoints = [[] for _ in np.arange(pointWindow.mt)]
    
    if crop == True:
        #for cropped image
        offsetX = xMin * (1/pixelSize)
        offsetY = yMin * (1/pixelSize)

    else:
        #no offset for FLIKA data
        offsetX = 0
        offsetY = 0
    
    for pt in pointArray:
        t = int(pt[0])
        if pointWindow.mt == 1:
            t = 0
        pointSize = g.m.settings['point_size']
        pointColor = QColor(g.m.settings['point_color'])
        #position = [pt[1]+(.5* (1/pixelSize)), pt[2]+(.5* (1/pixelSize)), pointColor, pointSize]
        position = [pt[1]-offsetX, pt[2]-offsetY, pointColor, pointSize]    
        pointWindow.scatterPoints[t].append(position)
    pointWindow.updateindex()


def plotTracks(pointsTime_0,points, xMin,xMax,yMin,yMax, crop=True):
    fig1, (ax1,ax2) = plt.subplots(1, 2, figsize=(12,4), sharex=True, sharey=True)
    points_rw  = pointsTime_0.rename(columns={"PositionX [µm]": "x", "PositionY [µm]": "y", "Time [s]": "time"})
    groups_rWalk = points_rw.groupby('ID')
    for name, group in groups_rWalk:
        ax1.plot(group.x * (1/pixelSize), group.y * (1/pixelSize), marker='.', linestyle='-', markersize=3, label=name)
    
    points_points  = points.rename(columns={"PositionX [µm]": "x", "PositionY [µm]": "y", "Tree ID": "ID", "Time [s]": "time"})
    groups_points = points_points.groupby('ID')
    for name, group in groups_points:
        ax2.plot(group.x * (1/pixelSize), group.y * (1/pixelSize), marker='.', linestyle='-', markersize=3, label=name)
    
    ax1.set_title("Random Walk")
    ax2.set_title("Point data")
    
    xaxisMin = int(np.min([points['PositionX [µm]'], points['PositionY [µm]']])* (1/pixelSize))
    xaxisMax = int(np.max([points['PositionX [µm]'], points['PositionY [µm]']])* (1/pixelSize))
    yaxisMin = int(np.min([points['PositionX [µm]'], points['PositionY [µm]']])* (1/pixelSize))
    yaxisMax = int(np.max([points['PositionX [µm]'], points['PositionY [µm]']])* (1/pixelSize))


    if crop == True:
        xaxisMin = xaxisMin - (xMin * (1/pixelSize))
        xaxisMax = xaxisMax - (xMin * (1/pixelSize))
        yaxisMin = yaxisMin - (yMin * (1/pixelSize))
        yaxisMax = yaxisMax - (yMin * (1/pixelSize))
    
    ax1.set_xlim(xaxisMin,xaxisMax)
    ax1.set_ylim(yaxisMin,yaxisMax)
    ax2.set_xlim(xaxisMin,xaxisMax)
    ax2.set_ylim(yaxisMin,yaxisMax)
        
    ax1.set(xlabel='PositionX [pixels]')
    ax1.set(ylabel='PositionY [pixels]')
    ax2.set(xlabel='PositionX [pixels]')
    ax2.set(ylabel='PositionY [pixels]')
    #plt.show()





def updateablePlotPoints(points,pointsTime_0):
    #plot updateable graph (works for 1 point, use groups to plot all points)
    fig, axs = plt.subplots(1, 2, figsize=(10,4), sharex=True, sharey=True)
    plt.subplots_adjust(left=0.25, bottom=0.25)
    
    #points by time
    points_byTime = points.groupby('frame')
    #RW by time
    RW_byTime = pointsTime_0.groupby('frame')
    
    #get points index (times in s not frames)
    RWGroupIndex = list(RW_byTime.groups)
    pointsGroupIndex = list(points_byTime.groups)
    
    #plot time 0
    RW_time = RW_byTime.get_group(RWGroupIndex[0])
    points_time = points_byTime.get_group(pointsGroupIndex[0])
    
    axs[0].scatter(RW_time['PositionX [µm]']* (1/pixelSize), RW_time['PositionY [µm]']* (1/pixelSize))
    axs[1].scatter(points_time['PositionX [µm]']* (1/pixelSize), points_time['PositionY [µm]']* (1/pixelSize))
    #axs[2].imshow(img[:,:,0])
    
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
        #axs[2].imshow(img[:,:,ind])
        
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


#define funcitons for NN
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
  

def NNtoAllPoints(pointsTime_0, points, savePath, exptName = ''):
    #select columns
    testData_df = pointsTime_0[['PositionX [µm]','PositionY [µm]']]
    trainData_df = pointsTime_0[['PositionX [µm]','PositionY [µm]']]
    
    #nearest neighbour
    distances_RW, trainData_indexes_RW = getNearestNeighbors(trainData_df.to_numpy(),testData_df.to_numpy())
    
    #get distances not to self
    nnDist_rWalk = distances_RW[:,1]
    #filter out zero distances
    mask = nnDist_rWalk > 0
    nnDist_rWalk_noZeros = nnDist_rWalk[mask] 
    
    
    ###### NEAREST NEIGHBOUR FOR DATASET ######
    
    #select columns
    testData_df = points[['PositionX [µm]','PositionY [µm]']]
    trainData_df = points[['PositionX [µm]','PositionY [µm]']]
    
    #nearest neighbour
    distances_points, trainData_indexes_points = getNearestNeighbors(trainData_df.to_numpy(),testData_df.to_numpy())
    
    #get distances not to self
    nnDist_pointData = distances_points[:,1]
    #filter out zero distances
    mask = nnDist_pointData > 0
    nnDist_pointData_noZeros = nnDist_pointData[mask] 
    
    
    #plot histograms
    
    nBins =100
    
    fig2, (ax3,ax4) = plt.subplots(2, 1, figsize=(12,4), sharex=True)
    fig2.suptitle('Nearest Neighbour Distances')
    
    ax3.hist(nnDist_rWalk, bins=nBins, label='Random Walk')
    ax4.hist(nnDist_pointData, bins=nBins, label='Point Data')
    
    ax3.set_title("Random Walk")
    ax4.set_title("Point data")
    
    ax3.set(ylabel = "# of observations")
    ax4.set(xlabel="distances (µm)", ylabel = "# of observations")
    
    ax3.set_yscale('log')
    ax4.set_yscale('log')
    #ax4.set_ylim([0,300])
    
    plt.show()
    
    # plot the cumulative histogram
    fig3, (ax5,ax6) = plt.subplots(2,1, figsize=(12, 4), sharex=True)
    ax5.hist(nnDist_rWalk, bins=nBins, density=True, histtype='step',
                               cumulative=True, label='Random Walk')
    
    ax6.hist(nnDist_pointData, bins=nBins, density=True, histtype='step',
                               cumulative=True, label='Random Walk')
    
    ax5.set_title("Random Walk")
    ax6.set_title("Point data")
    
    ax5.set(ylabel = "Likelihood of occurence")
    ax6.set(xlabel="distances (µm)", ylabel = "Likelihood of occurence")
    
    #ax5.set_yscale('log')
    #ax6.set_yscale('log')
    
    plt.show()
    
    #save analysis
    saveName = savePath + '_NN-Distances_data.csv'
    df = pd.DataFrame(list(zip(nnDist_rWalk, nnDist_pointData)),
                   columns =[exptName + '_RandomWalk', exptName + '_Points'])
    df.to_csv(saveName)    


def NNbyFrame(pointsTime_0, points, savePath, bins=200, exptName = ''):
    ####NN FOR EACH FRAME Every Point
    #point data
    groups_pointsTime = points.groupby('frame')
    
    distances_points_ALL_ALL = []
    
    for time in tqdm(groups_pointsTime):
        #plt.scatter(time[1]['PositionX [µm]'],time[1]['PositionY [µm]'])
        testData_df = time[1][['PositionX [µm]','PositionY [µm]']]
        trainData_df = time[1][['PositionX [µm]','PositionY [µm]']]
    
        #nearest neighbour
        distances_points_ALL, trainData_indexes_points_ALL= getNearestNeighbors(trainData_df.to_numpy(),testData_df.to_numpy())
    
        #get distances not to self
        nnDist_pointData_ALL = distances_points_ALL[:,1]
        
        distances_points_ALL_ALL.extend(nnDist_pointData_ALL.tolist())
    
    
    #random walk
    groups_RW_Time = pointsTime_0.groupby('frame')
    
    distances_RW_ALL_ALL = []
    
    for time in tqdm(groups_RW_Time):
        #plt.scatter(time[1]['PositionX [µm]'],time[1]['PositionY [µm]'])
        testData_df = time[1][['PositionX [µm]','PositionY [µm]']]
        trainData_df = time[1][['PositionX [µm]','PositionY [µm]']]
    
        #nearest neighbour
        distances_RW_ALL, trainData_indexes_RW_ALL = getNearestNeighbors(trainData_df.to_numpy(),testData_df.to_numpy())
    
        #get distances not to self
        nnDist_RW_ALL = distances_RW_ALL[:,1]
        
        distances_RW_ALL_ALL.extend(nnDist_RW_ALL.tolist())
    
    
    #plot histograms
    nBins = bins
    
    fig8, (ax15,ax16) = plt.subplots(2, 1, figsize=(8,4), sharex=True, sharey=True)
    fig8.suptitle('Nearest Neighbour Distances - all points to all points, frame by frame')
    
    ax15.hist(distances_RW_ALL_ALL, bins=nBins, label='Random Walk')
    ax16.hist(distances_points_ALL_ALL, bins=nBins, label='Point Data')
    
    ax15.set_title("Random Walk")
    ax16.set_title("Point data")
    
    ax15.set(ylabel = "# of observations")
    ax16.set(xlabel="distances (µm)", ylabel = "# of observations")
    
    #ax15.set_yscale('log')
    #ax16.set_yscale('log')
    ax16.set_xlim([0,5])
    
    plt.show()
    saveName = savePath + 'NN-hist.png'
    plt.savefig(saveName)
    # =============================================================================
    # # plot cumulative histogram
    # fig9 = plt.hist(distances_RW_ALL_ALL, bins=nBins, density=True, histtype='step',
    #                            cumulative=True, label='Random Walk', color='red')
    # 
    # plt.hist(distances_points_ALL_ALL, bins=nBins, density=True, histtype='step',
    #                            cumulative=True, label='Point Data', color='b')
    # 
    # 
    # 
    # plt.legend(loc='upper right')
    # 
    # plt.ylabel("Likelihood of occurence")
    # plt.xlabel("distances (µm)")
    # 
    # plt.yscale('log')
    # plt.xscale('log')
    # 
    # plt.show()
    # =============================================================================
    
    #save analysis
    saveName = savePath + '_NN-Distances_AllFrames_data.csv'
    df = pd.DataFrame(list(zip(distances_RW_ALL_ALL, distances_points_ALL_ALL)),
                   columns =[exptName + '_RandomWalk', exptName + '_Points'])
    df.to_csv(saveName)




def AllDistbyFrame(pointsTime_0, points, savePath, exptName = ''):
    #### ALL distances - all points, FOR EACH FRAME
    #point data
    groups_pointsTime = points.groupby('frame')
    
    distances_points_ALL_ALL = []
    
    for time in tqdm(groups_pointsTime):
        #plt.scatter(time[1]['PositionX [µm]'],time[1]['PositionY [µm]'])
        testData_df = time[1][['PositionX [µm]','PositionY [µm]']]
        trainData_df = time[1][['PositionX [µm]','PositionY [µm]']]
    
        #nearest neighbour
        distances_points_ALL, trainData_indexes_points_ALL= getAllDistances(trainData_df.to_numpy(),testData_df.to_numpy(),len(testData_df))
    
        #get distances not to self
        nnDist_pointData_ALL = distances_points_ALL[:,1:].flatten()
        
        distances_points_ALL_ALL.extend(nnDist_pointData_ALL.tolist())
    
    
    #random walk
    groups_RW_Time = pointsTime_0.groupby('frame')
    
    distances_RW_ALL_ALL = []
    
    for time in tqdm(groups_RW_Time):
        #plt.scatter(time[1]['PositionX [µm]'],time[1]['PositionY [µm]'])
        testData_df = time[1][['PositionX [µm]','PositionY [µm]']]
        trainData_df = time[1][['PositionX [µm]','PositionY [µm]']]
    
        #nearest neighbour
        distances_RW_ALL, trainData_indexes_RW_ALL = getAllDistances(trainData_df.to_numpy(),testData_df.to_numpy(),len(testData_df))
    
        #get distances not to self
        nnDist_RW_ALL = distances_RW_ALL[:,1:].flatten()
        
        distances_RW_ALL_ALL.extend(nnDist_RW_ALL.tolist())
    
    
    #plot histograms
    nBins =200
    
    fig10, (ax17, ax18) = plt.subplots(2, 1, figsize=(8,4), sharex=True, sharey=True)
    fig10.suptitle('All Distances - all points to all points, frame by frame')
    
    ax17.hist(distances_RW_ALL_ALL, bins=nBins, label='Random Walk')
    ax18.hist(distances_points_ALL_ALL, bins=nBins, label='Point Data')
    
    ax17.set_title("Random Walk")
    ax18.set_title("Point data")
    
    ax17.set(ylabel = "# of observations")
    ax18.set(xlabel="distances (µm)", ylabel = "# of observations")
    
    #ax17.set_yscale('log')
    #ax18.set_yscale('log')
    ax18.set_xlim([0,5])
    
    plt.show()
    saveName = savePath + 'ALL-Distances_hist.png'
    plt.savefig(saveName)
    # =============================================================================
    # # plot cumulative histogram
    # fig11 = plt.hist(distances_RW_ALL_ALL, bins=nBins, density=True, histtype='step',
    #                            cumulative=True, label='Random Walk', color='red')
    # 
    # plt.hist(distances_points_ALL_ALL, bins=nBins, density=True, histtype='step',
    #                            cumulative=True, label='Point Data', color='b')
    # 
    # 
    # 
    # plt.legend(loc='upper right')
    # 
    # plt.ylabel("Likelihood of occurence")
    # plt.xlabel("distances (µm)")
    # 
    # plt.yscale('log')
    # plt.xscale('log')
    # 
    # plt.show()
    # =============================================================================
    
    #save analysis
    saveName = savePath + '_ALL-Distances_AllFrames_data.csv'
    df = pd.DataFrame(list(zip(distances_RW_ALL_ALL, distances_points_ALL_ALL)),
                   columns =[exptName + '_RandomWalk', exptName + '_Points'])
    df.to_csv(saveName)

########################################################################################################################################
###################################                            RUN ANALYSIS            #################################################
########################################################################################################################################


#Load starting points
#filepaths
# BAPTA DATA
#pointFile = '/Users/george/Desktop/from_Gabby/BAPTA/GB_132_2021_08_11_HTEndothelial_BAPTA_plate1_6_denoised_dataexcel.xlsx'
#xMin,xMax,yMin,yMax = [20,30,30,40]
#trackFile = '/Users/george/Desktop/from_Gabby/BAPTA/GB_132_2021_08_11_HTEndothelial_BAPTA_plate1_6_denoised_trackexcel.xlsx'

# NON-BAPTA DATA
#control
#pointFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_Denoisedai_trackdata.xlsx'
#tiffFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_MMStack_Default.ome - Denoised.tif'
#xMin,xMax,yMin,yMax = [20,30,30,40]

#pointFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_yoda1_3_Denoisedai_trackdata.xlsx'
#tiffFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_yoda1_3_MMStack_Default.ome - Denoised.tif.tif'


#pointFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_2_Denoisedai_trackdata.xlsx'
#tiffFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_2_MMStack_Default.ome - Denoised.tif.tif'


#pointFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_yoda1_2_Denoisedai_trackdata.xlsx'
#tiffFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_yoda1_2_MMStack_Default.ome - Denoised.tif.tif'


#dataType='flika'

#ThunderSTORM
#pointFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_MMStack_Default.ome - Denoised.tif.csv'
#tiffFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_MMStack_Default.ome - Denoised.tif'
#xMin,xMax,yMin,yMax = [20,30,30,40]
#dataType='thunderstorm'

#FLIKA pyinsight
#pointFile = '/Users/george/Desktop/from_Gabby/flika/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_yoda1_3_Denoised_trackMSD.csv'
#tiffFile = '/Users/george/Desktop/from_Gabby/NonBAPTA/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_MMStack_Default.ome - Denoised.tif'
#lagFile = '/Users/george/Desktop/from_Gabby/flika/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_yoda1_3_Denoised_trackMSD_lagHisto.txt'
#xMin,xMax,yMin,yMax = [20,30,30,40]
#dataType='flika'


############################################################
###### ThunderSTORM BAPTA - cropped - tracked with flika
############################################################

# =============================================================================
# exptName = 'Control - BAPTA'
# pointFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedStacks/GB_132_2021_08_11_HTEndothelial_BAPTA_plate1_6_Denoise_ai_new_crop_locs_tracks.csv'
# tiffFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedStacks/GB_132_2021_08_11_HTEndothelial_BAPTA_plate1_6_Denoise_ai_new_crop.tif'
# lagFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedStacks/GB_132_2021_08_11_HTEndothelial_BAPTA_plate1_6_Denoise_ai_new_crop_locs_lagHisto.txt'
# xMin,xMax,yMin,yMax = [0,125,0,125]
# crop = False
# dataType='flika'
# =============================================================================


############################################################
###### ThunderSTORM Non-BAPTA - cropped - tracked with flika
############################################################

exptName = 'Control - Non-BAPTA'
pointFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedStacks/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_MMStack_Default.ome - Denoised_crop_tracks.csv'
tiffFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedStacks/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_MMStack_Default.ome - Denoised_crop.tif'
lagFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedStacks/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_MMStack_Default.ome - Denoised_crop_lagHisto'
xMin,xMax,yMin,yMax = [0,125,0,125]
crop = False
dataType='flika'


# =============================================================================
# exptName = 'Yoda1'
# pointFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedStacks/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_yoda1_3_MMStack_Default.ome - Denoised_crop_locs_tracks.csv'
# tiffFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedStacks/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_yoda1_3_MMStack_Default.ome - Denoised_crop.tif'
# lagFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedStacks/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_yoda1_3_MMStack_Default.ome - Denoised_crop_locs_lagHisto'
# xMin,xMax,yMin,yMax = [0,125,0,125]
# crop = False
# dataType='flika'
# =============================================================================


# =============================================================================
# exptName = 'GoF'
# pointFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedStacks/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_2_MMStack_Default.ome - Denoised_crop_locs_tracks.csv'
# tiffFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedStacks/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_2_MMStack_Default.ome - Denoised_crop.tif'
# lagFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedStacks/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_2_MMStack_Default.ome - Denoised_crop_locs_lagHisto'
# xMin,xMax,yMin,yMax = [0,125,0,125]
# crop = False
# dataType='flika'
# =============================================================================


# =============================================================================
# exptName = 'GoF_Yoda1'
# pointFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedStacks/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_yoda1_2_MMStack_Default.ome - Denoised_crop_locs_tracks.csv'
# tiffFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedStacks/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_yoda1_2_MMStack_Default.ome - Denoised_crop.tif'
# lagFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedStacks/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_yoda1_2_MMStack_Default.ome - Denoised_crop_locs_lagHisto'
# xMin,xMax,yMin,yMax = [0,125,0,125]
# crop = False
# dataType='flika'
# =============================================================================


# =============================================================================
# exptName = 'Simulated_70'
# pointFile = '/Users/george/Desktop/from_Gabby/simulatedParticles/simulated_70_32bit_locs_tracks.csv'
# tiffFile = '/Users/george/Desktop/from_Gabby/simulatedParticles/simulated_70_32bit.tif'
# lagFile = '/Users/george/Desktop/from_Gabby/simulatedParticles/simulated_70_32bit_locs_lagHisto.txt'
# dataType='flika'
# xMin,xMax,yMin,yMax = [0,125,0,125]
# crop = False
# =============================================================================

###########    thunderSTORM Non-BAPTA FILTERED CROPPED    ##########################

# =============================================================================
# exptName = 'Control_bright'
# pointFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_MMStack_Default.ome - Denoised_crop_tracks_bright_tracks.csv'
# tiffFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_MMStack_Default.ome - Denoised_crop.tif'
# lagFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_MMStack_Default.ome - Denoised_crop_tracks_bright_lagHist.csv'
# xMin,xMax,yMin,yMax = [0,125,0,125]
# crop = False
# dataType='flika'
# =============================================================================

# =============================================================================
# exptName = 'Control_dim'
# pointFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_MMStack_Default.ome - Denoised_crop_tracks_dim_tracks.csv'
# tiffFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_MMStack_Default.ome - Denoised_crop.tif'
# lagFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_1_MMStack_Default.ome - Denoised_crop_tracks_dim_lagHisto.csv'
# xMin,xMax,yMin,yMax = [0,125,0,125]
# crop = False
# dataType='flika'
# =============================================================================

# =============================================================================
# exptName = 'Yoda1_bright'
# pointFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_yoda1_3_MMStack_Default.ome - Denoised_crop_locs_tracks_bright_tracks.csv'
# tiffFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_yoda1_3_MMStack_Default.ome - Denoised_crop.tif'
# lagFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_yoda1_3_MMStack_Default.ome - Denoised_crop_locs_tracks_bright_lagHisto'
# xMin,xMax,yMin,yMax = [0,125,0,125]
# crop = False
# dataType='flika'
# =============================================================================

# =============================================================================
# exptName = 'Yoda1_dim'
# pointFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_yoda1_3_MMStack_Default.ome - Denoised_crop_locs_tracks_dim_tracks.csv'
# tiffFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_yoda1_3_MMStack_Default.ome - Denoised_crop.tif'
# lagFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate1_yoda1_3_MMStack_Default.ome - Denoised_crop_locs_tracks_dim_lagHisto'
# xMin,xMax,yMin,yMax = [0,125,0,125]
# crop = False
# dataType='flika'
# =============================================================================

# =============================================================================
# exptName = 'GoF_bright'
# pointFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_2_MMStack_Default.ome - Denoised_crop_locs_tracks_bright_tracks.csv'
# tiffFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_2_MMStack_Default.ome - Denoised_crop.tif'
# lagFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_2_MMStack_Default.ome - Denoised_crop_locs_tracks_bright_lagHisto'
# xMin,xMax,yMin,yMax = [0,125,0,125]
# crop = False
# dataType='flika'
# =============================================================================

# =============================================================================
# exptName = 'GoF_dim'
# pointFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_2_MMStack_Default.ome - Denoised_crop_locs_tracks_dim_tracks.csv'
# tiffFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_2_MMStack_Default.ome - Denoised_crop.tif'
# lagFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_2_MMStack_Default.ome - Denoised_crop_locs_tracks_dim_lagHisto'
# xMin,xMax,yMin,yMax = [0,125,0,125]
# crop = False
# dataType='flika'
# =============================================================================


# =============================================================================
# exptName = 'GoF_Yoda1_bright'
# pointFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_yoda1_2_MMStack_Default.ome - Denoised_crop_locs_tracks_bright_tracks.csv'
# tiffFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_yoda1_2_MMStack_Default.ome - Denoised_crop.tif'
# lagFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_yoda1_2_MMStack_Default.ome - Denoised_crop_locs_tracks_bright_lagHisto'
# xMin,xMax,yMin,yMax = [0,125,0,125]
# crop = False
# dataType='flika'
# =============================================================================


# =============================================================================
# exptName = 'GoF_Yoda1_dim'
# pointFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_yoda1_2_MMStack_Default.ome - Denoised_crop_locs_tracks_dim_tracks.csv'
# tiffFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_yoda1_2_MMStack_Default.ome - Denoised_crop.tif'
# lagFile = '/Users/george/Desktop/from_Gabby/thunderstorm/croppedFiltered/GB_174_2022_04_26_HTEndothelial_NonBapta_plate2_GoF_yoda1_2_MMStack_Default.ome - Denoised_crop_locs_tracks_dim_lagHisto'
# xMin,xMax,yMin,yMax = [0,125,0,125]
# crop = False
# dataType='flika'
# =============================================================================

# =============================================================================
# exptName = 'Simulated_70_bright'
# pointFile = '/Users/george/Desktop/from_Gabby/simulatedParticles/filtered/simulated_70_32bit_locs_tracks_bright_tracks.csv'
# tiffFile = '/Users/george/Desktop/from_Gabby/simulatedParticles/filtered/simulated_70_32bit.tif'
# lagFile = '/Users/george/Desktop/from_Gabby/simulatedParticles/filtered/simulated_70_32bit_locs_tracks_bright_lagHisto.txt'
# dataType='flika'
# xMin,xMax,yMin,yMax = [0,125,0,125]
# crop = False
# =============================================================================


# =============================================================================
# exptName = 'Simulated_70_dim'
# pointFile = '/Users/george/Desktop/from_Gabby/simulatedParticles/filtered/simulated_70_32bit_locs_tracks_dim_tracks.csv'
# tiffFile = '/Users/george/Desktop/from_Gabby/simulatedParticles/filtered/simulated_70_32bit.tif'
# lagFile = '/Users/george/Desktop/from_Gabby/simulatedParticles/filtered/simulated_70_32bit_locs_tracks_dim_lagHisto.txt'
# dataType='flika'
# xMin,xMax,yMin,yMax = [0,125,0,125]
# crop = False
# 
# =============================================================================



###############   RUN ANALYSIS   #####################

#recording options
pixelSize = 0.108

#LOAD DATA
points, nTracks, segLengths, maxTime, savePath = loadPointData(pointFile, xMin,xMax,yMin,yMax,crop=crop, dataType=dataType, lagFile=lagFile)
img = loadImgData(tiffFile, crop=crop, transpose=False, rotateflip=True)

#RW SIM
pointsTime_0 = randomWalkSim(points, maxTime)

#Plots
plotLagHist(segLengths, bins=100, savePath = savePath, exptName = exptName)
plotDataOnStack(img, points, pixelSize, crop=crop)
plotTracks(pointsTime_0,points,xMin,xMax,yMin,yMax,crop=crop)
updateablePlotPoints(points, pointsTime_0)

#NN Analysis
NNtoAllPoints(pointsTime_0,points, savePath, exptName = exptName)
NNbyFrame(pointsTime_0, points, savePath, bins=1000, exptName = exptName)
AllDistbyFrame(pointsTime_0, points, savePath, exptName = exptName)











