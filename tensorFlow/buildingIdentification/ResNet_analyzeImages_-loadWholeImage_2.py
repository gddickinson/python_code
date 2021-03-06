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

#load model
#fileName = "kerasModel_20171201-001742"
fileName = "kerasModel_20171204-062622"
model_filePath = r"C:\\Google Drive\\code\\python_code\\tensorFlow\\buildingIdentification\\results\\" + fileName

model = load_model(model_filePath)

#load map
#mapPath = r"J:\\neuralNet_data\\AerialImageDataset\\AerialImageDataset\\test\\cropped\\IMG-424.jpg"
mapPath = r"J:\neuralNet_data\AerialImageDataset\AerialImageDataset\test\images\bellingham19.tif"
#mapPath = r"J:\neuralNet_data\AerialImageDataset\AerialImageDataset\test\images\sfo25.tif"
#mapPath = r"J:\neuralNet_data\AerialImageDataset\AerialImageDataset\test\images\tyrol-e18.tif"
mapArray = np.array(ndimage.imread(mapPath, flatten=False))

#reduce map size for large map
startX = 1275
endX = startX + 200
startY = 1275
endY = startY + 200

mapArray = mapArray[startX:endX,startY:endY]
imgwidth, imgheight , colours = mapArray.shape

#split map into sections
dataList = []
num_px = 100
imageVectorSize = num_px * num_px * 3

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



# Loading the data (cat/non-cat)
X_test_orig = np.array(dataList)
Y_test_orig = np.zeros(len(dataList), dtype="int")
Y_test_orig = Y_test_orig.reshape(1,Y_test_orig.shape[0])
classes = np.array(('notBuilding','building','road','car'), dtype="str")

num_labels = np.size(classes)

# Normalize image vectors
X_test = X_test_orig/255.
# Convert training and test labels to one hot matrices
Y_test = convert_to_one_hot(Y_test_orig, num_labels)


print ("number of images to process = " + str(X_test.shape[0]))
print ("X_test shape: " + str(X_test.shape))
print ("Y_test shape: " + str(Y_test.shape))

    
image_predictions = model.predict(X_test, verbose=1)

predict_image = []

# =============================================================================
# for result in image_predictions :
#     if result[0] > result[1]:
#         predict_image.append(0)
#     else:
#         predict_image.append(1)
# =============================================================================

for result in image_predictions :
    if result[1] > result[0] and result[1] > result[2] and result[1] > result[3]:
        predict_image.append(1)
    elif result[2] > result[0] and result[2] > result[1] and result[2] > result[3]:
        predict_image.append(2)
    elif result[3] > result[0] and result[3] > result[1] and result[3] > result[2]:
        predict_image.append(3)
    else:
        predict_image.append(0)
        
        
image_prediction_final = np.array(predict_image)

array = image_prediction_final.reshape((imgwidth - num_px, imgheight- num_px))
#array = np.flipud(array)
array = np.uint8(array*85)

img = Image.open(mapPath)
img = Image.fromarray(mapArray)

img2 = copy.deepcopy(img)

piece = Image.fromarray(array)
img2.paste(piece,(int(num_px/2),int(num_px/2)))


fig1 = plt.figure(1)
plt.title("Input image")
plt.imshow(img)
fig1.show()

fig2 = plt.figure(2)
plt.title("Neural Net Output")
plt.imshow(img2)
fig2.show()



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
