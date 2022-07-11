# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 08:16:45 2017

@author: George
"""

#import math
import numpy as np
#import h5py
import matplotlib.pyplot as plt
import tensorflow as tf
from resnets_utils import *
from PIL import Image
from scipy import ndimage
import copy
from keras.models import Model, load_model
from tqdm import tqdm
import glob, os


#load model
#fileName = "kerasModel_20171201-001742"
#fileName = "kerasModel_20171204-062622"
#fileName = "kerasModel_20180221-025551" #40,000 images in training
#fileName = "kerasModel_20180302-024740" #80,000 images in training
#fileName = "kerasModel_20180311-103037" #100,000 images in training + 4,100 notBuilding Idaho examples
#fileName = "kerasModel_20180312-083230" #120,000 images in training + 10,600 notBuilding Idaho examples
fileName = "kerasModel_20180317-114850" #120,000 images in training + 10,600 notBuilding Idaho examples + 1648 building Idaho examples

model_filePath = r"C:\\Google Drive\\code\\python_code\\tensorFlow\\buildingIdentification\\results\\" + fileName

model = load_model(model_filePath)
resultsPath = r"C:\\Google Drive\\code\\python_code\\tensorFlow\\buildingIdentification\\results\\kerasModel_results\\"
savePath = r"C:\\Google Drive\\code\\python_code\\tensorFlow\\buildingIdentification\\results\\kerasModel_results\\" + fileName


#load map
#mapPath = r"J:\AerialImageDataset\AerialImageDataset\test\images\tyrol-e10.tif"
#mapPath = r"J:\AerialImageDataset\AerialImageDataset\test\images\innsbruck20.tif"
#mapPath = r"J:\AerialImageDataset\AerialImageDataset\test\images\sfo3.tif"
#mapPath = r"J:\AerialImageDataset\AerialImageDataset\test\images\bellingham19.tif"
#mapPath = r"J:\AerialImageDataset\AerialImageDataset\test\images\sfo25.tif"
#mapPath = r"J:\AerialImageDataset\AerialImageDataset\test\images\tyrol-e18.tif"
#mapPath = r"J:\AerialImageDataset\AerialImageDataset\test\images\tyrol-e28.tif"
#mapPath = r"J:\AerialImageDataset\AerialImageDataset\test\images\bloomington5.tif"
#mapPath = r"J:\AerialImageDataset\AerialImageDataset\test\images\bellingham21.tif"
#mapPath = r"J:\AerialImageDataset\AerialImageDataset\test\images\bloomington23.tif"
mapPath = r"C:\Users\George\Desktop\testImages\test4.jpg"
#mapPath = r"C:\Users\George\Desktop\buildingClassifier\finalClips\NAIP20150.jpg"

#load mapArray from image file
mapArray = np.array(ndimage.imread(mapPath, flatten=False))


# =============================================================================
# ##load image from lat/long coordinates - using imageCapture in resnets_utils
# centerPoint = (-114.318634, 43.522553) #(long,lat)
# zoom = 19   
# NW_lat_long, SE_lat_long = getNWSECorners(centerPoint,zoom)
# result = get_maps_image(NW_lat_long, SE_lat_long, zoom=zoom)
# saveImagePath = r"C:\Users\George\Desktop\testImages\test_lat_long.jpg"
# result.save(saveImagePath,"JPEG")
# mapArray = np.array(result)
# =============================================================================



#get list of arrays
def getDataList(mapArray, startX, endX, startY, endY):
    mapArray = mapArray[startX:endX,startY:endY]
    imgwidth, imgheight , colours = mapArray.shape
    
    #split map into sections
    dataList = []
    num_px = 100
    #imageVectorSize = num_px * num_px * 3
    
    #square maps only
    def crop(mapArray,height,width):
        imgwidth, imgheight , colours = mapArray.shape
        for i in range(imgheight-height):
            for j in range(imgwidth-width):
                yield mapArray[i:i+height, j:j+width]
    
    height=num_px
    width=num_px
    start_num=0
    for k,piece in enumerate(crop(mapArray,height,width),start_num):
        dataList.append(piece)
    return dataList


def getPredictionArray(dataList, savePath, x, y, i):
    
    imgwidth = 200
    imgheight = 200
    num_px = 100
    
    # Loading the data (cat/non-cat)
    X_test_orig = np.array(dataList)
    Y_test_orig = np.zeros(len(dataList), dtype="int")
    Y_test_orig = Y_test_orig.reshape(1,Y_test_orig.shape[0])
    classes = np.array(('notBuilding','building'), dtype="str")
    
    num_labels = np.size(classes)
    
    # Normalize image vectors
    X_test = X_test_orig/255.
    # Convert training and test labels to one hot matrices
    Y_test = convert_to_one_hot(Y_test_orig, num_labels)
    
    
    print ("number of images to process = " + str(X_test.shape[0]))
    print ("X_test shape: " + str(X_test.shape))
    print ("Y_test shape: " + str(Y_test.shape))
    
        
    image_predictions_original = model.predict(X_test, verbose=1)
    
    predict_image = []

##majority vote allocation   
    for result in image_predictions_original :
        if result[0] > result[1]:
            predict_image.append(0)
        else:
            predict_image.append(1)


###  for result in image_predictions_original :
#        if result[1] > 0.75:
#            predict_image.append(1)
#        else:
#            predict_image.append(0)
            
    
    image_predictions = np.array(predict_image)
    
    array = image_predictions.reshape((imgwidth - num_px, imgheight- num_px))
    #array = np.flipud(array)
    array = np.uint8(array*255)
    
    saveFile = savePath + "_array_" + str(i) + "_" + str(x) + "-" + str(y) + ".txt"
    np.savetxt(saveFile, array, delimiter=',')

    return


def displayResults(folderPath):
    os.chdir(folderPath)
    
    fileList = []
    for file in glob.glob("*.txt"):
        fileList.append(file)


    array0 = np.genfromtxt(fileList[0],delimiter=",")
    for i in range(1,5):
        array = np.genfromtxt(fileList[i],delimiter=",")
        array0 = np.hstack((array0,array))

    array1 = np.genfromtxt(fileList[5],delimiter=",")
    for i in range(6,10):
        array = np.genfromtxt(fileList[i],delimiter=",")
        array1 = np.hstack((array1,array))

    array2 = np.genfromtxt(fileList[10],delimiter=",")
    for i in range(11,15):
        array = np.genfromtxt(fileList[i],delimiter=",")
        array2 = np.hstack((array2,array))

    array3 = np.genfromtxt(fileList[15],delimiter=",")
    for i in range(16,20):
        array = np.genfromtxt(fileList[i],delimiter=",")
        array3 = np.hstack((array3,array))

    array4 = np.genfromtxt(fileList[20],delimiter=",")
    for i in range(21,25):
        array = np.genfromtxt(fileList[i],delimiter=",")
        array4 = np.hstack((array4,array))

    imageArray = np.vstack((array0,array1,array2,array3,array4))
    
    img = Image.fromarray(imageArray)
#    plt.figure()
#    plt.imshow(img)
    return img



#reduce map size for large map
startXloc = 200 #actually Y!
#endX = startX + 200
startYloc = 200 #actually X!
#endY = startY + 200

for i in range(3):
    
    for x in tqdm(range(5)):
        print("Run :" + str(x))
        print("----------------")
        startX = startXloc + (x * 100)
        endX = startX + 200
        
        for y in range(5):
            startY = startYloc + (y *100)
            endY = startY + 200
            
            dataList = getDataList(mapArray, startX, endX, startY, endY)
            getPredictionArray(dataList, savePath, startX, startY, i)
            print("-------------")
    startYloc = startYloc + 500
    


### Uncomment to display results
#piece = displayResults(resultsPath)
#
#startX = startXloc
#endX = startX + (6 * 100)
#startY = startYloc
#endY = startY + (6 * 100)
#
#num_px = 100
#
#
##img = Image.open(mapPath)
#mapArray = np.array(ndimage.imread(mapPath, flatten=False))
#mapArray = mapArray[startX:endX,startY:endY]
#img = Image.fromarray(mapArray)
#
#img2 = copy.deepcopy(img)
#
#img2.paste(piece,(int(num_px/2),int(num_px/2)))
#
#
#fig1 = plt.figure(1)
#plt.title("Input image")
#plt.imshow(img)
#fig1.show()
#
#fig2 = plt.figure(2)
#plt.title("Neural Net Output")
#plt.imshow(img2)
#fig2.show()
#
#
##get pixels that are white
#data = piece.getdata()
#height = 500
#width = 500
#pixelList = []
#
#for i in range(height):
#    for j in range(width):
#        stride = (width*i) + j
#        pixelList.append((j, i, data[stride]))
#
#whites = []
#for pixel in pixelList:
#    if pixel[2] > 0:
#        whites.append(pixel[0:2])
#
#
#whites = [list(elem) for elem in whites]
#
#x_values = [x[0] for x in whites]
#y_values = [y[1] for y in whites]
#
#plt.scatter(x_values,y_values)
#
##np.array of white pixels
#X = np.array(whites)



# =============================================================================
# #filter out green-ish from original image
# mapArrayGreen = mapArray[:,:,2]#>155
# mapArrayGreen = mapArrayGreen.astype(float)
# mapArrayGreen = mapArrayGreen[50:200+50,50:200+50]#*255
# 
# meanArray = np.mean(np.array([mapArrayGreen,array]),axis=0)
# 
# meanArray = meanArray[:,:]>80
# 
# img3 = copy.deepcopy(img)
# meanArray = meanArray.astype(float)*255
# piece2 = Image.fromarray(meanArray)
# 
# img3.paste(piece2,(int(num_px/2),int(num_px/2)))
# 
# 
# fig3 = plt.figure(3)
# plt.title("Neural Net averaged with Blue channel Output")
# plt.imshow(img3)
# fig3.show()
# =============================================================================
