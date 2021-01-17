# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 11:25:51 2018

@author: George
"""

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

from tensorflow import estimator


#load model
#fileName = "kerasModel_20171201-001742"
#fileName = "kerasModel_20171204-062622"
#fileName = "kerasModel_20180221-025551" #40,000 images in training
#fileName = "kerasModel_20180302-024740" #80,000 images in training
#fileName = "kerasModel_20180311-103037" #100,000 images in training + 4,100 notBuilding Idaho examples
fileName = "kerasModel_20180312-083230" #120,000 images in training + 10,600 notBuilding Idaho examples

serving_input_receiver_fn = r"C:\\Google Drive\\code\\python_code\\tensorFlow\\buildingIdentification\\results\\" + fileName

export_dir_base = r"C:\Google Drive\code\python_code\tensorFlow\buildingIdentification\results\kerasModel_exportToGCP" + fileName

estimator.Estimator.export_savedmodel(export_dir_base, serving_input_receiver_fn)