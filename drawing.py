# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 20:58:13 2015

@author: george
"""

import numpy as np
import cv2

# Create a black image
img = np.zeros((512,512,3), np.uint8)

#==============================================================================
# # Draw a diagonal blue line with thickness of 5 px
img2 = cv2.line(img,(0,0),(511,511),(255,0,0),5)
# 
img3 = cv2.rectangle(img,(384,0),(510,128),(0,255,0),3)
# 
img4 = cv2.ellipse(img,(256,256),(100,50),0,0,180,255,-1)
# 
pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
pts = pts.reshape((-1,1,2))
img5 = cv2.polylines(img,[pts],True,(0,255,255))
# 
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2)
#==============================================================================

plt.imshow(img)
plt.imshow(img2)
plt.imshow(img3)
plt.imshow(img4)
plt.imshow(img5)

plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()