# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 12:42:03 2018

@author: George
"""

from sklearn.datasets import load_iris
iris = load_iris()

from sklearn.cluster import DBSCAN
dbscan = DBSCAN(eps=0.5, metric='euclidean', min_samples=5)

dbscan.fit(iris.data)