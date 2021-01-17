# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 09:43:35 2017

@author: George
"""

from PIL import Image
import pickle
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.python.framework import ops
from tf_utils import predict_building


#load parameters
fileNumber = "20171012-072041"
filename_pickle = r"C:\\Google Drive\\code\\python_code\\tensorFlow\\buildingIdentification\\parameters\\parameter_" + fileNumber

with open(filename_pickle, 'rb') as handle:
    test_parameters = pickle.load(handle)

result = []
#mapPath = r"C:\\Google Drive\\code\\python_code\\tensorFlow\\buildingIdentification\\mapSections\\"
num_px = 100
imageVectorSize = num_px * num_px * 3

def crop(im,height,width):
    imgwidth, imgheight = im.size
    for i in range(imgheight-height):
        for j in range(imgwidth-width):
            box = (j, i, (j+1)*width, (i+1)*height)
            yield im.crop(box)



if __name__=='__main__':
    infile=r"D:\\neuralNet_data\\AerialImageDataset\\AerialImageDataset\\test\\cropped\\IMG-21.jpg"
    im = Image.open(infile)
    height=100
    width=100
    start_num=0
    for k,piece in enumerate(crop(im,height,width),start_num):
        img=Image.new('RGB', (height,width), 255)
        img.paste(piece)
        test_image = np.fromstring(img.tobytes(), dtype=np.uint8).reshape((1, num_px*num_px*3)).T
        result.append(predict_building(test_image, test_parameters, imageVectorSize))
        print(k)
        
    array = np.array(result)
    array = array.reshape((100,100))
    array = array*255
    
    fig1 = plt.figure(1)
    plt.imshow(array)
    fig1.show()       
            
        
        
        