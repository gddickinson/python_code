# -*- coding: utf-8 -*-
"""
Created on Sun May  7 17:05:27 2017

@author: George
"""
import serial
import io
import serial.tools.list_ports
import time

ports = list(serial.tools.list_ports.comports()) 

def getArduinoSerial(name = "Uno", baudRate=19200, timeOut = 1.1):
    for p in ports:
        if name in p[1]:
            ser = serial.serial_for_url(p[0], baudRate, timeout=timeOut)
            ser_sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
            return ser_sio
        else:
            print("No " + name + " detected")
        return


def getLine(name = "Uno", baudRate=19200, timeout = 1.1):
    serialObject = getArduinoSerial(name = name, baudRate = baudRate, timeOut=timeout)
    line = serialObject.readline()
    return line    

while True:
    print(getLine(name = "Mega", baudRate = 115200, timeout = 1.1))