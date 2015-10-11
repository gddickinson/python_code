# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 19:58:21 2015

@author: george
"""
import math
import matplotlib
import numpy as np
from matplotlib import pyplot as plt
import random



def sqrt(n, one):
     """
     Return the square root of n as a fixed point number with the one
     passed in.  It uses a second order Newton-Raphson convergence.  This
     doubles the number of significant figures on each iteration.
     """
     # Use floating point arithmetic to make an initial guess
     floating_point_precision = 10**16
     n_float = float((n * floating_point_precision) // one) / floating_point_precision
     x = (int(floating_point_precision * math.sqrt(n_float)) * one) // floating_point_precision
     n_one = n * one
     while 1:
         x_old = x
         x = (x + n_one // x) // 2
         if x == x_old:
             break
     return x


def pi_chudnovsky(one=1000000):
    """
    Calculate pi using Chudnovsky's series

    This calculates it in fixed point, using the value for one passed in
    """
    k = 1
    a_k = one
    a_sum = one
    b_sum = 0
    C = 640320
    C3_OVER_24 = C**3 // 24
    while 1:
        a_k *= -(6*k-5)*(2*k-1)*(6*k-1)
        a_k //= k*k*k*C3_OVER_24
        a_sum += a_k
        b_sum += k * a_k
        k += 1
        if a_k == 0:
            break
    total = 13591409*a_sum + 545140134*b_sum
    pi = (426880*sqrt(10005*one, one)*one) // total
    return pi

def pi_chudnovsky_bs(digits):
    """
    Compute int(pi * 10**digits)

    This is done using Chudnovsky's series with binary splitting
    """
    C = 640320
    C3_OVER_24 = C**3 // 24
    def bs(a, b):
        """
        Computes the terms for binary splitting the Chudnovsky infinite series

        a(a) = +/- (13591409 + 545140134*a)
        p(a) = (6*a-5)*(2*a-1)*(6*a-1)
        b(a) = 1
        q(a) = a*a*a*C3_OVER_24

        returns P(a,b), Q(a,b) and T(a,b)
        """
        if b - a == 1:
            # Directly compute P(a,a+1), Q(a,a+1) and T(a,a+1)
            if a == 0:
                Pab = Qab = 1
            else:
                Pab = (6*a-5)*(2*a-1)*(6*a-1)
                Qab = a*a*a*C3_OVER_24
            Tab = Pab * (13591409 + 545140134*a) # a(a) * p(a)
            if a & 1:
                Tab = -Tab
        else:
            # Recursively compute P(a,b), Q(a,b) and T(a,b)
            # m is the midpoint of a and b
            m = (a + b) // 2
            # Recursively calculate P(a,m), Q(a,m) and T(a,m)
            Pam, Qam, Tam = bs(a, m)
            # Recursively calculate P(m,b), Q(m,b) and T(m,b)
            Pmb, Qmb, Tmb = bs(m, b)
            # Now combine
            Pab = Pam * Pmb
            Qab = Qam * Qmb
            Tab = Qmb * Tam + Pam * Tmb
        return Pab, Qab, Tab
    # how many terms to compute
    DIGITS_PER_TERM = math.log10(C3_OVER_24/6/2/6)
    N = int(digits/DIGITS_PER_TERM + 1)
    # Calclate P(0,N) and Q(0,N)
    P, Q, T = bs(0, N)
    one = 10**digits
    sqrtC = sqrt(10005*one, one)
    return (Q*426880*sqrtC) // T

def genPi_Digit_List(length):
    digit_list=[]
    pi_to_n= str(pi_chudnovsky_bs(length))
    for digit in pi_to_n:
        digit_list.append(int(digit))
    return digit_list


number_of_digits = 100000
pi_digits = genPi_Digit_List(number_of_digits)
x = range(number_of_digits+1)
randomDigits = [random.randint(1,19) for _ in range(100000)]
random_digits1=np.array(randomDigits[:50000])
random_digits2=np.array(randomDigits[1:50001])
#plt.plot(x,pi_digits)



#==============================================================================
#ratio
pi_digits1=np.array(pi_digits[:50000])
pi_digits2=np.array(pi_digits[1:50001])
 
ratio1to2=np.divide(pi_digits2,pi_digits1)
randomRatio1to2 =np.divide(random_digits1,random_digits2)
x = range(50000)
 
fig = plt.figure()
ax = fig.add_subplot(2,1,1)
scatter =  plt.plot(x,ratio1to2, 'b.')
ax.set_xscale('log')


bx = fig.add_subplot(2,1,2)
scatter2 = plt.plot(x,randomRatio1to2, 'b.')
#==============================================================================
bx.set_xscale('log')
#show()


np.savetxt('pidigits.txt', pi_digits1, delimiter=',',fmt='%1d') 
np.savetxt('random_digits1.txt', pi_digits1, delimiter=',',fmt='%1d') 

