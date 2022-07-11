# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 14:36:45 2018

@author: George
"""

import json
from pycm import *
from glob import glob
import pandas as pd
from matplotlib import pyplot as plt

## to get matrix use command -> matrixList[0][1].matrix()

#pandas options (for SVM grid search result display)
pd.set_option('precision',3)
pd.set_option('display.column_space', 12)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_row', 100)
####step1
#path = r'C:\Google Drive\LCR_vegClassification_step1_ATXclass3'
#path = r'C:\Google Drive\LCR_vegClassification_SVM_Step1' #SVM Grid test
#path = r'C:\Google Drive\LCR_vegClassification_Sentinel2'


####step2
#simple classes
#path = r'C:\Google Drive\LCR_vegClassification_step2\simpleClasses'
#path = r'C:\Google Drive\LCR_vegClassification_SVM_NDVI_simpleClasses' #with NDVI
#path = r'C:\Google Drive\LCR_vegClassification_SVM_NDVI_simpleClasses_AXTclass3' #with NDVI ATX class3
#path = r'C:\Google Drive\LCR_vegClassification_Sentinel2_SVM_NDVI_allBands_newRange_simple'
#classList = ['Arrowweed','Marsh','Tamarisk','Willow','Cottonwood-Willow','Mesquite','Mesquite-Tamarisk','Other']

#detailed classes
#path = r'C:\Google Drive\LCR_vegClassification_step2'
#path = r'C:\Google Drive\LCR_vegClassification_SVM' #SVM Grid test
#path = r'C:\Google Drive\LCR_vegClassification_SVM_NVDI_Step2' #NDVI Grid
#path = r'C:\Google Drive\LCR_vegClassification_SVM_NDVI' #NDVI Grid
#path = r'C:\Google Drive\LCR_vegClassification_Sentinel2_SVM_NDVI_allBands_newRange' #NDVI Grid- Sentinel2
#path = r'C:\Google Drive\LCR_vegClassification_Sentinel2_trees'
#classList = ['Arrowweed', 'Atriplex', 'CottonWd','CotWd-Will', 'Creosote', 'Iodinebush', 'Mesquite', 'Mesq-Atx', 'Mesq-Tam', 'Other', 'Tamarisk', 'Tam-Arrow','Tam-Atx','Willow', 'Marsh']

#landsat7 and 2010 report classes
#path = r'C:\Google Drive\LCR_vegClassification2010_Landsat8'
#classList =['AG','ATX','AW','BG','BW','CR','CW','HM','MA','NC','OW','SC','SH','SM','SOW','UD']

#Simple class2 - new trainingPolygons
#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons'
#classList =['Tree', 'Marsh', 'Shrub','Bareground','Water']

#step2 - class3 using random Forest and new trainingPolygons
#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\class_step2_FOREST'
#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\class_step2_SVM'
#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\class_step2_SVM_GRID' #grid search
#classList = ['W','CW_W','CW', 'TAM', 'TAM_AW','TAM_ATX']

#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\classPlus_step2_SVM_GRID'
#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\classPlus_step2_SVM'
#classList = ['W','CW_W','CW', 'TAM', 'TAM_AW','TAM_ATX', 'MQ', 'MQ_TAM', 'AW']

#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\classPlusMarsh_step2_SVM'
#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons'
#classList = ['W','CW_W','CW', 'TAM', 'TAM_AW','TAM_ATX', 'MQ', 'MQ_TAM', 'AW', 'M']

#step3 option 2
#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons' #GRID search
#classList = ['CW','CW_W','CW_TAM','W_EX','W_GOOD', 'W_M', 'W_TAM', 'TAM', 'PV']


#final
#step1
#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\finalRun\4step\step1'
#classList = ['Arrowweed','Marsh','Tamarisk','Willow','CotWd-Will','Mesquite','Mesq-Tam','Other','Bareground','Water']
#step2
#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\finalRun\4step\step2'
#classList = ['W','CW_W','CW', 'TAM', 'TAM_AW','TAM_ATX', 'MQ', 'MQ_TAM', 'AW', 'M']
#step3
#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\finalRun\4step\step3'
#classList = ['W','CW_W','CW', 'TAM', 'TAM_AW','TAM_ATX']
#step3 option 2 or step 4
#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\finalRun\4step\step4'
#classList = ['CW','CW_W','CW_TAM','W_EX','W_GOOD', 'W_M', 'W_TAM', 'TAM', 'PV']

#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\FINAL_Correction_2Step\step1'
#classList = ['CW','CW_W','CW_TAM', 'ATX', 'W', 'W_M', 'W_TAM', 'TAM', 'PV', 'TAM_AW', 'TAM_ATX', 'MQ', 'MQ_TAM', 'AW', 'M', 'MQ_ATX','Other','BareGround','Water']

#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\FINAL_Correction_2Step\step2'
#classList = ['CW','CW_W','CW_TAM', 'ATX', 'W', 'W_M', 'W_TAM', 'TAM', 'PV', 'TAM_AW', 'TAM_ATX', 'MQ', 'MQ_TAM', 'AW', 'M', 'MQ_ATX','Other','BareGround']

#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\FINAL_Correction_combined\step1'
#classList = ['CW','CW_W','CW_TAM', 'ATX', 'W', 'W_M', 'W_TAM', 'TAM', 'PV', 'TAM_AW', 'TAM_ATX', 'MQ', 'MQ_TAM', 'AW', 'M', 'MQ_ATX','Other','BareGround','Water']

#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\FINAL_Correction_combined\step2'
#classList = ['CW','CW_W','CW_TAM', 'ATX', 'W', 'W_M', 'W_TAM', 'TAM', 'PV', 'TAM_AW', 'TAM_ATX', 'MQ', 'MQ_TAM', 'AW', 'M', 'MQ_ATX','Other','BareGround','Water']

path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\FINAL_Correction_2step_simpleClasses\step2'
classList = ['C','CW','W','TAM','OTHER', 'MARSH', 'BG','WATER']

#path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons'
path = r'C:\Google Drive\LCR_vegClassification_newTrainingPolygons\10232018_ConfusionMatirx\step2'
classList = ['CW','TAM','MQ','OTHER', 'HERB', 'BG','WATER']

def getConfusionMatrix(fileName):
    with open(fileName, "r") as read_file:
        data = json.load(read_file)
        matrix = data['features'][0]['properties']['matrix']
        cmDic = {}
        for i in range(1,len(matrix)):
            rowDic = {}
            for y in range(1,len(matrix[i])):
                rowDic[classList[y-1]] = matrix[i][y]                
            cmDic[classList[i-1]] = rowDic        
        return ConfusionMatrix(matrix = cmDic)
    
matrixList = []

for jsonFile in glob(path + "\\*.geojson"):
    #name = jsonFile.split("\\")[-1].split(".")[0].split("_")[-1]
    name = jsonFile.split("\\")[-1].split(".")[0].split("-")[-1] #for SVM grid search
    matrix = getConfusionMatrix(jsonFile)
    #name, matrix, accuracy, error rate, sensitivity (True Positive Rate), specificity (True Negative Rate), precision (Positive Predictive Value), fall-out (False Positive Rate) 
    matrixList.append([name, matrix, matrix.ACC, matrix.ERR, matrix.TPR, matrix.TNR, matrix.PPV, matrix.FPR, matrix.Kappa])

acc_df = pd.DataFrame([row[2] for row in matrixList], index= [row[0] for row in matrixList])
err_df = pd.DataFrame([row[3] for row in matrixList], index= [row[0] for row in matrixList])
tpr_df = pd.DataFrame([row[4] for row in matrixList], index= [row[0] for row in matrixList])
tnr_df = pd.DataFrame([row[5] for row in matrixList], index= [row[0] for row in matrixList])
ppv_df = pd.DataFrame([row[6] for row in matrixList], index= [row[0] for row in matrixList])
fpr_df = pd.DataFrame([row[7] for row in matrixList], index= [row[0] for row in matrixList])
kappa_df = pd.DataFrame([row[8] for row in matrixList], index= [row[0] for row in matrixList])

summaryList = [acc_df.mean(axis=1),err_df.mean(axis=1),tpr_df.mean(axis=1),tnr_df.mean(axis=1),ppv_df.mean(axis=1),fpr_df.mean(axis=1),kappa_df.mean(axis=1)]

summary_df = pd.DataFrame(summaryList, index=['ACC','ERR','TPR','TNR','PPV','FPR', 'KAPPA'])

print("----------------------- Summary Chart ----------------------- \n\n", summary_df, '\n\n--------------------------------------------------------------')

#plt.scatter(summary_df.iloc[[4]].round(3),summary_df.iloc[[5]].round(3))
#plt.xlabel("Precision (PPV)")
#plt.ylabel("Recall (FPR)")
#plt.title("")
#plt.show()