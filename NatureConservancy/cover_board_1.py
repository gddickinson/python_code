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
path = r"C:\Google Drive\Image_Interpretation\PVER Photos\DL006\\"
file = r"IMG_2040.jpg"
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

center_x = int(image_x/2)
center_y = int(image_y/2)

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
for x in range (center_x-500,center_x+500):
    for y in range (center_y-500,center_y+500):
        #pixels with equivalent values
        if image[x,y][b] == image[x,y][g]:
            image_other[x,y] = 255
            image_board[x,y] = 255
            image_equivalent[x,y] = 0
            equivalent_pixel += 1

        #count board pixels
        elif image[x,y][r] > image[x,y][g] and image[x,y][r] > image[x,y][b] and image[x,y][g]/image[x,y][b] > 1.2 and image[x,y][g]/image[x,y][b] < 3 and image[x,y][r]/image[x,y][g] > 1.4 and image[x,y][r]/image[x,y][g] < 2.8:
            
            if image[x,y][r] > 115 and image[x,y][r] < 210 and image[x,y][g] > 40 and image[x,y][g] < 110 and image[x,y][b] > 15 and image[x,y][b] < 75:
                
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

#threshold and find clusters
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
    if region.area >= 50:
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


#####Crop board area based on labeled regions
#
##set up arrays
#cropped_image = np.ones_like(image_original)*255
#cropped_image_other = np.ones_like(image_original)*255
#cropped_image_board = np.ones_like(image_original)*255
#cropped_image_equivalent = np.ones_like(image_original)*255
#
##pixel countvariables  
#cropped_board_pixel = 0
#cropped_other_pixel = 0
#cropped_equivalent_pixel = 0
#
#
# #loop through all pixels in image and set pixel to maximum channel value - count pixels in each channel   
#for x in range (image_x):
#    for y in range (image_y):
#        if x > (centeroid[0]-300) and x < (centeroid[0]+ 300) and y > (centeroid[1] - 225) and y < (centeroid[1] + 225):
#            #pixels with equivalent values
#            if image_original[x,y][b] == image_original[x,y][g]:
#                cropped_image_other[x,y] = 255
#                cropped_image_board[x,y] = 255
#                cropped_image_equivalent[x,y] = 0
#                cropped_equivalent_pixel += 1
#    
#            #count board pixels
#            elif image_original[x,y][r] > image_original[x,y][g] and image_original[x,y][r] > image_original[x,y][b] and image_original[x,y][g]/image_original[x,y][b] > 1.3:
#                
#                if image_original[x,y][r] > 125 and image_original[x,y][r] < 210 and image_original[x,y][g] > 40 and image_original[x,y][g] < 110 and image_original[x,y][b] > 15 and image_original[x,y][b] < 75:
#                    
#                    cropped_image_board[x,y] = 0
#                    cropped_image_other[x,y] = 255
#                    cropped_image_equivalent[x,y] = 255
#                    cropped_board_pixel += 1
#    
#                
#                else:
#                    cropped_image_board[x,y] = 255
#                    cropped_image_other[x,y] = 0
#                    cropped_image_equivalent[x,y] = 255
#                    cropped_other_pixel += 1
#                
#            #count green pixels   
#            elif image_original[x,y][g] > image_original[x,y][r] and image_original[x,y][g] > image_original[x,y][b]:
#                cropped_image_other[x,y] = 0
#                cropped_image_board[x,y] = 255
#                cropped_image_equivalent[x,y] = 255
#                cropped_other_pixel += 1
#    
#            #count blue pixels 
#            elif image_original[x,y][b] > image_original[x,y][r] and image_original[x,y][b] > image_original[x,y][g]:
#                cropped_image_board[x,y] = 255
#                cropped_image_equivalent[x,y] = 255
#                cropped_image_other[x,y] = 0
#                cropped_other_pixel += 1
#            
#            else:
#                cropped_image_other[x,y] = 255
#                cropped_image_board[x,y] = 255
#                cropped_image_equivalent[x,y] = 0
#                cropped_equivalent_pixel += 1
#        
#            
##plot result
#fig2, axes = plt.subplots(2, 2, figsize=(7, 6), sharex=True, sharey=True,
#                         subplot_kw={'adjustable': 'box-forced'})
#ax = axes.ravel()
#
#ax[0].imshow(image_original)
#ax[0].set_title("Original image (# of pixels = %d)" % (image_x * image_y))
#
#ax[1].imshow(cropped_image_equivalent)
#ax[1].set_title("equivalent (# of pixels = %d)" % cropped_equivalent_pixel)
#
#ax[2].imshow(cropped_image_board)
#ax[2].set_title("board (# of pixels = %d)" % cropped_board_pixel)
#
#ax[3].imshow(cropped_image_other)
#ax[3].set_title("other (# of pixels = %d)" % cropped_other_pixel)
#
#for a in ax.ravel():
#    a.axis('off')
#
#fig2.tight_layout()    
#
#print ("-----------------------------")
#print ("cropped board: %.2f" % (cropped_board_pixel/(image_x * image_y)*100), "%")
#print ("cropped blue: %.2f" % (cropped_other_pixel/(image_x * image_y)*100), "%")
#print ("cropped unassigned: %.2f" % (cropped_equivalent_pixel/(image_x * image_y)*100), "%")
#print ("total pixels counted = ", cropped_board_pixel + cropped_other_pixel + cropped_equivalent_pixel)     
#
##threshold and find clusters
#new_image = rgb2gray(cropped_image_board)
#new_image = new_image.astype(np.uint8)
#new_image = np.invert(new_image)
#
## apply threshold
#thresh = threshold_otsu(new_image)
## close holes
#bw = closing(new_image > thresh, square(2))
#
## remove artifacts connected to image border
#cleared = clear_border(bw)
#
## label image regions
#label_image = label(cleared, background=0)
#image_label_overlay = label2rgb(label_image, image=new_image)
#
#fig, ax = plt.subplots(figsize=(10, 6))
#ax.imshow(image_label_overlay)
#
#total_area = 0
#centeroid = (0,0)
#largest_region_area = 0
#
#for region in regionprops(label_image):
#    # take regions with large enough areas
#    if region.area >= 25:
#        area = region.area
#        if area > largest_region_area:
#            centeroid = region.centroid
#            largest_region_area = area
#            
#        # draw rectangle around segmented areas
#        minr, minc, maxr, maxc = region.bbox
#        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
#                                  fill=False, edgecolor='red', linewidth=1)
#        
#        ax.add_patch(rect)
#        total_area += area
#    area = 0
#
#rect2 = mpatches.Circle((centeroid[1],centeroid[0]))
#ax.add_patch(rect2)
#
#
#ax.set_axis_off()
#plt.tight_layout()
#plt.show()

print ("total # of pixels detected in board = ", total_area)