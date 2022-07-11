# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 15:12:52 2015

@author: george
"""

def genPrimes():
    primes = []   # primes generated so far
    last = 1      # last number tried
    while True:
        last += 1
        for p in primes:
            if last % p == 0:
                break
        else:
            primes.append(last)
            yield last
    
x= 0

for n in genPrimes():
    if x< 50:
        print n
        x +=1
    else:
        break