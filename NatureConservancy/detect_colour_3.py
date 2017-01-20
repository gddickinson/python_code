# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 15:44:57 2017

@author: George
"""

# import packages
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2hed
from skimage import io
import copy

#define path
path = r"C:\Users\George\Desktop\images\\"
file = r"trees_sky.jpg"
filename = path + file

#open image file
image = io.imread(filename)

#set up arrays
image_red = copy.deepcopy(image)
image_green = copy.deepcopy(image)
image_blue = copy.deepcopy(image)

#set image size variables
image_x, image_y = image.shape[0:2]

#image array index
r = 0
g = 1
b = 2

# colour settings   
red = [255,0,0]
green = [0,255,0]
blue = [0,0,255]
black = [0,0,0]
white = [255,255,255]    

#pixel countvariables  
red_pixel = 0
green_pixel = 0
blue_pixel = 0
equivalent_pixel = 0

 #loop through all pixels in image and set pixel to maximum channel value - count pixels in each channel   
for x in range (image_x):
    for y in range (image_y):
        #count red pixels
        if image[x,y][r] > image[x,y][g] and image[x,y][r] > image[x,y][b]:
            image_red[x,y] = red
            image_green[x,y] = white
            image_blue[x,y] = white
            red_pixel += 1
            
        #count green pixels   
        elif image[x,y][g] > image[x,y][r] and image[x,y][g] > image[x,y][b]:
            image_red[x,y] = white
            image_green[x,y] = green
            image_blue[x,y] = white
            green_pixel += 1

        #count blue pixels 
        elif image[x,y][b] > image[x,y][r] and image[x,y][b] > image[x,y][g]:
            image_red[x,y] = white
            image_green[x,y] = white
            image_blue[x,y] = blue
            blue_pixel += 1
        
        #pixels with equivalent values
        else:
            image_red[x,y] = white
            image_green[x,y] = white
            image_blue[x,y] = white
            equivalent_pixel += 1



#plot result
fig, axes = plt.subplots(2, 2, figsize=(7, 6), sharex=True, sharey=True,
                         subplot_kw={'adjustable': 'box-forced'})
ax = axes.ravel()

ax[0].imshow(image)
ax[0].set_title("Original image (# of pixels = %d)" % (image_x * image_y))

ax[1].imshow(image_red)
ax[1].set_title("red (# of pixels = %d)" % red_pixel)

ax[2].imshow(image_blue)
ax[2].set_title("blue (# of pixels = %d)" % blue_pixel)

ax[3].imshow(image_green)
ax[3].set_title("green (# of pixels = %d)" % green_pixel)

for a in ax.ravel():
    a.axis('off')

fig.tight_layout()