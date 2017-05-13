# -*- coding: utf-8 -*-
"""
Created on Sat May 13 11:07:24 2017

@author: George
"""

import socket
import sys
import serial
import time
import numpy as np

HOST, PORT = "localhost", 9999
#data = " ".join(sys.argv[1:])
#data = "hello"

class Arduino():   
    def __init__(self,Port='COM3',Boud=115200,connState=0): 
        self.parent=self
        self.port=Port
        self.boud=Boud
        self.connState=connState
        self.timeount=1
        self.ser=None
        self.connect()

    def connect(self): 
        try:
            self.ser=serial.Serial(self.port,self.boud,timeout=0.0001)
            self.connState=1
            return [1,'connect']
        except:
            self.connState=0
            return [0,'no hardware found']


    def loadData(self):     
        self.buffer=self.ser.read(1)        
        if (self.buffer!=''):
            try:
                print (self.buffer)
            except Exception:
                pass

ard=Arduino()
while True:
    if ard.connState:
        ard.loadData()
    else:
        print ("Arduino not found")
        break 
    
    def getSonar():    
        i=0
        a =[]
        b = []
        c = []
        while i<2:
            data = ser.read(30)
            if len(data) > 0:
                data = str(data)
                ser.flush()
                if "A" in data:
                    a.append(int(data.split('A')[1].split(")")[0]))
                if "C" in data:
                    b.append(int(data.split('C')[1].split(")")[0]))
                if "C" in data:
                    c.append(int(data.split('C')[1].split(")")[0]))
                i+=1        
            time.sleep(0.01)
        
        return  [np.mean(a),np.mean(b),np.mean(c)]



# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(str.encode(data + "\n"))

    # Receive data from the server and shut down
    received = sock.recv(1024)
finally:
    sock.close()

print ("Sent:     {}".format(data))
print ("Received: {}".format(received))