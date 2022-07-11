# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 16:19:01 2015

@author: george
"""

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

fgbg = cv2.BackgroundSubtractorMOG()
x=0
while(1):
    
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)

    cv2.imshow('frame',fgmask)
    
    if x > 2:
        x = 0
        fgbg = cv2.BackgroundSubtractorMOG()
    x +=1   
    print(x)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()