# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 11:53:26 2019

@author: George
"""

from qtpy import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
import flika
flika_version = flika.__version__
from flika import global_vars as g
from flika.window import Window
from flika.utils.io import tifffile
from flika.process.file_ import get_permutation_tuple
from flika.utils.misc import open_file_gui
import numpy as np


A_list = [np.zeros([10,10,10])]
displayWindow = Window(A_list[0],'Volume')

displayWindow.imageview.ImageView.sigTimeChanged.connect(print('ok'))