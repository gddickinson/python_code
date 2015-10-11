# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 11:25:43 2015

@author: George
"""

from __future__ import (absolute_import, division,print_function, unicode_literals)
import numpy as np
from pyunicorn.timeseries import RecurrenceNetwork

x = np.sin(np.linspace(0, 10 * np.pi, 1000))
net = RecurrenceNetwork(x, recurrence_rate=0.05)
print (net.transitivity())