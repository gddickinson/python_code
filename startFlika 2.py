# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 08:54:05 2020
Synapse3D - Clustering code
@author: George
"""
import os, sys, glob

import flika
from flika import global_vars as g
from flika.window import Window
from distutils.version import StrictVersion
import numpy as np

flika_version = flika.__version__
if StrictVersion(flika_version) < StrictVersion('0.2.23'):
    from flika.process.BaseProcess import BaseProcess, SliderLabel, CheckBox, ComboBox, BaseProcess_noPriorWindow, WindowSelector, FileSelector
else:
    from flika.utils.BaseProcess import BaseProcess, SliderLabel, CheckBox, ComboBox, BaseProcess_noPriorWindow, WindowSelector, FileSelector

from flika import *

from tifffile import imread

if __name__ == "__main__":
    start_flika()
    A = imread(r"C:\Users\g_dic\OneDrive\Desktop\trial_1_400step_20msecexp_po36slice_gcamp_hippo_MMStack_Pos0.ome.tif")
    data = Window(A,'data')