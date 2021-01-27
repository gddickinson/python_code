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
groupNumber = 3

#set filepath

#filtered by photons averaged dataset
filePath = r"Y:\George_D_DATA\2019-09-13\fromIAPETUS\run2\20190913_All-Matrices_syn2_pure_Triangles_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_12mM_PCD_TROLOX_1mM_13_42_03_fixed_locs_render_DRIFT_3_filter_picked_manual_avg.hdf5"

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
locs = locs[locs['group']==groupNumber]

x = locs['x']
y = locs['y']
photons=locs['photons']
lpx = locs['lpx']
lpy = locs['lpy']

centeroids = np.array([
        
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

centeroids = centeroids.tolist()

sortedList=[]

def getKey(item):
    return item[1]    

for elem in sorted(remap.items(),key=getKey) :
    #print(elem[0] , " ::" , elem[1] )
    #print(elem[0])
    sortedList.append(centeroids[elem[0]])


centeroids = np.array(sortedList)


##filter locs by centeroid positions
searchArea = 0.035 * 0.035
filteredLocs= pd.DataFrame()

#
#### UNCOMMENT ON FIRST RUN  ########
for i in range(len(centeroids)):
    query = "SELECT * FROM locs WHERE (((locs.x - {})*(locs.x - {})) + ((locs.y - {})*(locs.y - {}))) <= ({})".format(centeroids[i][0], centeroids[i][0], centeroids[i][1], centeroids[i][1], searchArea)
    filtered = ps.sqldf(query,locals())
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
#plt.figure(4)
fig4, ax2 = plt.subplots()
ax2.scatter(x,y, s=5, color='grey') 
plt.xlim(256.6,255.4)
plt.ylim(255.4,256.6)
ax2.scatter(x=filteredLocs.x, y=filteredLocs.y, s=6, color='blue')
ax2.scatter(centeroids[:,0],centeroids[:,1], color='red', s=50)

centeroidGroups=range(len(centeroids))

for i,txt in enumerate(centeroidGroups):
    ax2.annotate(txt, (centeroids[i][0]+0.02,centeroids[i][1]), size=12)


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
    

##incrementally alter background to try to improve false posiitive rate
##for i in [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 100, 150]:
#for i in [10]:    
#    #backgroundMean = backgroundMean + 25
#    backgroundMean = i
#        
#    bindingSiteStatDF = pd.DataFrame()
#    
#    bindingSiteStatDF['zeros'] = (bindingSiteDF < backgroundMean).astype(int).sum(axis=1)
#    bindingSiteStatDF['numberOfBindingSites'] = (numberOfBindingSites - bindingSiteStatDF['zeros'])
#    
#    
#    stats = bindingSiteDF.describe()
#    ind = np.arange(numberOfBindingSites)
#    siteMean = stats.loc['mean'].values
#    siteStd = stats.loc['std'].values
#    
#    
#    siteMap = bindingSiteDF > backgroundMean
#    siteMap_stats = siteMap.describe()
#    siteFrequency = siteMap_stats.loc['freq'].values
#    
#    numberOfGroups = len(filteredLocs['group'].unique())
#    
#    sitePercent = siteFrequency / numberOfGroups
#    
#    
#    centeroidGroups=range(len(centeroids))
#        
#    
#    decodeDF = siteMap.astype(int)
#
#    
#    savePath2 = filePath.split('.')[0] + '_incrementaBackground-TEST_{}.csv'.format(i)    
#    decodeDF.to_csv(savePath2, header=False, index=False)
#    print(i)
#

