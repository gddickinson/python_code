# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 08:16:45 2017

@author: George
"""

import pickle
import math
import numpy as np
import h5py
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.python.framework import ops
from tf_utils import predict_buildings_7layers, convert_to_one_hot
import scipy
from PIL import Image
from scipy import ndimage
import glob
import copy
from scipy import stats
from sklearn.neighbors import KernelDensity

#load parameters
fileNumber = "20171019-103626_7layer"
filename_pickle = r"C:\\Google Drive\\code\\python_code\\tensorFlow\\buildingIdentification\\parameters\\parameter_" + fileNumber

with open(filename_pickle, 'rb') as handle:
    test_parameters = pickle.load(handle)



mapPath = r"D:\\neuralNet_data\\AerialImageDataset\\AerialImageDataset\\test\\mapSections2\\"
dataList = glob.glob(r"D:\neuralNet_data\AerialImageDataset\AerialImageDataset\test\mapSections2\*.jpg")
numberFiles = len(dataList)

num_px = 100
imageVectorSize = num_px * num_px * 3

dataList = []
for i in range(numberFiles):
    dataList.append(mapPath + "IMG-" +str(i) + ".jpg")


#trainList = dataList[0:8000]
testList = dataList[0:numberFiles]

def label(fileName):
    if "notBuilding" in fileName:
        return 0
    return 1

def processImage(fname, num_px):
    image = np.array(ndimage.imread(fname, flatten=False))
    image = scipy.misc.imresize(image, size=(num_px,num_px)).reshape((num_px,num_px,3))
    return image

# Loading the data (cat/non-cat)
X_test_orig = np.array([np.array(processImage(fname, num_px)) for fname in testList])
Y_test_orig = np.array([np.array(label(fname)) for fname in testList])
Y_test_orig = Y_test_orig.reshape(1,Y_test_orig.shape[0])
classes = np.array(('notBuilding','building'), dtype="str")

num_labels = np.size(classes)

# Flatten the training and test images
X_test_flatten = X_test_orig.reshape(X_test_orig.shape[0], -1).T
# Normalize image vectors
X_test = X_test_flatten/255.
# Convert training and test labels to one hot matrices
Y_test = convert_to_one_hot(Y_test_orig, num_labels)


print ("number of test examples = " + str(X_test.shape[1]))
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


image_predictions = predict_buildings_7layers(X_test, test_parameters, X_test.shape[1], imageVectorSize)

array = image_predictions.reshape((100,100))
#array = np.flipud(array)
array = np.uint8(array*255)

#img = Image.open(r"D:\\neuralNet_data\\AerialImageDataset\\AerialImageDataset\\test\\cropped\\IMG-11.jpg")
img = Image.open(r"D:\\neuralNet_data\\AerialImageDataset\\AerialImageDataset\\test\\cropped\\IMG-425.jpg")
img2 = copy.deepcopy(img)
piece = Image.fromarray(array)
img.paste(piece,(50,50))


fig1 = plt.figure(1)
plt.imshow(img)
fig1.show()

fig2 = plt.figure(2)
plt.imshow(img2)
fig2.show()


# =============================================================================
# #cluster analysis
# def getPoints(array):
#     xAns = []
#     yAns = []
#     for x in range(array.shape[0]):
#         for y in range(array.shape[1]):
#             if array[x,y] > 0:
#                 xAns.append(x)
#                 yAns.append(y)
#     return np.array(xAns), np.array(yAns)
# 
# def kde2D(x, y, bandwidth, xbins=100j, ybins=100j, **kwargs): 
#     """Build 2D kernel density estimate (KDE)."""
# 
#     # create grid of sample locations (default: 100x100)
#     xx, yy = np.mgrid[x.min():x.max():xbins, 
#                       y.min():y.max():ybins]
# 
#     xy_sample = np.vstack([yy.ravel(), xx.ravel()]).T
#     xy_train  = np.vstack([y, x]).T
# 
#     kde_skl = KernelDensity(bandwidth=bandwidth, **kwargs)
#     kde_skl.fit(xy_train)
# 
#     # score_samples() returns the log-likelihood of the samples
#     z = np.exp(kde_skl.score_samples(xy_sample))
#     return xx, yy, np.reshape(z, xx.shape)        
# 
# xArray, yArray = getPoints(array)
# kernel = stats.gaussian_kde(xArray,yArray)
# 
# xx, yy, zz = kde2D(xArray,yArray,1.0)
# plt.pcolormesh(xx, yy, zz)
# plt.scatter(xArray, yArray, s=2, facecolor='white')
# =============================================================================
