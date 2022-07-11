# -*- coding: utf-8 -*-
"""
Created on Thu May 30 11:01:24 2019

@author: GEORGEDICKINSON
"""

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import h5py
import os
import shutil

#picasso hdf5 format (without averaging): ['frame', 'x', 'y', 'photons', 'sx', 'sy', 'bg', 'lpx', 'lpy']
#Column Name       |	Description                                                                                                                      |	C Data Type
#frame	            |The frame in which the localization occurred, starting with zero for the first frame.	                                                |unsigned long
#x                |The subpixel x coordinate in camera pixels	                                                                                          |float
#y	              |The subpixel y coordinate in camera pixels	                                                                                          |float
#photons	       |The total number of detected photons from this event, not including background or camera offset	                                      |float
#sx	             |The Point Spread Function width in camera pixels                                                                                       |	float
#sy	             |The Point Spread Function height in camera pixels                                                                                      |	float
#bg	             |The number of background photons per pixel, not including the camera offset                                                            |	float
#lpx	         |The localization precision in x direction, in camera pixels, as estimated by the Cramer-Rao Lower Bound of the Maximum Likelihood fit.  |	float
#lpy	         |The localization precision in y direction, in camera pixels, as estimated by the Cramer-Rao Lower Bound of the Maximum Likelihood fit.  |	float


#set filepath
filePath = r"Y:\George_D_DATA\2019-08-30\20190830_Matrix5_syn2_pure_Triangles_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_12mM_PCD_TROLOX_1mM_10_44_32_fixed_locs_picked.hdf5"
savePath = filePath.split('.')[0] + '_filtered.hdf5'

#info data in yaml
yamlPath = filePath.split('.')[0] + '.yaml'
yamlSavePath = filePath.split('.')[0] + '_filtered.yaml'

#open picasso hdf5 file as DF
locs = pd.read_hdf(filePath, '/locs')
#check header
headers = locs.dtypes.index
print(headers)
print(locs.head(n=1))

#scatter plot
locs.plot.scatter(x='x',y='y')

#plot histogram photons
locs.hist(column='photons',bins=10000)

#group by 'group' - get mean values
groupedLocs = locs.groupby('group',as_index=False).mean()

#group by 'group' - get counts
#groupedLocs_count = locs.groupby('group',as_index=False).count()
#groupedLocs_count.hist(column='frame', bins=200)

#plot mean photons for each group
fig, ax = plt.subplots()
scatter = ax.scatter(groupedLocs['x'], groupedLocs['y'], c=groupedLocs['photons'], cmap='plasma')
legend = ax.legend(*scatter.legend_elements(),
                loc="lower left", title="photons")
ax.axis([0,512,0,512])
ax.add_artist(legend)  


#filter by groups with mean photon counts > 8000
filteredLocs = groupedLocs.loc[(groupedLocs.photons > 8000)]
groupsToKeep = list(filteredLocs['group'])

#plot mean photons for each group
fig2, ax2 = plt.subplots()
scatter2 = ax2.scatter(filteredLocs['x'], filteredLocs['y'], c=filteredLocs['photons'], cmap='plasma')
legend = ax2.legend(*scatter2.legend_elements(),
                loc="lower left", title="photons")
ax2.axis([0,512,0,512])
ax2.add_artist(legend)  

#create new df with selected groups
newLocs = locs[locs['group'].isin(groupsToKeep)]

#plot histogram photons
newLocs.hist(column='photons',bins=10000)

#plot histogram lpx & lpy
newLocs.hist(column='lpx',bins=1000)
newLocs.hist(column='lpy',bins=1000)

# =============================================================================
# #get min,max values for x and y
# x_min = locs['x'].min()
# y_min = locs['y'].min()
# x_max = locs['x'].max()
# y_max = locs['y'].max()
# 
# #round x,y pixel values for grouping by pixel
# locs['x_round'] = locs.x.round(0)
# locs['y_round'] = locs.y.round(0)
# 
# #get min,max values for x and y
# x_round_min = locs['x_round'].min()
# y_round_min = locs['y_round'].min()
# x_round_max = locs['x_round'].max()
# y_round_max = locs['y_round'].max()
# 
# # get locations of structures by dropping duplicated x y values - keep the highest intensity
# locs_DupsDropped = locs.sort_values('photons', ascending=True).drop_duplicates(subset =["x_round","y_round"], keep = "last", inplace = False).sort_index()
# 
# #filter locs DF to one pixel location based on rounded value in dupsDropped
# x = locs_DupsDropped['x_round'].iloc[10]
# y = locs_DupsDropped['y_round'].iloc[10]
# 
# locs_OnePixel = locs.loc[(locs.x_round==x) & (locs.y_round==y)]
# 
# locs_OnePixel.hist(column='photons',bins=400)
# locs_OnePixel.plot.bar(x='frame', y='photons')
# 
# locs_OnePixel.plot.scatter(x='x',y='y', xlim=(x-1,x+1),ylim=(y-1,y+1))
# =============================================================================



def createPlot(df, groupNumber = 0, filterByPhotons = True, photonFilter = (5000,15000),filterByPrecision = True, precisionFilter = 0.025):
    #filter by group (for picked locs)
    if filterByPhotons == True:
        group = df.loc[(df.group == groupNumber) & (df.photons > photonFilter[0]) & (df.photons < photonFilter[1])]
    else:
        group = df.loc[df.group == groupNumber]

    if filterByPrecision == True:
        group = group.loc[(group.lpx < precisionFilter) & (group.lpx < precisionFilter)]

    
    #plot group histogram photons
    #group.hist(column='photons',bins=400)
    
    #plot group photons / frame
    #group.plot.bar(x='frame', y='photons')
    
    #plot group histogram lpx
    group.hist(column='lpx',bins=400)
    
    #plot group histogram lpy
    group.hist(column='lpy',bins=400)
    
    #scatter plot
    x = np.array(group['x'])
    y = np.array(group['y'])
    photons = np.array(group['photons'])
    
    meanX = np.mean(x)
    meanY = np.mean(y)
    
    
    fig, ax = plt.subplots()
    scatter = ax.scatter(x, y, c=photons, cmap='plasma')
    ax.axis([meanX-1,meanX+1,meanY-1,meanY+1])
    
    legend = ax.legend(*scatter.legend_elements(),
                    loc="lower left", title="photons")
    ax.add_artist(legend)    
    
    plt.show()
    return


createPlot(newLocs, groupNumber = 1, precisionFilter = 0.04)
createPlot(newLocs, groupNumber = 1, filterByPhotons = False, precisionFilter = 0.04)



#create filtered df for export
#finalLocs = newLocs.loc[(newLocs.photons > 5000) & (newLocs.photons < 15000) & (newLocs.lpx < 0.025) & (newLocs.lpy < 0.025)]

finalLocs = newLocs.loc[(newLocs.photons > 5000) & (newLocs.photons < 15000) & (newLocs.lpx < 0.04) & (newLocs.lpy < 0.04)]

#def save_locs(path, locs, info):
    #locs = _lib.ensure_sanity(locs, info)
#    with h5py.File(path, "w") as locs_file:
#        locs_file.create_dataset("locs", data=locs)
#    base, ext = os.path.splitext(path)
    #info_path = base + ".yaml"
    #save_info(info_path, info)

def saveHDF5(df, out_path):
    #from .io import save_locs   
    frames = df["frame"].astype(int)
    # make sure frames start at zero:
    x = df["x"]
    y = df["y"]
    photons = df["photons"].astype(int)    
    bg = df["bg"].astype(int)
    lpx = df["lpx"]
    lpy = df["lpy"]
    sx = df["sx"]
    sy= df["sy"]
    group = df["group"].astype(int)
    
    LOCS_DTYPE = [
        ("frame", "u4"),
        ("x", "f4"),
        ("y", "f4"),
        ("photons", "f4"),
        ("sx", "f4"),
        ("sy", "f4"),
        ("bg", "f4"),
        ("lpx", "f4"),
        ("lpy", "f4"),
        ("group", "i4"),
                    ]
    locs = np.rec.array((frames, x, y, photons, sx, sy, bg, lpx, lpy,group),dtype=LOCS_DTYPE,)

    locs.sort(kind="mergesort", order="frame")
    
    img_info = {}
    img_info["Generated by"] = "Picasso csv2hdf"
    img_info["Frames"] = int(np.max(frames)) + 1
    img_info["Height"] = int(np.ceil(np.max(y)))
    img_info["Width"] = int(np.ceil(np.max(x)))

    info = []
    info.append(img_info)

    #base, ext = os.path.splitext(path)
    #out_path = base + "_locs.hdf5"
    #save_locs(out_path, locs, info)
    
    with h5py.File(out_path, "w") as locs_file:
        locs_file.create_dataset("locs", data=locs)
    
    print("Saved to {}.".format(out_path))    
    return
       

def copy_rename(old_file_name, new_file_name):
    src_dir= os.curdir
    dst_dir= os.path.join(os.curdir , "subfolder")
    src_file = os.path.join(src_dir, old_file_name)
    shutil.copy(src_file,dst_dir)
    
    dst_file = os.path.join(dst_dir, old_file_name)
    new_dst_file_name = os.path.join(dst_dir, new_file_name)
    os.rename(dst_file, new_dst_file_name)   
    
    
#save hdf5 file    
saveHDF5(finalLocs,savePath)    
    
#save yadl info file    
copy_rename(yamlPath,yamlSavePath)    