# -*- coding: utf-8 -*-
"""
Created on Mon May  8 21:37:05 2017

@author: George
"""

import socket
import time
import cv2

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = b"Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

try:
    while True:
        s.send(MESSAGE)
        time.sleep(0.2)

except KeyboardInterrupt:
   pass
    
#data = s.recv(BUFFER_SIZE)
s.close()

#print ("received data:", data)