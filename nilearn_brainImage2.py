# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 16:20:12 2020

@author: g_dic
"""

from nilearn import plotting
from nilearn import image
import nilearn
from nilearn import surface
import numpy as np


filename = r"C:\Users\g_dic\OneDrive\Desktop\brain\test4d.nii.gz"

rsn = image.load_img(filename)
print(rsn.shape)

first_rsn = image.index_img(rsn, 0)
print(first_rsn.shape)

#plotting.plot_stat_map(first_rsn)

#get mesh
fsaverage = nilearn.datasets.fetch_surf_fsaverage()
#make texture
texture = surface.vol_to_surf(rsn, fsaverage.pial_right)

#smoothing
smoothed_img = image.smooth_img(rsn, fwhm=10)  

plotting.plot_glass_brain(smoothed_img)   

from nilearn.image.image import mean_img
mean_haxby = mean_img(rsn)

from nilearn.plotting import plot_epi, show
plot_epi(mean_haxby )


from nilearn.masking import compute_epi_mask
mask_img = compute_epi_mask(mean_haxby )

# Visualize it as an ROI
from nilearn.plotting import plot_roi
plot_roi(mean_haxby, rsn)




from skimage import measure
from skimage.draw import ellipsoid

# Generate a level set about zero of two identical ellipsoids in 3D
ellip_base = ellipsoid(6, 10, 16, levelset=True)
ellip_double = np.concatenate((ellip_base[:-1, ...],
                               ellip_base[2:, ...]), axis=0)

# Use marching cubes to obtain the surface mesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


data = first_rsn.dataobj

#data[data < 20] = 0

verts, faces, normals, values = measure.marching_cubes_lewiner(data, level=5,step_size=5)

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Fancy indexing: `verts[faces]` to generate a collection of triangles
mesh = Poly3DCollection(verts[faces])
mesh.set_edgecolor('k')
ax.add_collection3d(mesh)

ax.set_xlabel("x-axis: a = 6 per ellipsoid")
ax.set_ylabel("y-axis: b = 10")
ax.set_zlabel("z-axis: c = 16")

ax.set_xlim(0, 24)  # a = 6 (times two for 2nd ellipsoid)
ax.set_ylim(0, 20)  # b = 10
ax.set_zlim(0, 32)  # c = 16

plt.tight_layout()
plt.show()





