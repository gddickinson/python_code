# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 12:48:16 2016

@author: George
"""

import numpy as np
import matplotlib.pyplot as plt

def main():
    data = generate_data()
    xbar, ybar, cov = intertial_axis(data)

    fig, ax = plt.subplots()
    ax.imshow(data, cmap="hot")
    plot_bars(xbar, ybar, cov, ax)
    plt.show()

#==============================================================================
# def generate_data():
#     data = np.zeros((200, 200), dtype=np.float)
#     cov = np.array([[200, 100], [100, 200]])
#     ij = np.random.multivariate_normal((100,100), cov, int(1e5))
#     for i,j in ij:
#         data[int(i), int(j)] += 1
#     return data 
#==============================================================================

def generate_data():
    filename = 'J:\\WORK_IN_PROGRESS\\CellLights_AND_FIXATION\\cellLights_beads_100nm\\File_002_croppedBead3_50Frames_XY.txt'
    X = np.loadtxt(filename,skiprows=1,usecols=(0,))
    Y = np.loadtxt(filename,skiprows=1,usecols=(1,))
    maxXScale = 200/(max(X)-min(X))
    maxYScale = 200/(max(Y)-min(Y))        
    canvas = np.zeros((200,200))        
    x = X*maxXScale
    y = Y*maxYScale

    for i in X:
        canvas[(x[i])-1,(y[i])-1] = 1        
    #print(canvas)
    return canvas


def raw_moment(data, iord, jord):
    nrows, ncols = data.shape
    y, x = np.mgrid[:nrows, :ncols]
    data = data * x**iord * y**jord
    return data.sum()

def intertial_axis(data):
    """Calculate the x-mean, y-mean, and cov matrix of an image."""
    data_sum = data.sum()
    m10 = raw_moment(data, 1, 0)
    m01 = raw_moment(data, 0, 1)
    x_bar = m10 / data_sum
    y_bar = m01 / data_sum
    u11 = (raw_moment(data, 1, 1) - x_bar * m01) / data_sum
    u20 = (raw_moment(data, 2, 0) - x_bar * m10) / data_sum
    u02 = (raw_moment(data, 0, 2) - y_bar * m01) / data_sum
    cov = np.array([[u20, u11], [u11, u02]])
    return x_bar, y_bar, cov

def plot_bars(x_bar, y_bar, cov, ax):
    """Plot bars with a length of 2 stddev along the principal axes."""
    def make_lines(eigvals, eigvecs, mean, i):
        """Make lines a length of 2 stddev."""
        std = np.sqrt(eigvals[i])
        vec = 2 * std * eigvecs[:,i] / np.hypot(*eigvecs[:,i])
        x, y = np.vstack((mean-vec, mean, mean+vec)).T
        return x, y
    mean = np.array([x_bar, y_bar])
    eigvals, eigvecs = np.linalg.eigh(cov)
    ax.plot(*make_lines(eigvals, eigvecs, mean, 0), marker='o', color='white')
    ax.plot(*make_lines(eigvals, eigvecs, mean, -1), marker='o', color='red')
    ax.axis('image')

if __name__ == '__main__':
    main()