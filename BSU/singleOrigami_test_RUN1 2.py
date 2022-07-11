import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import h5py
import os
import shutil
from sklearn import cluster, datasets, mixture
from sklearn.neighbors import kneighbors_graph
from itertools import cycle, islice
from sklearn.preprocessing import StandardScaler, scale
from scipy.ndimage import gaussian_filter, distance_transform_edt, label
from skimage.filters import threshold_local
from skimage.color import rgb2gray
from skimage import measure
from skimage.feature import peak_local_max
from skimage.morphology import watershed
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandasql as ps

#picasso hdf5 format (with averaging): ['frame', 'x', 'y', 'photons', 'sx', 'sy', 'bg', 'lpx', 'lpy', 'group']
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


#set group number
groupNumber = 0

#set filepath

#filtered by photons averaged dataset
filePath = r"Y:\George_D_DATA\2019-09-13\fromIAPETUS\run1\20190913_All-Matrices_syn2_pure_Triangles_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_12mM_PCD_TROLOX_1mM_10_38_52_substack_fixed_locs_render_DRIFT_3_filter_picked_avg.hdf5"

#open picasso hdf5 file as DF
locs = pd.read_hdf(filePath, '/locs')
#check header
headers = locs.dtypes.index
print(headers)
print(locs.shape)
print(locs.head(n=10))
print(locs.tail(n=10))


#scatter plot
#locs.plot.scatter(x='x',y='y', s=1, c='photons')
#locs.plot.scatter(x='x',y='y', s=0.1, c='lpx', colormap='hot')

#guassian blur
x = locs['x']
y = locs['y']
nBins = 750
H, xedges, yedges = np.histogram2d(x,y,bins=nBins )
H_guass = gaussian_filter(H, sigma=5)

H_guassMask = H_guass < 3
H_guass[H_guassMask] = [0] 


fig2, ax0 = plt.subplots()
ax0.imshow(np.rot90(H_guass))
X, Y = np.meshgrid(xedges, yedges)
ax0.pcolormesh(X, Y, H_guass)


#group by 'group' - get mean values
groupedLocs = locs.groupby('group',as_index=False).mean().drop(['frame', 'x', 'y', 'sx', 'sy', 'bg', 'lpx', 'lpy'],axis=1)
#groupedLocs.rename(index=str,columns={'x':'meanX', 'y':'meanY', 'photons':'meanPHOTONS', 'sx':'meanSX', 'sy':'meanSY', 'bg':'meanBG', 'lpx':'meanLPX', 'lpy':'meanLPY'},inplace=True)
groupedLocs.rename(index=str,columns={'photons':'meanPHOTONS'},inplace=True)

#merge locs and groupedLocs based on group
locs = locs.merge(groupedLocs, on='group', how='outer')

#add normalized photon count (photons normalized by group mean photons)
locs['photons_normalized'] = np.divide(locs['photons'],locs['meanPHOTONS'])


#filter for one origami
#locs = locs[locs['group']==groupNumber]

x = locs['x']
y = locs['y']
photons=locs['photons']
lpx = locs['lpx']
lpy = locs['lpy']

centeroids = np.array([
           [255.71958259, 255.69333761],
           [255.72814302, 255.78319555],
           [255.74048875, 255.87767681],
           [255.74142617, 255.97923731],
           [255.74639736, 256.07217399],
           [255.76108733, 256.17018534],
           [255.77066288, 256.26601427],
           [255.78355315, 256.35948195],
           [255.82071001, 255.67866898],
           [255.82985827, 255.77520452],
           [255.85250244, 256.06201605],
           [255.85269209, 255.96629434],
           [255.86685775, 256.16015103],
           [255.87253386, 256.258609  ],
           [255.92236922, 255.66905634],
           [255.93646258, 255.76212678],
           [255.94493996, 255.85808181],
           [255.95435298, 255.95611669],
           [255.95689406, 256.0528124 ],
           [255.9799807 , 256.24502927],
           [255.99165543, 256.34208804],
           [256.02767293, 255.66071132],
           [256.04019665, 255.75443278],
           [256.05205556, 255.84773132],
           [256.05658976, 255.94818059],
           [256.0635278 , 256.04308315],
           [256.07675012, 256.14066511],
           [256.08075565, 256.23937208],
           [256.13399681, 255.64938082],
           [256.14642698, 255.74094276],
           [256.15685431, 255.83730987],
           [256.15953915, 255.9367729 ],
           [256.1711187 , 256.03239615],
           [256.18111837, 256.12773012],
           [256.18716473, 256.22469699],
           [256.19840957, 256.32108102],
           [256.25535955, 255.73497127],
           [256.26844735, 255.82486324],
           [256.2675156 , 255.9266499 ],
           [256.28150681, 256.01937165],
           [256.28702614, 256.11310706],
           [256.29600087, 256.2123688 ],
           [256.31085381, 256.31026453],
           [256.231     , 255.648     ],
           [255.898     , 256.36      ],
           [256.09      , 256.342     ],
           [255.977     , 256.151     ],
           [255.842     , 255.877     ]]
)



#plt.figure(4)
fig4, ax2 = plt.subplots()
ax2.scatter(x,y, s=0.1, color='black')

##filter locs by centeroid positions
searchArea = 0.035 * 0.035
filteredLocs= pd.DataFrame()

#
#### UNCOMMENT ON FIRST RUN  ########
for i in range(len(centeroids)):
    query = "SELECT * FROM locs WHERE (((locs.x - {})*(locs.x - {})) + ((locs.y - {})*(locs.y - {}))) <= ({})".format(centeroids[i][0], centeroids[i][0], centeroids[i][1], centeroids[i][1], searchArea)
    filtered = ps.sqldf(query,locals())
    print(len(filtered))
    filtered['bindingSite'] = i
    filteredLocs = filteredLocs.append(filtered)
    print(i)

##export filteredDF
#filteredLocs.to_csv(savePath)


#### COMMENT OUT ON FIRST RUN #######
##load filteredDF
#filteredLocs = pd.read_csv(savePath)


##########################################################################################################

#filteredLocs.plot.scatter(x='x',y='y', s=0.1, color='black')

ax2.scatter(x=filteredLocs.x, y=filteredLocs.y, s=0.1, color='blue')
ax2.scatter(centeroids[:,0],centeroids[:,1], color='red')

centeroidGroups=range(len(centeroids))

for i,txt in enumerate(centeroidGroups):
    ax2.annotate(txt, (centeroids[i][0]+0.02,centeroids[i][1]))


#get number of binding sites per object
def bindingSitePlot(df, groupNumber = 0, numberOfBindingSites = len(centeroids)):
    group = df.loc[df.group == groupNumber]
    count,division = np.histogram(group['bindingSite'], bins=numberOfBindingSites)
    return count

#binding sites
numberOfBindingSites = len(filteredLocs['bindingSite'].unique())    
bindingSiteDF = pd.DataFrame(columns=list(range(numberOfBindingSites))).astype(int)   
for i in range(len(filteredLocs['group'].unique())):
    bindingSiteDF.loc[i] = bindingSitePlot(filteredLocs, groupNumber = i)
    

#incrementally alter background to try to improve false posiitive rate
#for i in [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 100, 150]:
for i in [10]:    
    #backgroundMean = backgroundMean + 25
    backgroundMean = i
        
    bindingSiteStatDF = pd.DataFrame()
    
    bindingSiteStatDF['zeros'] = (bindingSiteDF < backgroundMean).astype(int).sum(axis=1)
    bindingSiteStatDF['numberOfBindingSites'] = (numberOfBindingSites - bindingSiteStatDF['zeros'])
    
    
    stats = bindingSiteDF.describe()
    ind = np.arange(numberOfBindingSites)
    siteMean = stats.loc['mean'].values
    siteStd = stats.loc['std'].values
    
    
    siteMap = bindingSiteDF > backgroundMean
    siteMap_stats = siteMap.describe()
    siteFrequency = siteMap_stats.loc['freq'].values
    
    numberOfGroups = len(filteredLocs['group'].unique())
    
    sitePercent = siteFrequency / numberOfGroups
    
    
    centeroidGroups=range(len(centeroids))
        
    
    decodeDF = siteMap.astype(int)
    decodeRenameDF = decodeDF.rename(columns={      0:43,
                                                    1:36,
                                                    2:37,
                                                    3:38,
                                                    4:39,
                                                    5:40,
                                                    6:41,
                                                    7:42,
                                                    8:28,
                                                    9:29,
                                                    10:30,
                                                    11:31,
                                                    12:32,
                                                    13:33,
                                                    14:34,
                                                    15:35,
                                                    16:21,
                                                    17:22,
                                                    18:23,
                                                    19:24,
                                                    20:25,
                                                    21:26,
                                                    22:27,
                                                    23:45,
                                                    24:14,
                                                    25:15,
                                                    26:16,
                                                    27:17,
                                                    28:18,
                                                    29:46,
                                                    30:19,
                                                    31:20,
                                                    32:8,
                                                    33:9,
                                                    34:47,
                                                    35:11,
                                                    36:10,
                                                    37:12,
                                                    38:13,
                                                    39:44,
                                                    40:0,
                                                    41:1,
                                                    42:2,
                                                    43:3,
                                                    44:4,
                                                    45:5,
                                                    46:6,
                                                    47:7
                                                                          
                                                 })
    
    
    
    decodeReorderDF = decodeRenameDF.reindex(sorted(decodeRenameDF.columns), axis=1)
    
    savePath2 = filePath.split('.')[0] + '_incrementaBackground-TEST_{}.csv'.format(i)    
    decodeReorderDF.to_csv(savePath2, header=False, index=False)
    print(i)


