# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 15:44:57 2017

@author: George
"""

# import packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from skimage import io
from skimage.color import rgb2gray
import copy

from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb

#define path
path = r"C:\Users\George\Desktop\images\Image_Interpretation\PVER Photos\DL006\\"
file = r"IMG_2038_test.jpg"
filename = path + file
filename2 = path + "result_" + file
filename3 = path + "result_other_" + file

#open image file
image = io.imread(filename)

#set up arrays
image_original = copy.deepcopy(image)
image_board = copy.deepcopy(image)
image_other = copy.deepcopy(image)
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

#pixel countvariables  
board_pixel = 0
other_pixel = 0
equivalent_pixel = 0

 #loop through all pixels in image and set pixel to maximum channel value - count pixels in each channel   
for x in range (image_x):
    for y in range (image_y):
        #pixels with equivalent values
        if image[x,y][b] == image[x,y][g]:
            image_other[x,y] = 255
            image_board[x,y] = 255
            image_equivalent[x,y] = 0
            equivalent_pixel += 1

        #count board pixels
        elif image[x,y][r] > image[x,y][g] and image[x,y][r] > image[x,y][b]:
            
            if image[x,y][r] > 118 and image[x,y][r] < 205 and image[x,y][g] > 47 and image[x,y][g] < 103 and image[x,y][b] > 22 and image[x,y][b] < 67:
                
                image_board[x,y] = 0
                image_other[x,y] = 255
                image_equivalent[x,y] = 255
                board_pixel += 1

            
            else:
                image_board[x,y] = 255
                image_other[x,y] = 0
                image_equivalent[x,y] = 255
                other_pixel += 1
            
        #count green pixels   
        elif image[x,y][g] > image[x,y][r] and image[x,y][g] > image[x,y][b]:
            image_other[x,y] = 0
            image_board[x,y] = 255
            image_equivalent[x,y] = 255
            other_pixel += 1

        #count blue pixels 
        elif image[x,y][b] > image[x,y][r] and image[x,y][b] > image[x,y][g]:
            image_board[x,y] = 255
            image_equivalent[x,y] = 255
            image_other[x,y] = 0
            other_pixel += 1
        
        else:
            image_other[x,y] = 255
            image_board[x,y] = 255
            image_equivalent[x,y] = 0
            equivalent_pixel += 1


#plot result
fig, axes = plt.subplots(2, 2, figsize=(7, 6), sharex=True, sharey=True,
                         subplot_kw={'adjustable': 'box-forced'})
ax = axes.ravel()

ax[0].imshow(image)
ax[0].set_title("Original image (# of pixels = %d)" % (image_x * image_y))

ax[1].imshow(image_equivalent)
ax[1].set_title("equivalent (# of pixels = %d)" % equivalent_pixel)

ax[2].imshow(image_board)
ax[2].set_title("board (# of pixels = %d)" % board_pixel)

ax[3].imshow(image_other)
ax[3].set_title("other (# of pixels = %d)" % other_pixel)

for a in ax.ravel():
    a.axis('off')

fig.tight_layout()

print ("board: %.2f" % (board_pixel/(image_x * image_y)*100), "%")
print ("blue: %.2f" % (other_pixel/(image_x * image_y)*100), "%")
print ("unassigned: %.2f" % (equivalent_pixel/(image_x * image_y)*100), "%")
print ("total pixels counted = ", board_pixel + other_pixel + equivalent_pixel)
print ("missing pixels = ", (image_x * image_y)-(board_pixel + other_pixel + equivalent_pixel))

#img_gray = rgb2gray(image_board)
#img_gray2 = rgb2gray(image_other)
#io.imsave(filename2,img_gray)
#io.imsave(filename3,img_gray2)


image = rgb2gray(image_board)
image = image.astype(np.uint8)
image = np.invert(image)

# apply threshold
thresh = threshold_otsu(image)
# close holes
bw = closing(image > thresh, square(3))

# remove artifacts connected to image border
cleared = clear_border(bw)

# label image regions
label_image = label(cleared, background=0)
image_label_overlay = label2rgb(label_image, image=image)

fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(image_label_overlay)

total_area = 0
centeroid = (0,0)
largest_region_area = 0

for region in regionprops(label_image):
    # take regions with large enough areas
    if region.area >= 75:
        area = region.area
        if area > largest_region_area:
            centeroid = region.centroid
            largest_region_area = area
            
        # draw rectangle around segmented areas
        minr, minc, maxr, maxc = region.bbox
        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                  fill=False, edgecolor='red', linewidth=1)
        
        ax.add_patch(rect)
        total_area += area
    area = 0

rect2 = mpatches.Circle((centeroid[1],centeroid[0]))
ax.add_patch(rect2)


ax.set_axis_off()
plt.tight_layout()
plt.show()

print ("total # of pixels detected in board = ", total_area)



cropped_image = np.ones_like(image_original)*255
cropped_image_other = np.ones_like(image_original)*255
cropped_image_board = np.ones_like(image_original)*255
cropped_image_equivalent = np.ones_like(image_original)*255

 #loop through all pixels in image and set pixel to maximum channel value - count pixels in each channel   
for x in range (image_x):
    for y in range (image_y):
        if x > (centeroid[0]-140) and x < (centeroid[0]+140) and y > (centeroid[1] -110) and y < (centeroid[1] +110):
            #pixels with equivalent values
            if image_original[x,y][b] == image_original[x,y][g]:
                cropped_image_other[x,y] = 255
                cropped_image_board[x,y] = 255
                cropped_image_equivalent[x,y] = 0
                equivalent_pixel += 1
    
            #count board pixels
            elif image_original[x,y][r] > image_original[x,y][g] and image_original[x,y][r] > image_original[x,y][b]:
                
                if image_original[x,y][r] > 118 and image_original[x,y][r] < 205 and image_original[x,y][g] > 47 and image_original[x,y][g] < 103 and image_original[x,y][b] > 22 and image_original[x,y][b] < 67:
                    
                    cropped_image_board[x,y] = 0
                    cropped_image_other[x,y] = 255
                    cropped_image_equivalent[x,y] = 255
                    board_pixel += 1
    
                
                else:
                    cropped_image_board[x,y] = 255
                    cropped_image_other[x,y] = 0
                    cropped_image_equivalent[x,y] = 255
                    other_pixel += 1
                
            #count green pixels   
            elif image_original[x,y][g] > image_original[x,y][r] and image_original[x,y][g] > image_original[x,y][b]:
                cropped_image_other[x,y] = 0
                cropped_image_board[x,y] = 255
                cropped_image_equivalent[x,y] = 255
                other_pixel += 1
    
            #count blue pixels 
            elif image_original[x,y][b] > image_original[x,y][r] and image_original[x,y][b] > image_original[x,y][g]:
                cropped_image_board[x,y] = 255
                cropped_image_equivalent[x,y] = 255
                cropped_image_other[x,y] = 0
                other_pixel += 1
            
            else:
                cropped_image_other[x,y] = 255
                cropped_image_board[x,y] = 255
                cropped_image_equivalent[x,y] = 0
                equivalent_pixel += 1
        
            
 #plot result
fig2, axes = plt.subplots(2, 2, figsize=(7, 6), sharex=True, sharey=True,
                         subplot_kw={'adjustable': 'box-forced'})
ax = axes.ravel()

ax[0].imshow(image_original)
ax[0].set_title("Original image (# of pixels = %d)" % (image_x * image_y))

ax[1].imshow(cropped_image_equivalent)
ax[1].set_title("equivalent (# of pixels = %d)" % equivalent_pixel)

ax[2].imshow(cropped_image_board)
ax[2].set_title("board (# of pixels = %d)" % board_pixel)

ax[3].imshow(cropped_image_other)
ax[3].set_title("other (# of pixels = %d)" % other_pixel)

for a in ax.ravel():
    a.axis('off')

fig2.tight_layout()           