# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 16:55:38 2016

@author: George
"""

from scipy.misc import imread
import numpy as np
import os, sys
import pylab as plt


def sigmoid(x):
    return 1.0/(1.0 + np.exp(-x))

def sigmoid_prime(x):
    return sigmoid(x)*(1.0-sigmoid(x))

def tanh(x):
    return np.tanh(x)

def tanh_prime(x):
    return 1.0 - x**2

def unrollImages(pathRoot, numberOfLabels, blackAndWhite = False, X_ScaleFactor = 128):

    def flattenImage(filename):
        img = imread(filename, flatten = blackAndWhite)
        img = img.flatten()
        return img
        
    def createXArray(fileList):
        Xarray = list(map(lambda x: flattenImage(x),fileList))
        return Xarray
    
    def createYArray(fileList, numberOfLabels):
        Yarray = list(map(lambda x: (x[x.index('_C')+2:x.index('_C')+4]),fileList))
        identityMatrix = np.identity(numberOfLabels+1)
        Yarray = list(map(lambda x: identityMatrix[int(x)], Yarray))
        return Yarray
    
    def listFilesInDirectory(pathRoot):
        ans = []
        for path, subdirs, files in os.walk(pathRoot):
            for name in files:
                ans.append(os.path.join(path, name))
        return ans
       
    dataSet = listFilesInDirectory(pathRoot)    
    X = np.array(createXArray(dataSet))
    Y = np.array(createYArray(dataSet,numberOfLabels))
    
    return (X-X_ScaleFactor)/X_ScaleFactor, Y

def unrollSingleImage(filename, blackAndWhite = False, X_ScaleFactor = 128):
    #X_ScaleFactor for RGB images with pixel intensities of 0 - 255
    img = imread(filename, flatten = blackAndWhite)
    img = img.flatten()
    return (img-(X_ScaleFactor))/X_ScaleFactor #scaling for gradient descent optimization



class NeuralNetwork:

    def __init__(self, layers, activation='sigmoid'):
        if activation == 'sigmoid':
            self.activation = sigmoid
            self.activation_prime = sigmoid_prime
        elif activation == 'tanh':
            self.activation = tanh
            self.activation_prime = tanh_prime

        # Set weights
        self.weights = []
        # layers = [2,2,1]
        # range of weight values (-1,1)
        # input and hidden layers - random((2+1, 2+1)) : 3 x 3
        for i in range(1, len(layers) - 1):
            r = 2*np.random.random((layers[i-1] + 1, layers[i] + 1)) -1
            self.weights.append(r)
        # output layer - random((2+1, 1)) : 3 x 1
        r = 2*np.random.random( (layers[i] + 1, layers[i+1])) - 1
        self.weights.append(r)

    def fit(self, X, y, learning_rate=0.2, epochs=100000):
        # Add column of ones to X
        # This is to add the bias unit to the input layer
        ones = np.atleast_2d(np.ones(X.shape[0]))
        X = np.concatenate((ones.T, X), axis=1)
         
        for k in range(epochs):
            if k % 10000 == 0: print ('epochs:', k)
            
            i = np.random.randint(X.shape[0])
            a = [X[i]]
            #print(a)
            for l in range(len(self.weights)):
                    dot_value = np.dot(a[l], self.weights[l])
                    activation = self.activation(dot_value)
                    a.append(activation)
            # output layer
            error = y[i] - a[-1]
            deltas = [error * self.activation_prime(a[-1])]

            # we need to begin at the second to last layer 
            # (a layer before the output layer)
            for l in range(len(a) - 2, 0, -1): 
                deltas.append(deltas[-1].dot(self.weights[l].T)*self.activation_prime(a[l]))

            # reverse
            # [level3(output)->level2(hidden)]  => [level2(hidden)->level3(output)]
            deltas.reverse()

            # backpropagation
            # 1. Multiply its output delta and input activation 
            #    to get the gradient of the weight.
            # 2. Subtract a ratio (percentage) of the gradient from the weight.
            for i in range(len(self.weights)):
                layer = np.atleast_2d(a[i])
                delta = np.atleast_2d(deltas[i])
                self.weights[i] += learning_rate * layer.T.dot(delta)

    def predict(self, x): 
        a = np.concatenate((np.ones(1).T, np.array(x)), axis=0)      
        for l in range(0, len(self.weights)):
            a = self.activation(np.dot(a, self.weights[l]))
        return a

    def importWeights(self, newWeights):
        self.weights = newWeights
    
    def saveWeights(self, filename):
        np.save(filename,self.weights)
        print('weights saved')

    def loadWeights(self, filename):
        self.weights = np.load(filename + '.npy')
        print('weights loaded')
        
