# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 16:19:01 2015

@author: george
"""

import numpy as np
import cv2

history = 10

inputVideo = cv2.VideoCapture(0)
fgbg = cv2.BackgroundSubtractorMOG()

while inputVideo.isOpened():
    retVal, frame = inputVideo.read()

    fgmask = fgbg.apply(frame, learningRate=1.0/history)

    cv2.imshow('Foreground', fgmask)
    cv2.imshow('Original', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break