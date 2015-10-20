# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 12:47:23 2015

@author: george
"""

import numpy as np
import cv2

face_cascade =cv2.CascadeClassifier('/home/george/opencv/data/haarcascades/haarcascade_frontalface_alt.xml')
if face_cascade.empty(): raise Exception("your face_cascade is empty. are you sure, the path is correct ?")

eye_cascade = cv2.CascadeClassifier('/home/george/opencv/data/haarcascades/haarcascade_eye.xml')
if eye_cascade.empty(): raise Exception("your eye_cascade is empty. are you sure, the path is correct ?")

def playcamera():
    video = cv2.VideoCapture(0)
    
    while(video.isOpened()):
        ret, frame = video.read()
        if frame == None:
            break
    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)        
        
        facedetect(gray)        
        cv2.imshow('Video', gray)    

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()
    return 

def facedetect(gray):
    frame = gray
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        
    return
    
if __name__ == '__main__':
    playcamera()
    cv2.destroyAllWindows()
