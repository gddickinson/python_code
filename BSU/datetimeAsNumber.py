# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 16:36:09 2020

@author: GEORGEDICKINSON
"""

from datetime import date

date_string = '2015-01-30'
now = date(*map(int, date_string.split('-')))

print(now)