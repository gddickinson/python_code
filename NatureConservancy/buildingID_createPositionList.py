# -*- coding: utf-8 -*-
"""
Created on Tue May 15 17:11:02 2018

@author: George
"""

import numpy as np
import glob
from tqdm import tqdm
import matplotlib.pyplot as plt
import json
import pandas as pd
import os
from sklearn.neighbors import NearestNeighbors

#set path
path = r'C:\Users\George\Desktop\custer_thresh_03\\'

#savePath
saveName = path + 'objectList.txt'

#get lists of json file names - create name list striped of '.json'
jsonList = glob.glob(path + "*.json")

#create function to extract data from json & jgw files return list of building positions for file
def getData(jsonFile):
    objectList = []
    fileName = jsonFile.split("\\")[-1].split(".")[0]
    jgwFileName = jsonFile.split('.')[0] + '.JGw'


    #import jgw data
    jgwFile = open(jgwFileName, 'r')
    content = jgwFile.readlines()
    jgwFile.close()
    xOffset = float(content[4])
    yOffset = float(content[5])
    
    
    #import json data
    with open(jsonFile) as json_data:
        jsonD = json.load(json_data)
        #print(d)
    
    #extract values from dict - add offsets
    for objectID in jsonD:
        objectList.append([fileName,
                             objectID.get("label"),
                             objectID.get("confidence"),
                             (objectID.get("bottomright").get('x') + xOffset),
                             (yOffset - objectID.get("bottomright").get('y')),
                             (objectID.get("topleft").get('x') + xOffset),
                             (yOffset - objectID.get("topleft").get('y'))                           
                             ])    
    
    return objectList

#define functions to return centeroid and area of bounding box
def centeroid(x1,y1,x2,y2):
    return ((x1 + x2)/2),((y1 + y2)/2)

def area(x1,y1,x2,y2):
    height = abs(y1-y2)
    width = abs(x1-x2)
    area = height * width
    return area


#iterate through list extracting bounding box coordinates from json files and jgw files for each object- append to new list
objectIDList = []

for file in tqdm(jsonList):
    
    #only process json files containing data
    statInfo = os.stat(file)
    if statInfo.st_size > 3:
    
        fileList = getData(file)
        
        #iterate through file list results - add to new list individually
        for item in fileList:
            #add centeroids and area
            centerX, centerY = centeroid(item[3],item[4],item[5],item[6])
            objectArea = area(item[3],item[4],item[5],item[6])
            
            item.append(centerX)
            item.append(centerY)
            item.append(objectArea)
            
            #filter by confidence values
            if item[2] > 0.3:
                objectIDList.append(item)


#determine distance of centeroid to nearest neighbour
def distance(p1, p2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lon1, lat1 = p1
    lon2, lat2 = p2
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    km = 6367 * c
    return km

#create list of centeroids
centeroidsList = []
for row in objectIDList:
    centeroidsList.append([row[7],row[8]])

#calculate nearest neighbours
print("Working on nearest-neighbour calculation...")
#nbrs = NearestNeighbors(n_neighbors=2, metric='euclidean').fit(centeroidsList) #to use haversine formula  but very slow
nbrs = NearestNeighbors(n_neighbors=2, metric='euclidean').fit(centeroidsList)
distances, indices = nbrs.kneighbors(centeroidsList)
result = distances[:, 1]    
print("Done with calculating distances!")

#add nearest neighbour distance to objectIDList
for i in range(len(objectIDList)):
    objectIDList[i].append(result[i])    
    
#convert objectList to dataframe
labels = ['fileName','label','confidence','botRight_X','botRight_Y','topLeft_X','topLeft_Y','cent_X','cent_Y','area','distNeigh']
df = pd.DataFrame.from_records(objectIDList,columns=labels)


#save df to csv file
df.to_csv(saveName,index_label="ObjectID")
print(saveName + " saved")

