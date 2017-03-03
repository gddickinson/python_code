# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 18:50:07 2017

@author: George
"""

from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
from skimage.color import label2rgb, rgb2lab
from skimage import io
import copy
import pyqtgraph as pg

filename = r'C:\Users\George\Desktop\testImages\2039_crop.jpg'
image = io.imread(filename)

#copy arrays
image_original = copy.deepcopy(image)
image_red = copy.deepcopy(image)
image_green = copy.deepcopy(image)
image_blue = copy.deepcopy(image)
image_board = copy.deepcopy(image)
image_other = copy.deepcopy(image)

x_pix,y_pix = image.shape[0:2]

board_mean_values = (198,96,60)

colors = OrderedDict({
		"red": (255, 0, 0),
		"green": (0, 255, 0),
		"blue": (0, 0, 255),
       "board": board_mean_values})

lab = np.zeros((len(colors), 1, 3), dtype="uint8")
colorNames = []


# loop over the colors dictionary
for (i, (name, rgb)) in enumerate(colors.items()):
	# update the L*a*b* array and the color names list
	lab[i] = rgb
	colorNames.append(name)
 
# convert the L*a*b* array from the RGB color space
# to L*a*b*
lab = rgb2lab(lab)

#set image size variables
image_x_origin = 0
image_y_origin = 0

#print("origin ",image_x_origin,image_y_origin)

image_x_end = x_pix
image_y_end = y_pix

ans_red = []
ans_green = []
ans_blue = []
ans_board = []
ans_final = []
x_pos = []
y_pos = []

# loop over the known L*a*b* color values
for (i, row) in enumerate(lab):
	# compute the distance between the current L*a*b*
	# color value and the image pixel
    for x in range (image_x_origin,image_x_end):
        for y in range (image_y_origin,image_y_end):
            d = dist.euclidean(row[0], image[x,y])

            if i == 0:
                ans_green.append(d)
            elif i == 1:
                ans_blue.append(d)
            elif i == 2:
                ans_red.append(d)
            elif i ==3:
                ans_board.append(d)
                x_pos.append(x)
                y_pos.append(y)
                ans_final.append(0)


            
for i in range(len(ans_red)):
    if ans_board[i] < ans_green[i] and ans_board[i] < ans_blue[i] and ans_board[i] < ans_red[i]:
        ans_final[i] = 3
    elif ans_red[i] < ans_green[i] and ans_red[i] < ans_blue[i]:
        ans_final[i] = 2
    elif ans_blue[i] < ans_red[i] and ans_blue[i] < ans_green[i]:
        ans_final[i] = 1
    else:
        ans_final[i] = 0

for i in range(len(ans_final)):
    if ans_final[i] == 3:
        image_board[(x_pos[i]),(y_pos[i])] = 0
    else:
        image_board[(x_pos[i]),(y_pos[i])] = 255
        
#plot result
image_board = np.rot90(image_board, k=1)
image_board = np.flipud(image_board)
resultCoverBoard = pg.image(image_board)