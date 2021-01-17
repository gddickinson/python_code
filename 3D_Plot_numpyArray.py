# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 11:34:39 2019

@author: George
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import affine_transform
from os.path import expanduser, isfile, join
from numpy import moveaxis
from skimage.transform import rescale
import copy

def get_transformation_matrix(theta=45):
    """
    theta is the angle of the light sheet
    Look at the pdf in this folder.
    """

    theta = theta/360 * 2 * np.pi # in radians
    hx = np.cos(theta)
    sy = np.sin(theta)
 
    S = np.array([[1, hx, 0],
                  [0, sy, 0],
                  [0, 0, 1]])

    return S


def get_transformation_coordinates(I, theta):
    negative_new_max = False
    S = get_transformation_matrix(theta)
    S_inv = np.linalg.inv(S)
    mx, my = I.shape

    four_corners = np.matmul(S, np.array([[0, 0, mx, mx],
                                          [0, my, 0, my],
                                          [1, 1, 1, 1]]))[:-1,:]
    range_x = np.round(np.array([np.min(four_corners[0]), np.max(four_corners[0])])).astype(np.int)
    range_y = np.round(np.array([np.min(four_corners[1]), np.max(four_corners[1])])).astype(np.int)
    all_new_coords = np.meshgrid(np.arange(range_x[0], range_x[1]), np.arange(range_y[0], range_y[1]))
    new_coords = [all_new_coords[0].flatten(), all_new_coords[1].flatten()]
    new_homog_coords = np.stack([new_coords[0], new_coords[1], np.ones(len(new_coords[0]))])
    old_coords = np.matmul(S_inv, new_homog_coords)
    old_coords = old_coords[:-1, :]
    old_coords = old_coords
    old_coords[0, old_coords[0, :] >= mx-1] = -1
    old_coords[1, old_coords[1, :] >= my-1] = -1
    old_coords[0, old_coords[0, :] < 1] = -1
    old_coords[1, old_coords[1, :] < 1] = -1
    new_coords[0] -= np.min(new_coords[0])
    keep_coords = np.logical_not(np.logical_or(old_coords[0] == -1, old_coords[1] == -1))
    new_coords = [new_coords[0][keep_coords], new_coords[1][keep_coords]]
    old_coords = [old_coords[0][keep_coords], old_coords[1][keep_coords]]
    return old_coords, new_coords



c=[0, 2, 1, 3]
d=[0, 2, 3, 1]
e=[0, 3, 1, 2] #
f=[0, 3, 2, 1] #


m=[2, 0, 1, 3]
n=[2, 0, 3, 1]
q=[2, 3, 0, 1]
r=[2, 3, 1, 0]

s=[3, 0, 1, 2] #
t=[3, 0, 2, 1] #
w=[3, 2, 0, 1]
x=[3, 2, 1, 0]

test = x

def perform_shear_transform(A, shift_factor, interpolate, datatype, theta):
    #A = moveaxis(A, [1, 3, 2, 0], [0, 1, 2, 3])
    #A = moveaxis(A, [2, 3, 0, 1], [0, 1, 2, 3])
    A = moveaxis(A, test, [0, 1, 2, 3])   
    m1, m2, m3, m4 = A.shape
    if interpolate:
        A_rescaled = np.zeros((m1*int(shift_factor), m2, m3, m4))
        for v in np.arange(m4):
            print('Upsampling Volume #{}/{}'.format(v+1, m4))
            A_rescaled[:, :, :, v] = rescale(A[:, :, :, v], (shift_factor, 1.), mode='constant', preserve_range=True)
    else:
        A_rescaled = np.repeat(A, shift_factor, axis=0)
    mx, my, mz, mt = A_rescaled.shape
    I = A_rescaled[:, :, 0, 0]
    old_coords, new_coords = get_transformation_coordinates(I, theta)
    old_coords = np.round(old_coords).astype(np.int)
    new_mx, new_my = np.max(new_coords[0]) + 1, np.max(new_coords[1]) + 1
    # I_transformed = np.zeros((new_mx, new_my))
    # I_transformed[new_coords[0], new_coords[1]] = I[old_coords[0], old_coords[1]]
    # Window(I_transformed)
    D = np.zeros((new_mx, new_my, mz, mt))
    D[new_coords[0], new_coords[1], :, :] = A_rescaled[old_coords[0], old_coords[1], :, :]
    #E = moveaxis(D, [0, 1, 2, 3], [1, 3, 2, 0])
    #E = moveaxis(D, [0, 1, 2, 3], [2, 3, 0, 1])
    E = moveaxis(D, [0, 1, 2, 3], test)   
    E = np.flip(E, 1)
    #Window(E[0, :, :, :])
    #E = E.astype(datatype)
    return E

def getCorners(vol):
    z,x,y = vol.nonzero()
    z_min = np.min(z)
    z_max = np.max(z)
    x_min = np.min(x)
    x_max = np.max(x)
    y_min = np.min(y)
    y_max = np.max(y)
    newArray = np.zeros(vol.shape)

    newArray[z_min,x_min,y_min] = 1    
    newArray[z_min,x_max,y_min] = 1    
    newArray[z_min,x_min,y_max] = 1    
    newArray[z_min,x_max,y_max] = 1    
    newArray[z_max,x_min,y_min] = 1    
    newArray[z_max,x_max,y_min] = 1    
    newArray[z_max,x_min,y_max] = 1    
    newArray[z_max,x_max,y_max] = 1     
    return newArray

shift_factor = 1
interpolate = False
theta = 45

#np.random.seed(29)
#d = np.random.randint(0,2,size=(3,3,3))

# =============================================================================
# d = np.ones((3,3,10))
# d = np.pad(d,2,'constant', constant_values=(0))
# 
# z,x,y = d.nonzero()
# 
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(x, y, -z, zdir='z', c= 'red')
# # set axes range
# ax.set_xlim(0, 15)
# ax.set_ylim(0, 15)
# ax.set_zlim(0, -15)
# #ax.set_aspect('equal')
# 
# #plt.savefig("demo.png")
# 
# # =============================================================================
# # # animate - rotate the axes and update
# # for angle in range(0, 360):
# #     ax.view_init(30, angle)
# #     plt.draw()
# #     plt.pause(.001)
# # =============================================================================
# 
# #d_t = np.reshape(d,(7,1,7,14))
# #d_t= perform_shear_transform(d, shift_factor, interpolate, d.dtype, theta)
# #d_t = d_t[:,0,:,:]
# 
# d_t = affine_transform(d, get_transformation_matrix())
# 
# 
# z1,x1,y1 = (d_t > 0.1).nonzero()
# 
# fig1 = plt.figure()
# ax1 = fig1.add_subplot(111, projection='3d')
# ax1.scatter(x1, y1, -z1, zdir='z', c= 'red')
# # set axes range
# ax1.set_xlim(0, 15)
# ax1.set_ylim(0, 15)
# ax1.set_zlim(0, -15)
# =============================================================================

filePath = join(expanduser("~/Desktop"),'array_4D_data_roundCell.npy')
data = np.float64(np.load(filePath))

#get 1 volume
vol = data[:,0,:,:]

##pad data
#vol = np.pad(vol, 5, 'constant', constant_values = 0)

vol_downSample = copy.deepcopy(vol)

#downsample data
prob = 0.001
mask = np.random.choice([False, True], vol_downSample.shape, p=[prob, 1-prob])
vol_downSample[mask] = 0

##z2,x2,y2 = vol.nonzero()
z2,x2,y2 =(vol_downSample > 1000).nonzero()

fig2 = plt.figure()
ax2 = fig2.add_subplot(111, projection='3d')
ax2.scatter(x2, y2, -z2, zdir='z', c= 'red', s=1)

vol_corners = getCorners(vol)
z2_c,x2_c,y2_c =vol_corners.nonzero()

ax2.scatter(x2_c, y2_c, -z2_c, zdir='z', c= 'green', s=5)

ax2.set_xlim(0, 500)
ax2.set_ylim(0, 500)
ax2.set_zlim(0, -500)

ax2.view_init(0,180)
plt.draw()


############################################################


data_t = perform_shear_transform(data, shift_factor, interpolate, data.dtype, theta)
vol_t = data_t[:,0,:,:]


vol_t_downSample = copy.deepcopy(vol_t)

#downsample data
mask = np.random.choice([False, True], vol_t_downSample.shape, p=[prob, 1-prob])
vol_t_downSample[mask] = 0


#z3,x3,y3 = vol_t_downSample.nonzero()
z3,x3,y3 =(vol_t_downSample > 1000).nonzero()

#vol_t = affine_transform(vol_downSample, np.linalg.inv(get_transformation_matrix()))
#z3,x3,y3 =(vol_t > 1000).nonzero()

fig3 = plt.figure()
ax3 = fig3.add_subplot(111, projection='3d')
ax3.scatter(x3, y3, -z3, zdir='z', c= 'red', s=1)

vol_t_corners = getCorners(vol_t)
z3_c,x3_c,y3_c =vol_t_corners.nonzero()

ax3.scatter(x3_c, y3_c, -z3_c, zdir='z', c= 'green', s=5)


ax3.set_xlim(0, 500)
ax3.set_ylim(0, 500)
ax3.set_zlim(0, -500)

ax3.view_init(0,180)
plt.draw()

