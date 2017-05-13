# -*- coding: utf-8 -*-
"""
Created on Sat May 13 11:07:24 2017

@author: George
"""

import socket
import sys

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])
data = "hello"

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