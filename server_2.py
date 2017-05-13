# -*- coding: utf-8 -*-
"""
Created on Mon May  8 21:37:58 2017

@author: George
"""

#!/usr/bin/env python

import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print ('Connection address:', addr)
try:
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print ("received data:", data)
        #conn.send(data)  # echo
except:
    pass
conn.close()