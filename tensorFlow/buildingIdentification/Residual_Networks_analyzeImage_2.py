import numpy as np
from keras import layers
from keras.layers import Input, Add, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, AveragePooling2D, MaxPooling2D, GlobalMaxPooling2D
from keras.models import Model, load_model
from keras.preprocessing import image
from keras.utils import layer_utils
from keras.utils.data_utils import get_file
from keras.applications.imagenet_utils import preprocess_input
import pydot
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
from keras.utils import plot_model
from resnets_utils import *
from keras.initializers import glorot_uniform
import scipy.misc
from matplotlib.pyplot import imshow
#get_ipython().magic('matplotlib inline')
import time
import keras.backend as K
K.set_image_data_format('channels_last')
K.set_learning_phase(1)


def identity_block(X, f, filters, stage, block):
    """
    Implementation of the identity block as defined in Figure 3
    
    Arguments:
    X -- input tensor of shape (m, n_H_prev, n_W_prev, n_C_prev)
    f -- integer, specifying the shape of the middle CONV's window for the main path
    filters -- python list of integers, defining the number of filters in the CONV layers of the main path
    stage -- integer, used to name the layers, depending on their position in the network
    block -- string/character, used to name the layers, depending on their position in the network
    
    Returns:
    X -- output of the identity block, tensor of shape (n_H, n_W, n_C)
    """
    
    # defining name basis
    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'
    
    # Retrieve Filters
    F1, F2, F3 = filters
    
    # Save the input value. You'll need this later to add back to the main path. 
    X_shortcut = X
    
    # First component of main path
    X = Conv2D(filters = F1, kernel_size = (1, 1), strides = (1,1), padding = 'valid', name = conv_name_base + '2a', kernel_initializer = glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis = 3, name = bn_name_base + '2a')(X)
    X = Activation('relu')(X)
    
    ### START CODE HERE ###
    
    # Second component of main path (≈3 lines)
    X = Conv2D(filters = F2, kernel_size = (f, f), strides = (1,1), padding = 'same', name = conv_name_base + '2b', kernel_initializer = glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis = 3, name = bn_name_base + '2b')(X)
    X = Activation('relu')(X)

    # Third component of main path (≈2 lines)
    X = Conv2D(filters = F3, kernel_size = (1, 1), strides = (1,1), padding = 'valid', name = conv_name_base + '2c', kernel_initializer = glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis = 3, name = bn_name_base + '2c')(X)

    # Final step: Add shortcut value to main path, and pass it through a RELU activation (≈2 lines)
    X = layers.Add()([X_shortcut, X])
    X = Activation('relu')(X)
    
    ### END CODE HERE ###
    
    return X


#tf.reset_default_graph()
#
#with tf.Session() as test:
#    np.random.seed(1)
#    A_prev = tf.placeholder("float", [3, 4, 4, 6])
#    X = np.random.randn(3, 4, 4, 6)
#    A = identity_block(A_prev, f = 2, filters = [2, 4, 6], stage = 1, block = 'a')
#    test.run(tf.global_variables_initializer())
#    out = test.run([A], feed_dict={A_prev: X, K.learning_phase(): 0})
#    print("out = " + str(out[0][1][1][0]))



def convolutional_block(X, f, filters, stage, block, s = 2):
    """
    Implementation of the convolutional block as defined in Figure 4
    
    Arguments:
    X -- input tensor of shape (m, n_H_prev, n_W_prev, n_C_prev)
    f -- integer, specifying the shape of the middle CONV's window for the main path
    filters -- python list of integers, defining the number of filters in the CONV layers of the main path
    stage -- integer, used to name the layers, depending on their position in the network
    block -- string/character, used to name the layers, depending on their position in the network
    s -- Integer, specifying the stride to be used
    
    Returns:
    X -- output of the convolutional block, tensor of shape (n_H, n_W, n_C)
    """
    
    # defining name basis
    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'
    
    # Retrieve Filters
    F1, F2, F3 = filters
    
    # Save the input value
    X_shortcut = X


    ##### MAIN PATH #####
    # First component of main path 
    X = Conv2D(F1, (1, 1), strides = (s,s), name = conv_name_base + '2a', kernel_initializer = glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis = 3, name = bn_name_base + '2a')(X)
    X = Activation('relu')(X)
    
    ### START CODE HERE ###

    # Second component of main path (≈3 lines)
    X = Conv2D(filters = F2, kernel_size = (f, f), strides = (1,1), padding = 'same', name = conv_name_base + '2b', kernel_initializer = glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis = 3, name = bn_name_base + '2b')(X)
    X = Activation('relu')(X)

    # Third component of main path (≈2 lines)
    X = Conv2D(filters = F3, kernel_size = (1, 1), strides = (1,1), padding = 'valid', name = conv_name_base + '2c', kernel_initializer = glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis = 3, name = bn_name_base + '2c')(X)

    ##### SHORTCUT PATH #### (≈2 lines)
    X_shortcut = Conv2D(F3, (1, 1), strides = (s,s), name = conv_name_base + '1', kernel_initializer = glorot_uniform(seed=0))(X_shortcut)
    X_shortcut = BatchNormalization(axis = 3, name = bn_name_base + '1')(X_shortcut)

    # Final step: Add shortcut value to main path, and pass it through a RELU activation (≈2 lines)
    X = layers.Add()([X_shortcut, X])
    X = Activation('relu')(X)
    
    ### END CODE HERE ###
    
    return X

#tf.reset_default_graph()
#
#with tf.Session() as test:
#    np.random.seed(1)
#    A_prev = tf.placeholder("float", [3, 4, 4, 6])
#    X = np.random.randn(3, 4, 4, 6)
#    A = convolutional_block(A_prev, f = 2, filters = [2, 4, 6], stage = 1, block = 'a')
#    test.run(tf.global_variables_initializer())
#    out = test.run([A], feed_dict={A_prev: X, K.learning_phase(): 0})
#    print("out = " + str(out[0][1][1][0]))


def ResNet50(input_shape = (100, 100, 3), classes = 4):
    """
    Implementation of the popular ResNet50 the following architecture:
    CONV2D -> BATCHNORM -> RELU -> MAXPOOL -> CONVBLOCK -> IDBLOCK*2 -> CONVBLOCK -> IDBLOCK*3
    -> CONVBLOCK -> IDBLOCK*5 -> CONVBLOCK -> IDBLOCK*2 -> AVGPOOL -> TOPLAYER

    Arguments:
    input_shape -- shape of the images of the dataset
    classes -- integer, number of classes

    Returns:
    model -- a Model() instance in Keras
    """
    
    # Define the input as a tensor with shape input_shape
    X_input = Input(input_shape)

    
    # Zero-Padding
    X = ZeroPadding2D((3, 3))(X_input)
    
    # Stage 1
    X = Conv2D(100, (7, 7), strides = (2, 2), name = 'conv1', kernel_initializer = glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis = 3, name = 'bn_conv1')(X)
    X = Activation('relu')(X)
    X = MaxPooling2D((3, 3), strides=(2, 2))(X)

    # Stage 2
    X = convolutional_block(X, f = 3, filters = [100, 100, 256], stage = 2, block='a', s = 1)
    X = identity_block(X, 3, [100, 100, 256], stage=2, block='b')
    X = identity_block(X, 3, [100, 100, 256], stage=2, block='c')

    ### START CODE HERE ###

    # Stage 3 (≈4 lines)
    X = convolutional_block(X, f = 3, filters = [128,128,512], stage = 3, block='a', s = 2)
    X = identity_block(X, 3, [128,128,512], stage=3, block='b')
    X = identity_block(X, 3, [128,128,512], stage=3, block='c')
    X = identity_block(X, 3, [128,128,512], stage=3, block='d')

    # Stage 4 (≈6 lines)
    X = convolutional_block(X, f = 3, filters = [256, 256, 1024], stage = 4, block='a', s = 2)
    X = identity_block(X, 3, [256, 256, 1024], stage=4, block='b')
    X = identity_block(X, 3, [256, 256, 1024], stage=4, block='c')
    X = identity_block(X, 3, [256, 256, 1024], stage=4, block='d')
    X = identity_block(X, 3, [256, 256, 1024], stage=4, block='e')
    X = identity_block(X, 3, [256, 256, 1024], stage=4, block='f')

    # Stage 5 (≈3 lines)
    X = convolutional_block(X, f = 3, filters = [512, 512, 2048], stage = 5, block='a', s = 2)
    X = identity_block(X, 3, [512, 512, 2048], stage=5, block='b')
    X = identity_block(X, 3, [512, 512, 2048], stage=5, block='c')

    # AVGPOOL (≈1 line). Use "X = AveragePooling2D(...)(X)"
    X = AveragePooling2D((2, 2), name='avg_pool')(X)
    
    ### END CODE HERE ###

    # output layer
    X = Flatten()(X)
    X = Dense(classes, activation='softmax', name='fc' + str(classes), kernel_initializer = glorot_uniform(seed=0))(X)
    
    
    # Create model
    model = Model(inputs = X_input, outputs = X, name='ResNet50')

    return model


model = ResNet50(input_shape = (100, 100, 3), classes = 4)


# As seen in the Keras Tutorial Notebook, prior training a model, you need to configure the learning process by compiling the model.


model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


# In[ ]:
# The model is now ready to be trained. The only thing you need is a dataset.

##############################################################################################
########################## Load Aerial Data ##################################################
##############################################################################################

from random import shuffle
import glob


num_px = 100

imageVectorSize = num_px * num_px * 3

dataList = glob.glob(r"J:\neuralNet_data\AerialImageDataset\AerialImageDataset\train\labelledImages\*.jpg")
dataList2 = glob.glob(r"J:\neuralNet_data\AerialImageDataset\ISPRS_BENCHMARK_DATASETS\Vaihingen\train\*.jpg")

numberFiles = len(dataList)

#shuffle the dataset
#shuffle(dataList)

print("dataList loaded")


trainingSize = 5000
testSize = 400

trainList = dataList[0:trainingSize]
testList = dataList[trainingSize:trainingSize+testSize]

trainList = trainList + dataList2



def label(fileName):
    if "notBuilding" in fileName:
        return 0
    if "road" in fileName:
        return 2
    if "car" in fileName:
        return 3
    return 1

def processImage(fname, num_px):
    image = scipy.misc.imread(fname)
    image = scipy.misc.imresize(image, size=(num_px,num_px)).reshape((num_px,num_px,3))
    print(fname, sep= ' ', end='', flush=True)

    return image

# Loading the data (cat/non-cat)
X_train_orig = np.array([np.array(processImage(fname, num_px)) for fname in trainList])
Y_train_orig = np.array([np.array(label(fname)) for fname in trainList])
Y_train_orig = Y_train_orig.reshape(1,Y_train_orig.shape[0])
X_test_orig = np.array([np.array(processImage(fname, num_px)) for fname in testList])
Y_test_orig = np.array([np.array(label(fname)) for fname in testList])
Y_test_orig = Y_test_orig.reshape(1,Y_test_orig.shape[0])
classes = np.array(('notBuilding','building','road','car'), dtype="str")

num_labels = np.size(classes)

###########################################################################################

# Flatten the training and test images
#X_train_flatten = X_train_orig.reshape(X_train_orig.shape[0], -1).T
#X_test_flatten = X_test_orig.reshape(X_test_orig.shape[0], -1).T
# Normalize image vectors
X_train = X_train_orig/255.
X_test = X_test_orig/255.
# Convert training and test labels to one hot matrices
Y_train = convert_to_one_hot(Y_train_orig, num_labels).T
Y_test = convert_to_one_hot(Y_test_orig, num_labels).T


print ("number of training examples = " + str(X_train.shape[0]))
print ("number of test examples = " + str(X_test.shape[0]))
print ("X_train shape: " + str(X_train.shape))
print ("Y_train shape: " + str(Y_train.shape))
print ("X_test shape: " + str(X_test.shape))
print ("Y_test shape: " + str(Y_test.shape))


#############################################################################################
#############################################################################################
#############################################################################################

# Let's load the SIGNS Dataset.

# =============================================================================
# #X_train_orig, Y_train_orig, X_test_orig, Y_test_orig, classes = load_dataset()
# 
# ## Normalize image vectors
# #X_train = X_train_orig/255.
# #X_test = X_test_orig/255.
# 
# ## Convert training and test labels to one hot matrices
# #Y_train = convert_to_one_hot(Y_train_orig, 6).T
# #Y_test = convert_to_one_hot(Y_test_orig, 6).T
# #
# #print ("number of training examples = " + str(X_train.shape[0]))
# #print ("number of test examples = " + str(X_test.shape[0]))
# #print ("X_train shape: " + str(X_train.shape))
# #print ("Y_train shape: " + str(Y_train.shape))
# #print ("X_test shape: " + str(X_test.shape))
# #print ("Y_test shape: " + str(Y_test.shape))
# =============================================================================


# In[ ]:
# Run the following cell to train your model on 2 epochs with a batch size of 32. On a CPU it should take you around 5min per epoch. 

model.fit(X_train, Y_train, epochs = 20, batch_size = 32)


# Let's see how this model (trained on only two epochs) performs on the test set.

preds = model.evaluate(X_test, Y_test)
print ("Loss = " + str(preds[0]))
print ("Test Accuracy = " + str(preds[1]))

savePath = r"C:\\Google Drive\\code\\python_code\\tensorFlow\\buildingIdentification\\results\\kerasModel_" +time.strftime("%Y%m%d-%H%M%S")
model.save(savePath)

# For the purpose of this assignment, we've asked you to train the model only for two epochs. You can see that it achieves poor performances. Please go ahead and submit your assignment; to check correctness, the online grader will run your code only for a small number of epochs as well.

# After you have finished this official (graded) part of this assignment, you can also optionally train the ResNet for more iterations, if you want. We get a lot better performance when we train for ~20 epochs, but this will take more than an hour when training on a CPU. 
# 
# Using a GPU, we've trained our own ResNet50 model's weights on the SIGNS dataset. You can load and run our trained model on the test set in the cells below. It may take ≈1min to load the model.


# =============================================================================
# model = load_model('ResNet50.h5') 
# 
# 
# preds = model.evaluate(X_test, Y_test)
# print ("Loss = " + str(preds[0]))
# print ("Test Accuracy = " + str(preds[1]))
# =============================================================================


# ## 4 - Test on your own image (Optional/Ungraded)

# If you wish, you can also take a picture of your own hand and see the output of the model. To do this:
#     1. Click on "File" in the upper bar of this notebook, then click "Open" to go on your Coursera Hub.
#     2. Add your image to this Jupyter Notebook's directory, in the "images" folder
#     3. Write your image's name in the following code
#     4. Run the code and check if the algorithm is right! 

# In[ ]:

#Something not right here - prediction working OK with array of images - but doesn't seem to work with a single image...

img_path = r"J:\neuralNet_data\AerialImageDataset\AerialImageDataset\train\labelledImages\crop_0_1049_building.jpg"

img = image.load_img(img_path, target_size=(100, 100))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)
print('Input image shape:', x.shape)
my_image = scipy.misc.imread(img_path)
imshow(my_image)
print("class prediction vector [p(0), p(1)] = ")

x = np.expand_dims(X_train[1],axis=0)


prediction = model.predict(x)
print(prediction)

if prediction[0][0] > prediction[0][1]:
    print (classes[0])
else:
    print (classes[1])



# You can also print a summary of your model by running the following code.

# In[ ]:

#model.summary()


# Finally, run the code below to visualize your ResNet50. You can also download a .png picture of your model by going to "File -> Open...-> model.png".

# In[ ]:

# =============================================================================
# plot_model(model, to_file='model.png')
# SVG(model_to_dot(model).create(prog='dot', format='svg'))
# =============================================================================
