# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 10:28:42 2020

@author: g_dic
"""

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
#print('numpy: '+np.version.full_version)
import matplotlib.animation as animation
import matplotlib
#print('matplotlib: '+matplotlib.__version__)
#%matplotlib inline

# animation params
Nfrm = 10
fps = 10

# shape functions
def generateSphere():
    '''
    Generates Z data for the points in the X, Y meshgrid and parameter phi.
    '''
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    X= np.cos(u)*np.sin(v)
    Y = np.sin(u)*np.sin(v)
    Z = np.cos(v)
    return X,Y,Z


# def sphere(u, v):
#     x = sin(u) * cos(v)
#     y = cos(u)
#     z = -sin(u) * sin(v)
#     return x, y, z

def generateKlein():
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = 3 * np.cos(u) * (1 + np.sin(u)) + (2 * (1 - np.cos(u) / 2)) * np.cos(u) * np.cos(v)
    z = -8 * np.sin(u) - 2 * (1 - np.cos(u) / 2) * np.sin(u) * np.cos(v)

        #x = 3 * np.cos(u) * (1 + np.sin(u)) + (2 * (1 - cos(np.u) / 2)) * cos(np.v + np.pi)
        #z = -8 * np.sin(u)
    y = -2 * (1 - np.cos(u) / 2) * np.sin(v)
    return x, y, z

    

def generateMobius():
    theta = np.linspace(0, 2 * np.pi, 30)
    w = np.linspace(-0.25, 0.25, 8)
    w, theta = np.meshgrid(w, theta)
    phi = 0.5 * theta
    # radius in x-y plane
    r = 1 + w * np.cos(phi)
    
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = w * np.sin(phi)
    return x,y,z


def generatePlane(Zaxis=0):
    x=np.linspace(-3,3,128) # x goes from -3 to 3, with 256 steps
    y=np.linspace(-3,3,128) # y goes from -3 to 3, with 256 steps
    X,Y=np.meshgrid(x,y)
    Z = np.zeros_like(X) + Zaxis
    return X,Y,Z



def generateCube(center=[0,0,0], size=(1.0,1.0,1.0)):
    """
       Create a data array for cuboid plotting.
    
    
       ============= ================================================
       Argument      Description
       ============= ================================================
       center        center of the cuboid, triple
       size          size of the cuboid, triple, (x_length,y_width,z_height)
       :type size: tuple, numpy.array, list
       :param size: size of the cuboid, triple, (x_length,y_width,z_height)
       :type center: tuple, numpy.array, list
       :param center: center of the cuboid, triple, (x,y,z)
    
    
      """
        
    # suppose axis direction: x: to left; y: to inside; z: to upper
    # get the (left, outside, bottom) point
    o = [a - b / 2 for a, b in zip(center, size)]
    # get the length, width, and height
    l, w, h = size
    x = [[o[0], o[0] + l, o[0] + l, o[0], o[0]],  # x coordinate of points in bottom surface
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],  # x coordinate of points in upper surface
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],  # x coordinate of points in outside surface
         [o[0], o[0] + l, o[0] + l, o[0], o[0]]]  # x coordinate of points in inside surface
    y = [[o[1], o[1], o[1] + w, o[1] + w, o[1]],  # y coordinate of points in bottom surface
         [o[1], o[1], o[1] + w, o[1] + w, o[1]],  # y coordinate of points in upper surface
         [o[1], o[1], o[1], o[1], o[1]],          # y coordinate of points in outside surface
         [o[1] + w, o[1] + w, o[1] + w, o[1] + w, o[1] + w]]    # y coordinate of points in inside surface
    z = [[o[2], o[2], o[2], o[2], o[2]],                        # z coordinate of points in bottom surface
         [o[2] + h, o[2] + h, o[2] + h, o[2] + h, o[2] + h],    # z coordinate of points in upper surface
         [o[2], o[2], o[2] + h, o[2] + h, o[2]],                # z coordinate of points in outside surface
         [o[2], o[2], o[2] + h, o[2] + h, o[2]]]                # z coordinate of points in inside surface
    return np.array(x), np.array(y), np.array(z)  


def generateTorus():
    n = 50
    theta = np.linspace(0, 2.*np.pi, n)
    phi = np.linspace(0, 2.*np.pi, n)
    theta, phi = np.meshgrid(theta, phi)
    c, a = 2, 1
    x = (c + a*np.cos(theta)) * np.cos(phi)
    y = (c + a*np.cos(theta)) * np.sin(phi)
    z = a * np.sin(theta)
    return x,y,z

def generatePringle():
    n_radii = 8
    n_angles = 36
    
    # Make radii and angles spaces (radius r=0 omitted to eliminate duplication).
    radii = np.linspace(0.125, 1.0, n_radii)
    angles = np.linspace(0, 2*np.pi, n_angles, endpoint=False)[..., np.newaxis]
    
    radii, angles = np.meshgrid(radii, angles)
    
    # Convert polar (radii, angles) coords to cartesian (x, y) coords.
    # points in the (x, y) plane.
    x = (radii*np.cos(angles))
    y = (radii*np.sin(angles))
    
    # Compute z to make the pringle surface.
    z = np.sin(-x*y)
    return x,y,z

def test():
    def fun(x, y):
        return x**2 + y
    x = y = np.arange(-3.0, 3.0, 0.05)
    X, Y = np.meshgrid(x, y)
    zs = np.array(fun(np.ravel(X), np.ravel(Y)))
    Z = zs.reshape(X.shape)
    return X,Y,Z

def generatePyramid(center=[0,0,0], size=(1.0,1.0,1.0)):
    o = [a - b / 2 for a, b in zip(center, size)]
    # get the length, width, and height
    l, w, h = size
    x = [[0, 0, 0, 0, 0],  # x coordinate of points in bottom surface
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],  # x coordinate of points in upper surface
         [0, 0, 0, 0, 0],  # x coordinate of points in outside surface
         [0, 0, 0, 0, 0]]  # x coordinate of points in inside surface
    y = [[0,0,0,0,0],  # y coordinate of points in bottom surface
         [o[1], o[1], o[1] + w, o[1] + w, o[1]],  # y coordinate of points in upper surface
         [0, 0, 0, 0, 0],          # y coordinate of points in outside surface
         [0, 0, 0, 0, 0]]    # y coordinate of points in inside surface
    z = [[o[2], o[2], o[2], o[2], o[2]],                        # z coordinate of points in bottom surface
         [o[2] + h, o[2] + h, o[2] + h, o[2] + h, o[2] + h],    # z coordinate of points in upper surface
         [o[2], o[2], o[2], o[2], o[2]],                # z coordinate of points in outside surface
         [o[2], o[2], o[2], o[2] , o[2]]]                # z coordinate of points in inside surface
    return np.array(x), np.array(y), np.array(z)     
    


# transformation functions
def scaleXYZ(X,Y,Z, phi, X_factor=1, Y_factor=1, Z_factor=1):
    return X*(X_factor*phi),Y*(Y_factor*phi),Z*(Z_factor*phi)

def rotateX(X, Y, Z, deg):
    """ Rotates this point around the X axis the given number of degrees. Return the x, y, z coordinates of the result"""
    rad = deg * np.pi / 180
    cosa = np.cos(rad)
    sina = np.sin(rad)
    Y = Y * cosa - Z * sina
    Z = Y * sina + Z * cosa
    return X, Y, Z   

def transpose(X,Y,Z, D, X_factor=0, Y_factor=0, Z_factor=0):
    return X+(X_factor*D),Y+(Y_factor*D),Z+(Z_factor*D)


def wave(X, Y, Z, phi):
    '''
    Generates Z data for the points in the X, Y meshgrid and parameter phi.
    '''
    R = 1 - np.sqrt(X**2 + Y**2)
    return X,Y, np.sinc(2 * np.pi * X + phi) * R

def wave2(X,Y,Z,phi,func='sin'):
    R = np.sqrt(X**2 + Y**2)
    if func == 'sin':
        Z = np.sin(R) * phi
    if func == 'cos':
        Z = np.cos(R) * phi        
    return X,Y, Z
    

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')


# Set the z axis limits so they aren't recalculated each frame.
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(-3, 3)

# Begin plotting.
wframe = None

# define update routine
def update(idx):
    #init shape
    #X,Y,Z = generateSphere()
    #X,Y,Z = generatePlane()
    #X,Y,Z = generateCube()    
    #X,Y,Z = generateMobius()
    #X,Y,Z = generateTorus()
    #X,Y,Z = generateKlein()
    #X,Y,Z = generatePringle()
    X,Y,Z = generatePyramid()
    
    phi=phis[idx]
    print(phi)
    global wframe
    # If a line collection is already remove it before drawing.
    if wframe:
        ax.collections.remove(wframe)

    # Plot the new wireframe and pause briefly before continuing.
    #X,Y,Z = scaleXYZ(X,Y,Z,phi)
    #X,Y,Z = rotateX(X,Y,Z,phi*180)  
    #X,Y,Z = wave(X,Y,Z,phi)
    #X,Y,Z = wave2(X,Y,Z,phi)
    X,Y,Z = transpose(X,Y,Z, phi, 1,0)
    
    
    wframe = ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1, color='k', linewidth=0.5)
    #wframe = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color='k', linewidth=0.5)

phis = np.linspace(0, 3, 5)
reversePhis = np.linspace(3, 0, 5)
phis = np.concatenate((phis, reversePhis), axis=0) 
ani = animation.FuncAnimation(fig, update, Nfrm, interval=1000/fps)