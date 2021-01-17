# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 09:42:45 2018

@author: George
"""

import pandas as pd
from matplotlib import pyplot as plt
from collections import Counter


fileName = r'C:\Users\George\Desktop\SoundScience\LCR_Survey_2018\classes.csv'
df1 = pd.read_csv(fileName)

dom1 = df1['Dom_1'].tolist()

tally = Counter(dom1)

print(tally)
      