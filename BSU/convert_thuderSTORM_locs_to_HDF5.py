# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 16:32:04 2019

@author: GEORGEDICKINSON
"""

import pandas as pd

#look at picasso hdf5 file
#filePath = r"C:/Users/georgedickinson/Documents/BSU_work/thunderStorm analysis/2019-03-04/picasso_processing/002_dNAM-Exp01-wReg_100pM-100uL-30min_Mid-3nM-18mM-Mg 2019 March 04 11_10_26-raw_locs.hdf5"
#locs = pd.read_hdf(filePath, '/locs')
#headers = locs.dtypes.index

picasso_headers = ['frame', 'x', 'y', 'photons', 'sx', 'sy', 'bg', 'lpx', 'lpy', 'ellipticity', 'net_gradient']

#import thuderStorm loc file
filePath = r"C:\Users\georgedickinson\Documents\BSU_work\thunderStorm analysis\2019-03-20\20193020_Chris_Triangles_300msExp_Mid-9nt-3nM_MgCl2_18mM_002 2019 March 20 12_26_45-raw-locs-DRIFT_CORRECTED.csv"

locs = pd.read_csv(filePath)

#thunderStorm_headers = locs.dtypes.index
thunderStorm_headers = ['id', 'frame', 'x [nm]', 'y [nm]', 'sigma [nm]', 'intensity [photon]', 'offset [photon]', 'bkgstd [photon]', 'uncertainty_xy [nm]']

locs.rename(index=str, columns={'x [nm]':'x', 'y [nm]':'y', 'sigma [nm]':'ellipticity', 'intensity [photon]':'photons',
                                'offset [photon]':'TODO', 'bkgstd [photon]':'bg', 'uncertainty_xy [nm]':'TODO'})




