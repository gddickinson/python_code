# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 15:44:57 2017

@author: George
"""

# import packages
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import copy

#define path
path = r"C:\Google Drive\Image_Interpretation\PVER Photos\DL005\\"
file = r"IMG_2053.jpg"
filename = path + file
filename2 = path + "result_" + file

#set limits for thresholding by brightness
dark_threshold = 100
light_threshold = 250

#open image file
image = io.imread(filename)

#set up arrays
image_bright_adjusted = copy.deepcopy(image)
image_sky = copy.deepcopy(image)
image_canopy = copy.deepcopy(image)
image_equivalent = copy.deepcopy(image)

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

#pixel count variables  
sky_pixel = 0
canopy_pixel = 0
equivalent_pixel = 0


#loop through all pixels in image and assign brightest pixels to sky and darkest pixels to canopy (by setting colour)
for x in range (image_x):
    for y in range (image_y):
        #remove pixels from sky and add to canopy if below darkness threshold
        if np.mean(image[x,y]) < dark_threshold:
            image_bright_adjusted[x,y] = green
        #make white pixels blue to ensure they are counted
        if np.mean(image[x,y]) > light_threshold:
            image_bright_adjusted[x,y] = blue


#loop through all pixels in image and set pixel to sky or canopy based on colour - count pixels   
for x in range (image_x):
    for y in range (image_y):
        #pixels with equivalent values
        if image_bright_adjusted[x,y][b] == image_bright_adjusted[x,y][g]:
            image_sky[x,y] = 255
            image_canopy[x,y] = 255
            image_equivalent[x,y] = 0
            equivalent_pixel += 1

        #count red canopy pixels
        elif image_bright_adjusted[x,y][r] > image_bright_adjusted[x,y][g] and image_bright_adjusted[x,y][r] > image_bright_adjusted[x,y][b]:
            image_canopy[x,y] = 0
            image_sky[x,y] = 255
            image_equivalent[x,y] = 255
            canopy_pixel += 1
            
        #count green canopy pixels   
        elif image_bright_adjusted[x,y][g] > image_bright_adjusted[x,y][r] and image_bright_adjusted[x,y][g] > image_bright_adjusted[x,y][b]:
            image_sky[x,y] = 255
            image_canopy[x,y] = 0
            image_equivalent[x,y] = 255
            canopy_pixel += 1

        #count blue sky pixels 
        elif image_bright_adjusted[x,y][b] > image_bright_adjusted[x,y][r] and image_bright_adjusted[x,y][b] > image_bright_adjusted[x,y][g]:
            image_canopy[x,y] = 255
            image_equivalent[x,y] = 255
            image_sky[x,y] = 0
            sky_pixel += 1
        
        else:
            image_sky[x,y] = 255
            image_canopy[x,y] = 255
            image_equivalent[x,y] = 0
            equivalent_pixel += 1
            


#plot result
fig, axes = plt.subplots(2, 2, figsize=(7, 6), sharex=True, sharey=True,
                         subplot_kw={'adjustable': 'box-forced'})
ax = axes.ravel()

ax[0].imshow(image)
ax[0].set_title("Original image (# of pixels = %d)" % (image_x * image_y))

ax[1].imshow(image_equivalent)
ax[1].set_title("unassigned (# of pixels = %d)" % equivalent_pixel)

ax[2].imshow(image_sky)
ax[2].set_title("sky (# of pixels = %d)" % sky_pixel)

ax[3].imshow(image_canopy)
ax[3].set_title("canopy (# of pixels = %d)" % canopy_pixel)

for a in ax.ravel():
    a.axis('off')

fig.tight_layout()

print ("sky: %.2f" % (sky_pixel/(image_x * image_y)*100), "%")
print ("canopy: %.2f" % (canopy_pixel/(image_x * image_y)*100), "%")
print ("unassigned: %.2f" % (equivalent_pixel/(image_x * image_y)*100), "%")
print ("total pixels counted = ", sky_pixel + canopy_pixel + equivalent_pixel)
#print ("missing pixels = ", (image_x * image_y)-(sky_pixel + canopy_pixel + equivalent_pixel))

#io.imsave(filename2,image_sky)