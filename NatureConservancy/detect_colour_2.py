# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 15:09:38 2017

@author: George
"""

## import the necessary packages
#import skimage
import numpy as np
#
#define path
path = r"C:\Users\George\Desktop\images\\"
file = r"Flower.jpg"
filename = path + file

image = path + filename


import matplotlib.pyplot as plt

from skimage.color import rgb2hed
from skimage.color import rgb2hed
from skimage import io
from matplotlib.colors import LinearSegmentedColormap


# Create an artificial color close to the orginal one
cmap_blue = LinearSegmentedColormap.from_list('mycmap', ['blue', 'white'])
cmap_red = LinearSegmentedColormap.from_list('mycmap', ['red',
                                             'white'])
cmap_green = LinearSegmentedColormap.from_list('mycmap', ['green',
                                               'white'])

#ihc_rgb = data.immunohistochemistry()
ihc_rgb = io.imread(filename)


ihc_hed = rgb2hed(ihc_rgb)

fig, axes = plt.subplots(2, 2, figsize=(7, 6), sharex=True, sharey=True,
                         subplot_kw={'adjustable': 'box-forced'})
ax = axes.ravel()

ax[0].imshow(ihc_rgb)
ax[0].set_title("Original image")

ax[1].imshow(ihc_hed[:, :, 0], cmap=cmap_red)
ax[1].set_title("red")

ax[2].imshow(ihc_hed[:, :, 1], cmap=cmap_blue)
ax[2].set_title("blue")

ax[3].imshow(ihc_hed[:, :, 2], cmap=cmap_green)
ax[3].set_title("green")

for a in ax.ravel():
    a.axis('off')

fig.tight_layout()

from skimage.exposure import rescale_intensity

# Rescale hematoxylin and DAB signals and give them a fluorescence look
h = rescale_intensity(ihc_hed[:, :, 0], out_range=(0, 1))
d = rescale_intensity(ihc_hed[:, :, 2], out_range=(0, 1))
zdh = np.dstack((np.zeros_like(h), d, h))

fig = plt.figure()
axis = plt.subplot(1, 1, 1, sharex=ax[0], sharey=ax[0], adjustable='box-forced')
axis.imshow(zdh)
axis.set_title("Stain separated image (rescaled)")
axis.axis('off')
plt.show()