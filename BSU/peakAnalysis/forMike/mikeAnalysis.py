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
import pandasql as ps
from itertools import groupby
from operator import itemgetter

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
filePath = r"C:\Users\g_dic\Documents\bsu\forMike\20190913_All-Matrices_syn2_pure_Triangles_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_12mM_PCD_TROLOX_1mM_10_38_52_substack_fixed_locs_render_DRIFT_3_filter_Matrix_05.hdf5"

#savePath = filePath.split('.')[0] + '_filtered.hdf5'

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
#locs.plot.scatter(x='x',y='y',s=1)

#get centroid positions used for grid
centroids = np.array([
        
           [255.65026699, 256.2699313 ],
           [255.65522196, 255.9542909 ],
           [255.65336587, 256.16112367],
           [255.66110178, 255.74295807],
           [255.74678208, 256.05605212],
           [255.74547016, 256.16300094],
           [255.75104081, 256.2720415 ],
           [255.75228561, 255.84415798],
           [255.75351785, 255.95273798],
           [255.75479689, 255.73969906],
           [255.84866381, 256.05934078],
           [255.84685329, 256.16708376],
           [255.85103522, 256.27369471],
           [255.85160587, 255.74273925],
           [255.85740968, 255.85026562],
           [255.94392418, 256.27673285],
           [255.94391768, 256.05966314],
           [255.94611554, 256.17014591],
           [255.95094813, 255.95014021],
           [255.95158306, 255.85177168],
           [255.95400055, 255.74037337],
           [256.03677785, 256.2720229 ],
           [256.03969133, 256.06114094],
           [256.04283514, 256.16603679],
           [256.04661846, 255.85896198],
           [256.04490558, 255.96022842],
           [256.05086907, 255.7461775 ],
           [256.14012688, 256.1753788 ],
           [256.14023585, 256.0697952 ],
           [256.140229  , 256.2836567 ],
           [256.14513271, 255.75414015],
           [256.14299781, 255.96175843],
           [256.2314431 , 256.17345542],
           [256.23032086, 256.28052939],
           [256.23801515, 256.06644361],
           [256.23637598, 255.96237802],
           [256.2397271 , 255.75018973],
           [256.23966435, 255.85825364],
           [256.32819487, 256.17121161],
           [256.33097833, 255.75340018],
           [256.32980017, 256.06243964],
           [256.32933863, 255.96060716],
           [256.33441629, 255.85686116],
           [256.144     , 255.865     ],
           [255.851     , 255.954     ],
           [255.652     , 256.057     ],
           [255.659     , 255.846     ],
           [256.327     , 256.281     ]]

)



remap={  33:2,
         29:3,
         21:4,
         15:5,
         12:6,
         6:7,
         0:8,
         38:9,
         32:10,
         27:11,
         23:12,
         17:13,
         11:14,
         5:15,
         2:16,
         40:17,
         34:18,
         28:19,
         22:20,
         16:21,
         10:22,
         4:23,
         41:25,
         35:26,
         31:27,
         25:28,
         18:29,
         44:30,
         8:31,
         1:32,
         42:33,
         37:34,
         43:35,
         24:36,
         19:37,
         14:38,
         7:39,
         39:41,
         36:42,
         30:43,
         26:44,
         20:45,
         13:46,
         9:47,
         3:48,
         47:1,
         45:24,
         46:40                                                                         
         }



#plot centroids
#plt.scatter(centroids[:,0],centroids[:,1],c='red')

#add site position to each localization
#filter locs by centroid positions using SQL
searchArea = 0.04 * 0.04
filteredLocs= pd.DataFrame()
centroidList = centroids.tolist()

for i in range(len(centroidList)):
    query = "SELECT * FROM locs WHERE (((locs.x - {})*(locs.x - {})) + ((locs.y - {})*(locs.y - {}))) <= ({})".format(centroidList[i][0], centroidList[i][0], centroidList[i][1], centroidList[i][1], searchArea)
    filtered = ps.sqldf(query,locals())
    filtered['bindingSite'] = i
    filteredLocs = filteredLocs.append(filtered)
    print(i)

#plot
filteredLocs.plot.scatter(x='x',y='y',s=1)

#plot all binding sites against time
#all origami
#filteredLocs.plot.scatter(x='frame',y='photons',c='bindingSite',colormap='tab20b',s=0.5)
#filter one origami
origamiDF = filteredLocs.loc[filteredLocs['group'] == 0]
#plot
#origamiDF.plot.scatter(x='frame',y='photons')

#plot trace for an origamis site position
siteDF = origamiDF.loc[origamiDF['bindingSite'] == 0]
siteDF.plot.scatter(x='frame',y='photons')


# group consecutive points into seperate peaks  
peakList =[]
peakOnlyData = []
amplitudeList = []
maxAmplitudeList = []
ONtimeList = []
OFFtimeList = []

peakNumber = 0 

indexes = siteDF['frame']


for k,g in groupby(enumerate(indexes),lambda x:x[0]-x[1]):
    group = (map(itemgetter(1),g))
    group = list(map(int,group))
    print(group)



    
    peakNumber += 1


# get OFF times
OFFtimeList.append(peakList[0][0])
for i in range(1,len(peakList)):
    OFFtimeList.append(peakList[i][0]-peakList[i-1][-1])
    #indexed
    OFFtimeList_forMike.append([traceIndex,i, peakList[i][0]-peakList[i-1][-1]])




