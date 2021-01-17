# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 12:20:02 2018

@author: George
"""

from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs
import numpy as np
#import h5py
import matplotlib.pyplot as plt
from PIL import Image
from scipy import ndimage
import copy
import glob, os
from math import sqrt
#from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray


#resultsPath = r"C:\\Google Drive\\code\\python_code\\tensorFlow\\buildingIdentification\\results\\kerasModel_results\\"
#mapPath = r"C:\Users\George\Desktop\testImages\\test5.jpg"

resultsPath = r"C:\\Google Drive\\code\\python_code\\tensorFlow\\buildingIdentification\\results\\kerasModel_results\\"
mapPath = r"C:\Users\George\Desktop\testImages\test4.jpg"


dy = 500
dx = 1500

final = Image.new("F", (int(dx), int(dy)))

os.chdir(resultsPath)
fileList = []
for file in glob.glob("*.txt"):
    fileList.append(file)
    
for file in fileList:
    im = np.genfromtxt(file,delimiter=",") 
    img = Image.fromarray(im)
    posY,posX = file.split("_")[-1].replace(".txt","").split("-")
    final.paste(img, (int(posX)-200, int(posY)-200))
 
startX = 200
endX = startX + (6 * 100)
startY = 200
endY = startY + (6*3 * 100)

num_px = 100


#img = Image.open(mapPath)
mapArray = np.array(ndimage.imread(mapPath, flatten=False))
mapArray = mapArray[startX:endX,startY:endY]
inputMap = Image.fromarray(mapArray)

img2 = copy.deepcopy(inputMap)

img2.paste(final,(int(num_px/2),int(num_px/2)))   
    
fig1 = plt.figure(1)
plt.title("Input image")
plt.imshow(inputMap)
fig1.show()    
    
fig2, ax1 = plt.subplots(1)
plt.title("Neural Net Output")
ax1.imshow(final)
fig2.show()    
    
fig3, ax2 = plt.subplots(1)
plt.title("Neural Net Output")
ax2.imshow(inputMap)
fig3.show()    
    
 
#get pixels that are white
data = final.getdata()
height = 500
width = 500 * 3
pixelList = []

for i in range(height):
    for j in range(width):
        stride = (width*i) + j
        pixelList.append((j, i, data[stride]))

whites = []
for pixel in pixelList:
    if pixel[2] > 0:
        whites.append(pixel[0:2])


whites = [list(elem) for elem in whites]

x_values = [x[0]+50 for x in whites]
y_values = [y[1]+50 for y in whites]

plt.scatter(x_values,y_values,1)

X = np.array(whites)
rec = plt.Rectangle((50,50),500*3,500,linewidth=1,edgecolor='r',facecolor='none')
ax2.add_patch(rec)


#plt.tight_layout()
plt.show()
   
    
