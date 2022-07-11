# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 08:16:45 2017

@author: George
"""

import pickle
#import math
import numpy as np
#import h5py
import matplotlib.pyplot as plt
import tensorflow as tf
#from tensorflow.python.framework import ops
from tf_utils import predict_buildings_6layers, convert_to_one_hot
#import scipy
from PIL import Image
from scipy import ndimage
#import glob
import copy
#from scipy import stats
#from sklearn.neighbors import KernelDensity

#load parameters
fileNumber = "20171018-090446_6layer"
filename_pickle = r"C:\\Google Drive\\code\\python_code\\tensorFlow\\buildingIdentification\\parameters\\parameter_" + fileNumber

with open(filename_pickle, 'rb') as handle:
    test_parameters = pickle.load(handle)


print("layer shapes")
print("W1 = " + str(test_parameters["W1"].shape))
print("b1 = " + str(test_parameters["b1"].shape))
print("W2 = " + str(test_parameters["W2"].shape))
print("b2 = " + str(test_parameters["b2"].shape))
print("W3 = " + str(test_parameters["W3"].shape))
print("b3 = " + str(test_parameters["b3"].shape))
print("W4 = " + str(test_parameters["W4"].shape))
print("b4 = " + str(test_parameters["b4"].shape))
print("W5 = " + str(test_parameters["W5"].shape))
print("b5 = " + str(test_parameters["b5"].shape))  

#load map
#mapPath = r"D:\\neuralNet_data\\AerialImageDataset\\AerialImageDataset\\test\\cropped\\IMG-424.jpg"
#mapPath = r"D:\neuralNet_data\AerialImageDataset\AerialImageDataset\test\images\bellingham19.tif"
mapPath = r"D:\neuralNet_data\AerialImageDataset\AerialImageDataset\test\images\sfo25.tif"
#mapPath = r"D:\neuralNet_data\AerialImageDataset\AerialImageDataset\test\images\tyrol-e18.tif"
mapArray = np.array(ndimage.imread(mapPath, flatten=False))

#reduce map size for large map
startX = 1500
endX = startX + 300
startY = 1500
endY = startY + 300

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
classes = np.array(('notBuilding','building'), dtype="str")

num_labels = np.size(classes)

# Flatten the training and test images
X_test_flatten = X_test_orig.reshape(X_test_orig.shape[0], -1).T
# Normalize image vectors
X_test = X_test_flatten/255.
# Convert training and test labels to one hot matrices
Y_test = convert_to_one_hot(Y_test_orig, num_labels)


print ("number of images to process = " + str(X_test.shape[1]))
print ("X_test shape: " + str(X_test.shape))
print ("Y_test shape: " + str(Y_test.shape))

def create_placeholders(n_x, n_y):
    """
    Creates the placeholders for the tensorflow session.
    
    Arguments:
    n_x -- scalar, size of an image vector (num_px * num_px = 64 * 64 * 3 = 12288)
    n_y -- scalar, number of classes (from 0 to 5, so -> 6)
    
    Returns:
    X -- placeholder for the data input, of shape [n_x, None] and dtype "float"
    Y -- placeholder for the input labels, of shape [n_y, None] and dtype "float"
    
    Tips:
    - You will use None because it let's us be flexible on the number of examples you will for the placeholders.
      In fact, the number of examples during test/train is different.
    """

    ### START CODE HERE ### (approx. 2 lines)
    X = tf.placeholder(tf.float32,shape = [n_x, None])
    Y = tf.placeholder(tf.float32,shape = [n_y, None])
    ### END CODE HERE ###
    
    return X, Y


image_predictions = predict_buildings_6layers(X_test, test_parameters, X_test.shape[1], imageVectorSize)

array = image_predictions.reshape((imgwidth - num_px, imgheight- num_px))
#array = np.flipud(array)
array = np.uint8(array*255)

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
