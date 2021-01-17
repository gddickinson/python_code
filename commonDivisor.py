# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:03:34 2020

@author: g_dic
"""


def commonDivisor(m,n, max_t=1000):
    '''Use Eulcids algorithm to determine the greatest common divisor for two positive integers m and n'''
    #ensure input correct
    if isinstance(m, int) == False or isinstance(n,int) == False:
        return 'integers only', None
    if m < 0 or n < 0:
        return 'positive integers only', None
    #initiate t
    t = 0
    while t < max_t:
        #set m to Remainder of m/n
        m = m%n
        #if m== 0 return n
        if m == 0:
            return n, t
        #divide n by m let n be the remainder
        n = n%m
        #if n == 0 return m
        if n == 0:
            return m, t
        #increment t by 1 per loop
        t += 1
    #if max_t exceeded return fail message
    return 'timed out at {}'.format(t), t 


ans, t = commonDivisor(6099,2166)  
print (ans, t)  