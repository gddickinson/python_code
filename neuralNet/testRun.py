# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 17:06:14 2016

@author: George
"""

from scipy.misc import imread
import numpy as np
import os, sys
from neuralNet_withBackProp import *
import pylab as plt
from sklearn import datasets
from scipy import *

if __name__ == '__main__':


###################################################################
#    #test data    
#    #X = features in array
#    X = np.array([[0, 0],
#                  [0, 1],
#                  [1, 0],
#                  [1, 1]])
#
#    #y = labels in vector 
#    y = np.array([[0,0,0,1], [0,0,1,0], [0,1,0,0], [1,0,0,0]])
#    hiddenLayers = 1
##################################################################

###########################################################################
##plant leaf data
##sort of works with 100 hidden layers
#    hiddenLayers = 100
#    path = r"C:\Users\George\Desktop\plant_identifyer\data\RGB"
#    numberOfLabelledImages = 40
#
#    X, y = unrollImages(path, numberOfLabelledImages, blackAndWhite = True)
############################################################################

############################################################################
#handwritten number data
    X = digits.images.reshape((digits.images.shape[0], -1))
    X = X/16

    yVector = []
    for i in digits.target:
        yVector.append(i)
    identityMatrix = eye(10)
 
    y = []
    for i in yVector:
        y.append(identityMatrix[i])
    
    y = np.array(y)
    hiddenLayers = 10    
###########################################################################

    inputLayer = X.shape[1]    
    outputLayer = y.shape[1]

    nn = NeuralNetwork([inputLayer,hiddenLayers,outputLayer])

    nn.fit(X, y, epochs=100000)

    predictionSet = []
    for e in X:
        print(e,nn.predict(e))
        predictionSet.append(nn.predict(e))