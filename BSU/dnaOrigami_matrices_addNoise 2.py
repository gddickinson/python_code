# -*- coding: utf-8 -*-
"""
Created on Wed May  2 10:26:19 2018

@author: George
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb
from skimage import io
from skimage.util import random_noise
from skimage.transform import rotate

import glob, os

from tifffile import imread

outpath = r"C:\Users\g_dic\OneDrive\Desktop\BSU_DATA\matrices\unfolded\low\annotations"
inpath = r"C:\Users\g_dic\OneDrive\Desktop\BSU_DATA\matrices\unfolded\low\\"

os.chdir(inpath)
fileList = []
for file in glob.glob("*.tif"):
    fileList.append(file)

boxTL_x = 100
boxTL_y = 100
boxBR_x = 300
boxBR_y = 300

#iterate through tiff files in folder
for infile in fileList:
    image = imread(inpath+infile)
    height,width = image.shape
    
    #generate n rotated noisey images for each tiff
    for i in range(10):
    
        #make noisey image (random amounts of noise)
        rndNoise_amount = np.random.randint(0,9) * 0.001
        rndNoise = np.zeros_like(image)
        rndNoise = random_noise(rndNoise, mode='salt', amount=rndNoise_amount)
        #set rectangle inside boundary box to zero
        rndNoise[boxTL_x:boxBR_x,boxTL_y:boxBR_y] = 0
        #combine image and noise
        rndNoise = image + rndNoise
        
        #rotate image random amount
        rndRotation = np.random.randint(0,360)
        rndNoise = rotate(rndNoise,rndRotation)
        
        #define bounding box
        minr = boxTL_y
        minc = boxTL_x
        maxr = boxBR_y
        maxc = boxBR_x
        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                  fill=False, edgecolor='red', linewidth=2)
        
        
# =============================================================================
         # #plot images
         # fig, axs = plt.subplots(1,2, figsize=(10, 6))
         # axs[0].imshow(image)
         # axs[1].imshow(rndNoise)
         
         # #draw bounding box
         # axs[1].add_patch(rect)
         
         # plt.show()
# =============================================================================
        
        filenameFormated = infile.split(".")[0]+ "_{}.jpg".format(i)
        #save jpg version of rotated noisey image
        io.imsave(filenameFormated,rndNoise)
        
        ###write annotation xml
        
        filename = os.path.join(outpath ,infile.split(".")[0] + "_{}.xml".format(i))
         
        file = open(filename,'w+') 
        
        file.write('<annotation>')
        file.write('\t<filename>%s</filename>' % filenameFormated)
        file.write('\t<size>')
        file.write('\t\t<width>%s</width>' % width)
        file.write('\t\t<height>%s</height>' % height)
        file.write('\t\t<depth>3</depth>')
        file.write('\t</size>')
        file.write('\t<segmented>0</segmented>')
        
        
        file.write('\t<object>')
        file.write('\t\t<name>dnaorigami</name>')
        file.write('\t\t<pose>Unspecified</pose>')
        file.write('\t\t<truncated>0</truncated>')
        file.write('\t\t<difficult>0</difficult>')
        file.write('\t\t<bndbox>')
        
        file.write('\t\t\t<xmin>%s</xmin>' % minc)
        file.write('\t\t\t<ymin>%s</ymin>' % minr)
        file.write('\t\t\t<xmax>%s</xmax>' % maxc)
        file.write('\t\t\t<ymax>%s</ymax>' % maxr)
        
        file.write('\t\t</bndbox>')
        file.write('\t</object>')
        
        
        file.write('</annotation>')
        file.close()
        print("Finished with: " + str(filenameFormated))