# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 17:21:40 2015

@author: george
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import time


def genFib():
    fibn_1 = 1 #fib(n-1)
    fibn_2 = 0 #fib(n-2)
    while True:
        # fib(n) = fib(n-1) + fib(n-2)
        next = fibn_1 + fibn_2
        yield next
        fibn_2 = fibn_1
        fibn_1 = next

def fib_plot(steps):  
    count= 0
    #previous = 0
    x,y = [],[]
    for n in genFib():
        if count< steps+5:
            print n
            count +=1
            if count%2 == 1:
                x.append(n)
                x.append(n)
            else:
                y.append(n)
                y.append(n)
        else:
            break
    
    for index in range(len(x)):
        if index % 4 ==0:
            x[index-1]=x[index-1]*-1
            x[index-2]=x[index-2]*-1
    
    for index in range(len(y)):
        if index % 4 ==0:
            y[index-1]=y[index-1]*-1
            y[index-2]=y[index-2]*-1
    
    x = [0]+x
    x = x[:steps]
    y = y[:steps]
    return x,y

def init():
    line.set_data([], [])
    return line,
    
    
def animate(i):    
    x,y = fib_plot(i)
    line.set_data(x, y)
    return line,

fig = plt.figure()
ax1 = plt.axes(xlim=(-1000, 1000), ylim=(-1000, 1000))

line, = ax1.plot([], [], lw=2)

ani = animation.FuncAnimation(fig, animate, init_func=init, interval=200)
plt.show()