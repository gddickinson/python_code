from __future__ import division
import numpy as np
#from scipy import stats
import matplotlib
from matplotlib import pyplot as plt

filename = "/home/george/Desktop/pwctools/singlePuff1.txt"
y = np.loadtxt(filename,skiprows=0,usecols=(0,))

soft=1          # 1 for guassian
beta=200.0      # beta of kernel
width=5         # width of kernel
display=1       # 1 to report iteration values
stoptol=0.001   # tolerance for convergence
maxiter=50      # maximum number of iterations

y=np.array(y[:])
N=np.size(y,0)
w=np.zeros((N,N))
j=arange(0,N)

#construct initial bilateral kernel
for i in arange(0,N):
    w[i,arange(0,N)]=(abs(i-j) <= width)

#initial guess from input signal
xold=np.copy(y)

#new matrix for storing distances
d=np.zeros((N,N))

fig1 = plt.plot(y)

if (display):
    if (soft):
        print('Soft kernel')
    else:
        print('Hard kernel')
    print('Kernel parameters beta= %d, W= %d' % (beta,width))
    print('Iter# Change')

#start iteration
iterate=1
gap=np.inf

while (iterate < maxiter):

    if (display):
        print('%d %f'% (iterate,gap))

    # calculate paiwise distances for all points
    for i in arange(0,N):
        d[:,i] = (0.5 * (xold - xold[i]) ** 2)
    
    #create kernel
    if (soft):
        W=np.multiply(np.exp(-beta*d),w)

    else:
        W=np.multiply((d <= beta ** 2),w)
    
    #apply kernel to get weighted mean shift   
    xnew1=np.sum(np.multiply(np.transpose(W),xold), axis=1)
    xnew2=np.sum(W, axis=1)
    xnew=np.divide(xnew1,xnew2)
   
    plt.plot(xnew)   
    
    #check for convergence
    gap=np.sum(np.square(xold-xnew))

    if (gap < stoptol):
        if (display):
            print('Converged in %d iterations' % iterate)
        break

    xold=np.copy(xnew)
    iterate+=1

if (display):
    if (iterate == maxiter):
        print('Maximum iterations exceeded')

x=np.copy(xnew)
