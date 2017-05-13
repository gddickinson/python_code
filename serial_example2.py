# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:49:16 2017

@author: George
"""

import serial
from time import sleep
import numpy as np

port = "COM3"
ser = serial.Serial(port, 115200, timeout=0)

a = []
b = []
c = []

i=0
while i<3:
    data = ser.read(30)
    ser.flush()
    if len(data) > 0:
        print ('Got:', data)
        if "A" in str(data):
            a.append(int(str(data).split('A')[1].split(")")[0]))
        if "C" in str(data):
            b.append(int(str(data).split('C')[1].split(")")[0]))
        if "C" in str(data):
            c.append(int(str(data).split('C')[1].split(")")[0]))
        i+=1        
    sleep(0.1)

ser.close()

print (np.mean(a))
print (np.mean(b))
print (np.mean(c))