# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 17:06:52 2015

@author: george
"""

def genFib():
    fibn_1 = 1 #fib(n-1)
    fibn_2 = 0 #fib(n-2)
    while True:
        # fib(n) = fib(n-1) + fib(n-2)
        next = fibn_1 + fibn_2
        yield next
        fibn_2 = fibn_1
        fibn_1 = next

x= 0

for n in genFib():
    if x< 50:
        print n
        x +=1
    else:
        break