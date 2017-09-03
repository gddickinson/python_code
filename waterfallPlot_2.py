import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot
from matplotlib.collections import PolyCollection



def drawPropagation(beta2, C, z):
    """ beta2 in ps / km
        C is chirp
        z is an array of z positions """
    T = np.linspace(-10, 10, 100)
    sx = T.size
    sy = z.size

    T = np.tile(T, (sy, 1))
    z = np.tile(z, (sx, 1)).T

    U = 1 / np.sqrt(1 - 1j*beta2*z * (1 + 1j * C)) * np.exp(- 0.5 * (1 + 1j * C) * T * T / (1 - 1j*beta2*z*(1 + 1j*C)))

    fig = pyplot.figure()
    ax = fig.add_subplot(1,1,1, projection='3d')
    U = np.abs(U)

    verts = []
    for i in range(T.shape[0]):
        verts.append(list(zip(T[i, :], U[i, :])))

    poly = PolyCollection(verts, facecolors=(1,1,1,1), edgecolors=(0,0,1,1))
    ax.add_collection3d(poly, zs=z[:, 0], zdir='y')
    ax.set_xlim3d(np.min(T), np.max(T))
    ax.set_ylim3d(np.min(z), np.max(z))
    ax.set_zlim3d(np.min(U), np.max(U))

drawPropagation(1.0, 1.0, np.linspace(-2, 2, 10))
pyplot.show()