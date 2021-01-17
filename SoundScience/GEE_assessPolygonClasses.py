# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 14:48:14 2018

@author: George
"""

from matplotlib import pyplot as plt
import pandas as pd
import ast
import numpy as np

#pd.set_option('display.column_space', 1)
#pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_row', 20)
pd.set_option('display.width', 150)

#fileName = r'C:\Google Drive\LCR_vegClassification_polygonAssessment_Sentinel2_4Step_MODIS_NAIP\step4.csv'
#saveName = r'C:\Google Drive\LCR_vegClassification_polygonAssessment_Sentinel2_4Step_MODIS_NAIP\step4_result.csv'
#saveNamePercent = r'C:\Google Drive\LCR_vegClassification_polygonAssessment_Sentinel2_4Step_MODIS_NAIP\step4_resultPercent.csv'

fileName = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\robGeorge_polygons_step2_smooth_histo.csv'
saveName = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\robGeorge_polygons_step2_smooth_histo_result.csv'
saveNamePercent = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\robGeorge_polygons_step2_smooth_histo_resultPercent.csv'


df = pd.read_csv(fileName, dtype={'class': int, 'OBJECTID': int})

#convert string to list
histogram = []

for row in df['histogram'].fillna('missing'):
    if 'missing' in row:
        histogram.append(['missing']) 
    else:
        histogram.append(ast.literal_eval(row))

##get main class allocation from histogram
allocatedClasses = []
#
for row in histogram:
    count = 0
    classType = None
    for entry in row:
        if entry == 'missing':
            pass
        else:
            if entry[1] > count:
                classType = int(entry[0])
                count = entry[1]
    
    allocatedClasses.append(classType)        

#compare allocated classes with polygon classTypes
comparison = []
for i in range(len(allocatedClasses)):
    comparison.append([df['OBJECTID'][i],df['vegClass'][i], df['finalClass'][i], allocatedClasses[i], df['finalClass'][i] == allocatedClasses[i], df['histogram'][i]])

#remove polygons that weren't counted
comparisonRemoveExcludedPolygons = []
classList = []
classIndex = []

for row in comparison:
    if row[3] != None:
        comparisonRemoveExcludedPolygons.append(row)
        if row[1] not in classList:
            classList.append(row[1])
            classIndex.append(row[2])

#convert string list to list
for i in range(len(comparisonRemoveExcludedPolygons)):
    comparisonRemoveExcludedPolygons[i][5] = ast.literal_eval(comparisonRemoveExcludedPolygons[i][5])
    
#divide list entries into array
histoArray = np.zeros([len(classList),len(classList)])

for row in comparisonRemoveExcludedPolygons:
    for i in range(len(classList)):
        if classList[i] in row[1]:
            for entry in row[5]:
                histoArray[i,int(entry[0])] = histoArray[i,int(entry[0])] + entry[1]

#convert floats to ints
histoArray = histoArray.astype(int)

#combine and order lists by class number
classList = list(zip(classIndex,classList,histoArray))
classList.sort()

#add names and histograms to dictionaries to aid making dataframe
classDict = {}
classNames = {}

for i in range(len(classList)):
    if classList[i][0] < 10:
        classDict['0' + str(classList[i][0]) + '_' + classList[i][1]] = classList[i][2]
    else:
        classDict[str(classList[i][0]) + '_' + classList[i][1]] = classList[i][2]
    classNames[classList[i][0]] = classList[i][1]

#create dataframe of results
df2 = pd.DataFrame.from_dict(classDict, orient='index')
#df2.rename(columns=classNames, inplace = True)
df2.sort_index(inplace=True)
 
#delete excess marsh catagories (15 and 16)
#df2.drop([15,16], axis=1, inplace = True) #for step 3
print(df2)
df2.to_csv(saveName)

df2sum = df2.sum(axis=1)
df2div = df2.div(df2sum.tolist(), axis=0)
df2perc = df2div.fillna(0).multiply(100).astype(int)
print(df2perc)

df2perc.to_csv(saveNamePercent)



       