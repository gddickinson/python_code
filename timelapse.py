# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 17:19:16 2017

@author: George
"""

import numpy as np
import cv2
import time
import os

# time delay between frames
delay = 2.5

# folder to write to
folder = r'C:\Users\George\Desktop\timelapse'

subfolder = time.strftime("%d-%m-%Y_%I-%M-%S_%p")

newpath = folder + '\\' + subfolder

if not os.path.exists(newpath):
    os.makedirs(newpath)

filename = newpath + '\\' + 'img'

#filetype
fileType = '.tif'
#fileType = '.jpg'

cap = cv2.VideoCapture(0)
# 2304 x 1296 gets me 1280x720
cap.set(4, 2304.0)
cap.set(3, 1296.0)
#print str(cap.get(3)),str(cap.get(4))

ret, frame = cap.read()
count = 0
while(1):
        
    ret, frame = cap.read()
    frame_num = "%08d" % (count,)
    cv2.imwrite(filename + '_' + frame_num + fileType, frame)
    k = cv2.waitKey(1)
    
    if k == ord('q'):
        break   

    count = count + 1
    time.sleep(delay)

cv2.destroyAllWindows()
cap.release()