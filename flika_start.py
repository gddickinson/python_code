# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 14:25:22 2019

@author: George
"""
from distutils.version import StrictVersion
import flika
from flika import global_vars as g
from flika.window import Window
from flika.process.file_ import save_file_gui, open_file_gui, open_file
from flika import *

try:
    flika_version = flika.__version__
except AttributeError:
    flika_version = '0.0.0'
if StrictVersion(flika_version) < StrictVersion('0.1.0'):
    import global_vars as g
    from process.BaseProcess import BaseProcess, WindowSelector, SliderLabel, CheckBox
    from window import Window
    from roi import ROI_rectangle, makeROI
    from process.file_ import open_file_gui, open_file
    g.alert('The detect_puffs no longer works with older versions of Filka. Delete your current version of Flika and reinstall the newer version before using this plugin. ')
else:
    from flika import global_vars as g
    from flika.window import Window
    from flika.roi import ROI_rectangle, makeROI
    from flika.process.file_ import open_file
    from flika.utils.misc import open_file_gui
    from flika.process import *
    from flika.utils.misc import save_file_gui
    if StrictVersion(flika_version) < StrictVersion('0.2.23'):
        from flika.process.BaseProcess import BaseProcess, WindowSelector, SliderLabel, CheckBox
    else:
        from flika.utils.BaseProcess import BaseProcess, WindowSelector, SliderLabel, CheckBox

from flika.process.file_ import save_file_gui, open_file_gui, open_file

start_flika()

data_window = open_file(r"C:\Users\g_dic\OneDrive\Desktop\testing\particles.tif")

butter_image = butterworth_filter(filter_order, low, high, framerate, keepSourceWindow=True)            
