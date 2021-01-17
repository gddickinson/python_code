# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 15:33:37 2017

@author: George
"""

#import math
import numpy as np
#import h5py
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.python.framework import ops
from tf_utils import load_dataset, load_dataset_cat, random_mini_batches, convert_to_one_hot, predict_building_7layers, linear_function, sigmoid, cost, one_hot_matrix, ones, create_placeholders
import glob
import scipy
from scipy import ndimage
from random import shuffle
import time

#%matplotlib inline
np.random.seed(1)
#

# Loading the dataset

#HDF5
# =============================================================================
# X_train_orig, Y_train_orig, X_test_orig, Y_test_orig, classes = load_dataset_cat()
# =============================================================================

##############################################################################################

num_px = 100

imageVectorSize = num_px * num_px * 3

dataList = glob.glob(r"D:\neuralNet_data\AerialImageDataset\AerialImageDataset\train\labelledImages\*.jpg")
numberFiles = len(dataList)

shuffle(dataList)

print("dataList loaded")


trainingSize = 10000
testSize = 400

trainList = dataList[0:trainingSize]
testList = dataList[trainingSize:trainingSize+testSize]

def label(fileName):
    if "notBuilding" in fileName:
        return 0
    return 1

def processImage(fname, num_px):
    image = np.array(ndimage.imread(fname, flatten=False))
    image = scipy.misc.imresize(image, size=(num_px,num_px)).reshape((num_px,num_px,3))
    return image

# Loading the data (cat/non-cat)
X_train_orig = np.array([np.array(processImage(fname, num_px)) for fname in trainList])
Y_train_orig = np.array([np.array(label(fname)) for fname in trainList])
Y_train_orig = Y_train_orig.reshape(1,Y_train_orig.shape[0])
X_test_orig = np.array([np.array(processImage(fname, num_px)) for fname in testList])
Y_test_orig = np.array([np.array(label(fname)) for fname in testList])
Y_test_orig = Y_test_orig.reshape(1,Y_test_orig.shape[0])
classes = np.array(('notBuilding','building'), dtype="str")

num_labels = np.size(classes)

###########################################################################################

# Flatten the training and test images
X_train_flatten = X_train_orig.reshape(X_train_orig.shape[0], -1).T
X_test_flatten = X_test_orig.reshape(X_test_orig.shape[0], -1).T
# Normalize image vectors
X_train = X_train_flatten/255.
X_test = X_test_flatten/255.
# Convert training and test labels to one hot matrices
Y_train = convert_to_one_hot(Y_train_orig, num_labels)
Y_test = convert_to_one_hot(Y_test_orig, num_labels)



print ("number of training examples = " + str(X_train.shape[1]))
print ("number of test examples = " + str(X_test.shape[1]))
print ("X_train shape: " + str(X_train.shape))
print ("Y_train shape: " + str(Y_train.shape))
print ("X_test shape: " + str(X_test.shape))
print ("Y_test shape: " + str(Y_test.shape))



X, Y = create_placeholders(imageVectorSize, num_labels)
print ("X = " + str(X))
print ("Y = " + str(Y))


def initialize_parameters():
    """
    Initializes parameters to build a neural network with tensorflow. The shapes are:
                        W1 : [25, 12288]
                        b1 : [25, 1]
                        W2 : [12, 25]
                        b2 : [12, 1]
                        W3 : [6, 12]
                        b3 : [6, 1]
    
    Returns:
    parameters -- a dictionary of tensors containing W1, b1, W2, b2, W3, b3
    """
    
    tf.set_random_seed(1)                   # so that your "random" numbers match ours
        
    ### START CODE HERE ### (approx. 6 lines of code)
    W1 = tf.get_variable("W1", [25,imageVectorSize], initializer = tf.contrib.layers.xavier_initializer(seed = 1))
    b1 = tf.get_variable("b1", [25,1], initializer = tf.zeros_initializer())
    W2 = tf.get_variable("W2", [25,25], initializer = tf.contrib.layers.xavier_initializer(seed = 1))
    b2 = tf.get_variable("b2", [25,1], initializer = tf.zeros_initializer())
    W3 = tf.get_variable("W3", [25,25], initializer = tf.contrib.layers.xavier_initializer(seed = 1))
    b3 = tf.get_variable("b3", [25,1], initializer = tf.zeros_initializer())
    W4 = tf.get_variable("W4", [25,25], initializer = tf.contrib.layers.xavier_initializer(seed = 1))
    b4 = tf.get_variable("b4", [25,1], initializer = tf.zeros_initializer()) 
    W5 = tf.get_variable("W5", [12,25], initializer = tf.contrib.layers.xavier_initializer(seed = 1))
    b5 = tf.get_variable("b5", [12,1], initializer = tf.zeros_initializer())       
    W6 = tf.get_variable("W6", [12,12], initializer = tf.contrib.layers.xavier_initializer(seed = 1))
    b6 = tf.get_variable("b6", [12,1], initializer = tf.zeros_initializer())  
    W7 = tf.get_variable("W7", [num_labels,12], initializer = tf.contrib.layers.xavier_initializer(seed = 1))
    b7 = tf.get_variable("b7", [num_labels,1], initializer = tf.zeros_initializer())
    
    
    ### END CODE HERE ###

    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2,
                  "W3": W3,
                  "b3": b3,
                  "W4": W4,
                  "b4": b4,
                  "W5": W5,
                  "b5": b5,
                  "W6": W6,
                  "b6": b6,                                   
                  "W7": W7,
                  "b7": b7}
    
    return parameters


tf.reset_default_graph()
with tf.Session() as sess:
    parameters = initialize_parameters()
    print("W1 = " + str(parameters["W1"]))
    print("b1 = " + str(parameters["b1"]))
    print("W2 = " + str(parameters["W2"]))
    print("b2 = " + str(parameters["b2"]))
    print("W3 = " + str(parameters["W3"]))
    print("b3 = " + str(parameters["b3"]))
    print("W4 = " + str(parameters["W4"]))
    print("b4 = " + str(parameters["b4"]))
    print("W5 = " + str(parameters["W5"]))
    print("b5 = " + str(parameters["b5"]))     
    print("W6 = " + str(parameters["W6"]))
    print("b6 = " + str(parameters["b6"]))      
    
def forward_propagation(X, parameters):
    """
    Implements the forward propagation for the model: LINEAR -> RELU -> LINEAR -> RELU -> LINEAR -> SOFTMAX
    
    Arguments:
    X -- input dataset placeholder, of shape (input size, number of examples)
    parameters -- python dictionary containing your parameters "W1", "b1", "W2", "b2", "W3", "b3"
                  the shapes are given in initialize_parameters

    Returns:
    Z3 -- the output of the last LINEAR unit
    """
    
    # Retrieve the parameters from the dictionary "parameters" 
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']
    W3 = parameters['W3']
    b3 = parameters['b3']
    W4 = parameters['W4']
    b4 = parameters['b4']
    W5 = parameters['W5']
    b5 = parameters['b5']
    W6 = parameters['W6']
    b6 = parameters['b6']   
    W7 = parameters['W7']
    b7 = parameters['b7']    
    
    ### START CODE HERE ### (approx. 5 lines)              # Numpy Equivalents:
    Z1 = tf.add(tf.matmul(W1,X), b1)                       # Z1 = np.dot(W1, X) + b1
    A1 = tf.nn.relu(Z1)                                    # A1 = relu(Z1)
    Z2 = tf.add(tf.matmul(W2,A1), b2)                      # Z2 = np.dot(W2, a1) + b2
    A2 = tf.nn.relu(Z2)                                    # A2 = relu(Z2)
    Z3 = tf.add(tf.matmul(W3,A2),b3)                       # Z3 = np.dot(W3,Z2) + b3
    A3 = tf.nn.relu(Z3)                                    # A2 = relu(Z2)
    Z4 = tf.add(tf.matmul(W4,A3),b4)                       # Z3 = np.dot(W3,Z2) + b3
    A4 = tf.nn.relu(Z4)                                    # A2 = relu(Z2)
    Z5 = tf.add(tf.matmul(W5,A4),b5)                       # Z3 = np.dot(W3,Z2) + b3
    A5 = tf.nn.relu(Z5)                                    # A2 = relu(Z2)
    Z6 = tf.add(tf.matmul(W6,A5),b6)                       # Z3 = np.dot(W3,Z2) + b3
    A6 = tf.nn.relu(Z6)                                    # A2 = relu(Z2)
    Z7 = tf.add(tf.matmul(W7,A6),b7)                       # Z3 = np.dot(W3,Z2) + b3    
    
    ### END CODE HERE ###
    
    return Z7


tf.reset_default_graph()

with tf.Session() as sess:
    X, Y = create_placeholders(imageVectorSize, num_labels)
    parameters = initialize_parameters()
    Z7 = forward_propagation(X, parameters)
    print("Z7 = " + str(Z7))
    
def compute_cost(Z7, Y):
    """
    Computes the cost
    
    Arguments:
    Z3 -- output of forward propagation (output of the last LINEAR unit), of shape (6, number of examples)
    Y -- "true" labels vector placeholder, same shape as Z3
    
    Returns:
    cost - Tensor of the cost function
    """
    
    # to fit the tensorflow requirement for tf.nn.softmax_cross_entropy_with_logits(...,...)
    logits = tf.transpose(Z7)
    labels = tf.transpose(Y)
    
    ### START CODE HERE ### (1 line of code)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = logits, labels = labels))
    ### END CODE HERE ###
    
    return cost

tf.reset_default_graph()

with tf.Session() as sess:
    X, Y = create_placeholders(imageVectorSize, num_labels)
    parameters = initialize_parameters()
    Z7 = forward_propagation(X, parameters)
    cost = compute_cost(Z7, Y)
    print("cost = " + str(cost))


def model(X_train, Y_train, X_test, Y_test, learning_rate = 0.00005,
          num_epochs = 5000, minibatch_size = 32, print_cost = True):
    """
    Implements a three-layer tensorflow neural network: LINEAR->RELU->LINEAR->RELU->LINEAR->SOFTMAX.
    
    Arguments:
    X_train -- training set, of shape (input size = 12288, number of training examples = 1080)
    Y_train -- test set, of shape (output size = 6, number of training examples = 1080)
    X_test -- training set, of shape (input size = 12288, number of training examples = 120)
    Y_test -- test set, of shape (output size = 6, number of test examples = 120)
    learning_rate -- learning rate of the optimization
    num_epochs -- number of epochs of the optimization loop
    minibatch_size -- size of a minibatch
    print_cost -- True to print the cost every 100 epochs
    
    Returns:
    parameters -- parameters learnt by the model. They can then be used to predict.
    """
    
    ops.reset_default_graph()                         # to be able to rerun the model without overwriting tf variables
    tf.set_random_seed(1)                             # to keep consistent results
    seed = 3                                          # to keep consistent results
    (n_x, m) = X_train.shape                          # (n_x: input size, m : number of examples in the train set)
    n_y = Y_train.shape[0]                            # n_y : output size
    costs = []                                        # To keep track of the cost
    
    # Create Placeholders of shape (n_x, n_y)
    ### START CODE HERE ### (1 line)
    X, Y = create_placeholders(n_x, n_y)
    ### END CODE HERE ###

    # Initialize parameters
    ### START CODE HERE ### (1 line)
    parameters = initialize_parameters()
    ### END CODE HERE ###
    
    # Forward propagation: Build the forward propagation in the tensorflow graph
    ### START CODE HERE ### (1 line)
    Z7 = forward_propagation(X, parameters)
    ### END CODE HERE ###
    
    # Cost function: Add cost function to tensorflow graph
    ### START CODE HERE ### (1 line)
    cost = compute_cost(Z7, Y)
    ### END CODE HERE ###
    
    # Backpropagation: Define the tensorflow optimizer. Use an AdamOptimizer.
    ### START CODE HERE ### (1 line)
    optimizer = tf.train.AdamOptimizer(learning_rate = learning_rate).minimize(cost)
    ### END CODE HERE ###
    
    # Initialize all the variables
    init = tf.global_variables_initializer()

    # Start the session to compute the tensorflow graph
    with tf.Session() as sess:
        
        # Run the initialization
        sess.run(init)
        
        # Do the training loop
        for epoch in range(num_epochs):

            epoch_cost = 0.                       # Defines a cost related to an epoch
            num_minibatches = int(m / minibatch_size) # number of minibatches of size minibatch_size in the train set
            seed = seed + 1
            minibatches = random_mini_batches(X_train, Y_train, minibatch_size, seed)

            for minibatch in minibatches:

                # Select a minibatch
                (minibatch_X, minibatch_Y) = minibatch
                
                # IMPORTANT: The line that runs the graph on a minibatch.
                # Run the session to execute the "optimizer" and the "cost", the feedict should contain a minibatch for (X,Y).
                ### START CODE HERE ### (1 line)
                _ , minibatch_cost = sess.run([optimizer, cost], feed_dict={X: minibatch_X, Y: minibatch_Y})
                ### END CODE HERE ###
                
                epoch_cost += minibatch_cost / num_minibatches

            # Print the cost every epoch
            if print_cost == True and epoch % 100 == 0:
                print ("Cost after epoch %i: %f" % (epoch, epoch_cost))
            if print_cost == True and epoch % 5 == 0:
                costs.append(epoch_cost)
                
        # plot the cost
        f = plt.figure(1)
        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('iterations (per tens)')
        plt.title("Learning rate =" + str(learning_rate))
        f.show()

        # lets save the parameters in a variable
        parameters = sess.run(parameters)
        print ("Parameters have been trained!")

        # Calculate the correct predictions
        correct_prediction = tf.equal(tf.argmax(Z7), tf.argmax(Y))

        # Calculate accuracy on the test set
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

        print ("Train Accuracy:", accuracy.eval({X: X_train, Y: Y_train}))
        print ("Test Accuracy:", accuracy.eval({X: X_test, Y: Y_test}))
        
        return parameters

start_Time = time.time()    
parameters = model(X_train, Y_train, X_test, Y_test)
end_Time = time.time() - start_Time
print ("Run time  = " + str(end_Time))

import scipy
from PIL import Image
from scipy import ndimage

# reprocess your image to fit algorithm.
#fname = "images/" + my_image
fname = r"J:\neuralNet_data\AerialImageDataset\AerialImageDataset\train\labelledImages\crop_117_17_building.jpg"
image = np.array(ndimage.imread(fname, flatten=False))
my_image = scipy.misc.imresize(image, size=(num_px,num_px)).reshape((1, num_px*num_px*3)).T
my_image_prediction = predict_building_7layers(my_image, parameters, imageVectorSize)


g = plt.figure(2)
plt.imshow(scipy.misc.imresize(image, size=(num_px,num_px)))
g.show()
print("Your algorithm predicts: y = " + str(np.squeeze(my_image_prediction)))

import pickle
import time

filename_pickle = r"C:\\Google Drive\\code\\python_code\\tensorFlow\\buildingIdentification\\parameters\\parameter_" +time.strftime("%Y%m%d-%H%M%S") + "_7layer"

with open(filename_pickle, 'wb') as handle:
    pickle.dump(parameters, handle, protocol=pickle.HIGHEST_PROTOCOL)

print("parameter file saved")

with open(filename_pickle, 'rb') as handle:
    test_parameters = pickle.load(handle)















