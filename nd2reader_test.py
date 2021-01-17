# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 14:07:53 2020

@author: g_dic
"""


from nd2reader import ND2Reader
import matplotlib.pyplot as plt

#filename = r"C:\Users\g_dic\OneDrive\Desktop\from_IanP\2020-02-05_RedLaser70_DRIFT_TEST_1.nd2"
filename = r"C:\Users\g_dic\OneDrive\Desktop\from_IanP\2020-02-3_TestRecording.nd2"


with ND2Reader(filename) as images:
    # width and height of the image
    print('%d x %d px' % (images.metadata['width'], images.metadata['height']))


with ND2Reader(filename) as images:
    # width and height of the image
    print(images.metadata)


with ND2Reader(filename) as images:
  plt.imshow(images[0])
  
