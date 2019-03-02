# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 13:45:36 2014

@author: Kyle
I found another library which performs a nearly identical function after I wrote this.  It is located in https://github.com/ZhuangLab/storm-analysis/blob/master/sa_library/gaussfit.py
"""
from __future__ import absolute_import, division, print_function # Enable the new behaviour
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt4 import QtGui, QtCore
from leastsqbound import leastsqbound

def cosd(degrees):
    return np.cos(np.radians(degrees))
def sind(degrees):
    return np.sin(np.radians(degrees))

#### SYMETRICAL GAUSSIAN  
def fitGaussian(I=None, p0=None, bounds=None, display=False):
    '''
    Takes an nxm matrix and returns an nxm matrix which is the gaussian fit
    of the first.  p0 is a list of parameters [xorigin, yorigin, sigma,amplitude]
    0-19 should be [-.2889 -.3265 -.3679 -.4263 -.5016 -.6006 ... -.0228 .01913]
    '''

    x=np.arange(I.shape[0])
    y=np.arange(I.shape[1])
    if display:
        data=Puff3d(I,'Original Data')
    X=[x,y]
    p0=[round(p,3) for p in p0] 
    p, cov_x, infodic, mesg, ier = leastsqbound(err, p0,args=(I,X),bounds = bounds,ftol=.0000001,full_output=True)
    #xorigin,yorigin,sigmax,sigmay,angle,amplitude=p
    I_fit=gaussian(x[:,None], y[None,:],*p)
    if not display:
        return p, I_fit, I_fit
    else:
        fitted_data=Puff3d(I_fit,'Fitted')
        return data, fitted_data, p

        
def gaussian(x,y,xorigin,yorigin,sigma,amplitude):
    '''xorigin,yorigin,sigmax,sigmay,angle'''
    return amplitude*(np.exp(-(x-xorigin)**2/(2.*sigma**2))*np.exp(-(y-yorigin)**2/(2.*sigma**2)))
    
    
def gaussian_1var(p, x): #INPUT_MAT,xorigin,yorigin,sigma):
    '''xorigin,yorigin,sigmax,sigmay,angle'''
    xorigin,yorigin,sigma,amplitude= p
    x0=x[0]
    x1=x[1]
    x0=x0[:,None]
    x1=x1[None,:]
    return amplitude*(np.exp(-(x0-xorigin)**2/(2.*sigma**2))*np.exp(-(x1-yorigin)**2/(2.*sigma**2)))
    
    
def err(p, y, x):
    ''' 
    p is a tuple contatining the initial parameters.  p=(xorigin,yorigin,sigma, amplitude)
    y is the data we are fitting to (the dependent variable)
    x is the independent variable
    '''
    remander=y - gaussian_1var(p, x)
    remander=remander**2
    return remander.ravel()
    

    
    
    
    
    

