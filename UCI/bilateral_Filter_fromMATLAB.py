# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 15:16:12 2015

@author: George
"""
from __future__ import (absolute_import, division,print_function, unicode_literals)
import numpy as np
from scipy import stats
import matplotlib
from matplotlib import pyplot as plt
import math

def pwc_bilateral(y=None, soft=None, beta=None, width=None, display=None, stoptol=None, maxiter=None):
    # Performs PWC denoising of the input signal using hard or soft kernel
    # bilateral filtering.
    #
    # Usage:
    # x = pwc_bilateral(y, soft, beta, width, display, stoptol, maxiter)
    #
    # Input arguments:
    # - y          Original signal to denoise of length N.
    # - soft       Set this to 1 to use the soft Gaussian kernel, else uses
    #              the hard kernel.
    # - beta       Kernel parameter. If soft Gaussian kernel, then this is the
    #              precision parameter. If hard kernel, this is the kernel
    #              support.
    # - width      Spatial kernel width W.
    # - display    (Optional) Set to 0 to turn off progress display, 1 to turn
    #              on. If not specifed, defaults to progress display on.
    # - stoptol    (Optional) Precision of estimate as determined by square
    #              magnitude of the change in the solution. If not specified,
    #              defaults to 1e-3.
    # - maxiter    (Optional) Maximum number of iterations. If not specified,
    #              defaults to 50.
    #
    # Output arguments:
    # - x          Denoised output signal.
    #
    # (c) Max Little, 2011. If you use this code for your research, please cite:
    # M.A. Little, Nick S. Jones (2011)
    # "Generalized Methods and Solvers for Noise Removal from Piecewise
    # Constant Signals: Part I - Background Theory"
    # Proceedings of the Royal Society A (in press)

##Checks function input to ensure correct number of arguments ###
#    error(nargchk(4, 7, nargin))
#    if (nargin < 5):
#        display = 1
#        end
#    if (nargin < 6):
#        stoptol = 1e-3
#        end
#    if (nargin < 7):
#        maxiter = 50
#        end

    y = np.array(y[:])
    N = np.size(y, 1)

    # Construct bilateral sequence kernel
    w = np.zeros(N, N)
    j = np.array[1:N]
    for i in mslice[1:N]:
        w(i, mslice[:]).lvalue = (abs(i - j) <= width)
        end

    xold = y                # Initial guess using input signal
    d = zeros(N, N)

    if (display):
        if (soft):
            fprintf(mstring('Soft kernel\\n'))
        else:
            fprintf(mstring('Hard kernel\\n'))
            end
            fprintf(mstring('Kernel parameters beta=%7.2e, W=%7.2e\\n'), beta, width)
            fprintf(mstring('Iter# Change\\n'))
            end

    # Iterate
    iter = 1
    gap = Inf
    while (iter < maxiter):

        if (display):
            fprintf(mstring('%5d %7.2e\\n'), iter, gap)
            end

    # Compute pairwise distances between all samples
    for i in mslice[1:N]:
        d(mslice[:], i).lvalue = 0.5 * (xold - xold(i)) **elpow** 2
        end

    # Compute kernels
    if (soft):
        W = exp(-beta * d) *elmul* w                                        # Gaussian (soft) kernel
    else:
        W = (d <= beta ** 2) *elmul* w                                        # Characteristic (hard) kernel
        end

    # Do kernel weighted mean shift update step
    xnew = sum(W.cT * xold, 2) /eldiv/ sum(W, 2)

    gap = sum((xold - xnew) **elpow** 2)

    # Check for convergence
    if (gap < stoptol):
        if (display):
            fprintf(mstring('Converged in %d iterations\\n'), iter)
            end
            break
            end

    xold = xnew
    iter = iter + 1
    end

    if (display):
        if (iter == maxiter):
            fprintf(mstring('Maximum iterations exceeded\\n'))
            end
            end

    x = xnew