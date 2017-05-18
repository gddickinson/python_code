# -*- coding: utf-8 -*-
"""
Created on Sat May 13 17:41:59 2017

@author: George
"""
import serial
import numpy as np
import signal
import sys
import time
import socket

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
            print('connected')
            return [1,'connect']
        except:
            self.connState=0
            print('no hardware found')
            return [0,'no hardware found']


    def loadData(self):     
        self.buffer=self.ser.read(1)        
        if (self.buffer!=''):
            try:
                print (self.buffer)
            except Exception:
                pass

    def getSonar(self):    
        a=0
        b=0
        c=0
        self.data=self.ser.read(30)
        if (self.data!=''):
            try:
                self.data = str(self.data)
                self.ser.flush()
                if "A" in self.data:
                    a = (int(self.data.split('A')[1].split(")")[0]))
                if "B" in self.data:
                    b = (int(self.data.split('B')[1].split(")")[0]))
                if "C" in self.data:
                    c = (int(self.data.split('C')[1].split(")")[0]))
                #print(a,b,c)
                return  [a,b,c]
                self.ser.flush()
            except Exception:
                print("no data")
                self.ser.flush()

    def close(self):
        self.ser.close()

#create serial connection
ard=Arduino()

        
def run_program():
    while True:
        if ard.connState:
            #data = ard.loadData()
            data = ard.getSonar()    
            print(data)


        else:
            print ("Arduino not found")
            break

def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if input("\nReally quit? (y/n)> ").lower().startswith('y'):
            ard.close()
            sys.exit(1)

    except KeyboardInterrupt:
        print("Ok ok, quitting")
        ard.close()
        sys.exit(1)

    # restore the exit gracefully handler here    
    signal.signal(signal.SIGINT, exit_gracefully)


    
if __name__ == '__main__':
    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    run_program()   