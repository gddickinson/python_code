# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 15:58:44 2020

@author: g_dic
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection


# Retrieve destrieux parcellation in fsaverage5 space from nilearn
from nilearn import datasets
from nilearn import plotting

destrieux_atlas = datasets.fetch_atlas_surf_destrieux()

# The parcellation is already loaded into memory
parcellation = destrieux_atlas['map_left']

# Retrieve fsaverage5 surface dataset for the plotting background. It contains
# the surface template as pial and inflated version and a sulcal depth maps
# which is used for shading
fsaverage = datasets.fetch_surf_fsaverage()

# The fsaverage dataset contains file names pointing to the file locations
print('Fsaverage5 pial surface of left hemisphere is at: %s' %
      fsaverage['pial_left'])
print('Fsaverage5 inflated surface of left hemisphere is at: %s' %
      fsaverage['infl_left'])
print('Fsaverage5 sulcal depth map of left hemisphere is at: %s' %
      fsaverage['sulc_left'])

import numpy as np
from nilearn import surface

atlas = destrieux_atlas
coordinates = []
labels = destrieux_atlas['labels']
for hemi in ['left', 'right']:
    vert = destrieux_atlas['map_%s' % hemi]
    rr, _ = surface.load_surf_mesh(fsaverage['pial_%s' % hemi])
    for k, label in enumerate(labels):
        if "Unknown" not in str(label):  # Omit the Unknown label.
            # Compute mean location of vertices in label of index k
            coordinates.append(np.mean(rr[vert == k], axis=0))

coordinates = np.array(coordinates)  # 3D coordinates of parcels

# We now make a synthetic connectivity matrix that connects labels
# between left and right hemispheres.
n_parcels = len(coordinates)
corr = np.zeros((n_parcels, n_parcels))
n_parcels_hemi = n_parcels // 2
corr[np.arange(n_parcels_hemi), np.arange(n_parcels_hemi) + n_parcels_hemi] = 1
corr = corr + corr.T

# plotting.plot_connectome(corr, coordinates,
#                          edge_threshold="90%",
#                          title='fsaverage Destrieux atlas')
# plotting.show()


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#faces = Poly3DCollection(edges, linewidths=1, edgecolors='k')
#faces.set_facecolor((0,0,1,0.1))

#ax.add_collection3d(faces)

# Plot the points themselves to force the scaling of the axes
ax.scatter(coordinates[:,0], coordinates[:,1], coordinates[:,2], s=5)

#ax.set_aspect('equal')

fig.show()
