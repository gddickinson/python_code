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


#set filepath

#filtered by photons averaged dataset
filePath = r"Y:\George_D_DATA\2019-09-13\fromIAPETUS\run2\20190913_All-Matrices_syn2_pure_Triangles_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_12mM_PCD_TROLOX_1mM_13_42_03_fixed_locs_render_DRIFT_3_filter_picked_manual_avg.hdf5"
backgroundCenteroids = np.array([[255.652,256.057],[255.659,255.846], [256.327,256.281]])


savePath = filePath.split('.')[0] + '_analysisResult.csv'


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
locs.plot.scatter(x='x',y='y', s=0.1, c='lpx', colormap='hot')
x = locs['x']
y = locs['y']
photons=locs['photons']
lpx = locs['lpx']
lpy = locs['lpy']


#group by 'group' - get mean values
groupedLocs = locs.groupby('group',as_index=False).mean().drop(['frame', 'x', 'y', 'sx', 'sy', 'bg', 'lpx', 'lpy'],axis=1)
#groupedLocs.rename(index=str,columns={'x':'meanX', 'y':'meanY', 'photons':'meanPHOTONS', 'sx':'meanSX', 'sy':'meanSY', 'bg':'meanBG', 'lpx':'meanLPX', 'lpy':'meanLPY'},inplace=True)
groupedLocs.rename(index=str,columns={'photons':'meanPHOTONS'},inplace=True)

#merge locs and groupedLocs based on group
locs = locs.merge(groupedLocs, on='group', how='outer')

#add normalized photon count (photons normalized by group mean photons)
locs['photons_normalized'] = np.divide(locs['photons'],locs['meanPHOTONS'])

#plt.figure(1)
#plt.scatter(x,y, s=1,c=photons)
#plt.scatter(x,y, s=1,c=lpx)

#guassian blur
nBins = 750
H, xedges, yedges = np.histogram2d(x,y,bins=nBins )
H_guass = gaussian_filter(H, sigma=5)

H_guassMask = H_guass < 3
H_guass[H_guassMask] = [0] 


fig2, ax0 = plt.subplots()
ax0.imshow(np.rot90(H_guass))
X, Y = np.meshgrid(xedges, yedges)
ax0.pcolormesh(X, Y, H_guass)


#threshold
#gray = rgb2gray(H_guass)
thresholded = threshold_local(H_guass, 3)            
binary_adaptive = H_guass > thresholded

#fig3, ax = plt.subplots()
#ax.pcolormesh(X, Y, binary_adaptive)

#blob detection ##REPLACED BY WATERSHED DETECTION##
#labels = measure.label(binary_adaptive)

#watershed
D = distance_transform_edt(binary_adaptive)

nBins = 750
H, xedges, yedges = np.histogram2d(x,y,bins=nBins )
D = gaussian_filter(D, sigma=6)

D_guassMask = D < 4
D[D_guassMask] = [0] 

localMax = peak_local_max(D, indices=False,min_distance=5)
# perform a connected component analysis on the local peaks,
# using 8-connectivity, then appy the Watershed algorithm
markers = label(localMax, structure=np.ones((3, 3)))[0]
labels = watershed(-D, markers, mask=binary_adaptive)
print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))


fig3, ax = plt.subplots()
ax.pcolormesh(X, Y, D)
#ax.pcolormesh(X, Y, labels)
#ax.pcolormesh(X, Y, mask)




#for scaling
minXValue = min(xedges)
maxXValue = max(xedges)
minYValue = min(yedges)
maxYValue = max(yedges)

xRange = maxXValue - minXValue
yRange = maxYValue - minYValue

centeroids = []
boxProps = []


for region in measure.regionprops(labels):
    # take regions with large enough areas
    if region.area >= 200 and region.area < 1800 and region.solidity > 0.8:
	
        # draw rectangle around segmented objects
        minr, minc, maxr, maxc = region.bbox
        
        #scale to match original data range
        minr = (np.divide(minr,nBins) * yRange) + minYValue
        minc = (np.divide(minc,nBins) * xRange) + minXValue
        maxr = (np.divide(maxr,nBins) * yRange) + minYValue
        maxc = (np.divide(maxc,nBins) * xRange) + minXValue
        
        boxProps.append([minr,minc,maxr,maxc])
        
        #get centeroid
        (cent_x,cent_y) = region.centroid 
        cent_y = (np.divide(cent_y,nBins) * yRange) + minYValue
        cent_x = (np.divide(cent_x,nBins) * xRange) + minXValue
        
        centeroids.append([cent_x,cent_y]) 

        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
												fill=False, edgecolor='red', linewidth=2)
        
        ax.add_patch(rect)

#manually add centeroids here, if needed
centeroids = centeroids + [[256.144,255.865],[255.851,255.954],[255.652,256.057],[255.659,255.846], [256.327,256.281]]

centeroids = np.array(centeroids)

#plt.figure(4)
fig4, ax2 = plt.subplots()
ax2.scatter(x,y, s=0.1, color='black')



##filter locs by centeroid positions
searchArea = 0.035 * 0.035
filteredLocs= pd.DataFrame()

#
#### UNCOMMENT ON FIRST RUN  ########
#for i in range(len(centeroids)):
#    query = "SELECT * FROM locs WHERE (((locs.x - {})*(locs.x - {})) + ((locs.y - {})*(locs.y - {}))) <= ({})".format(centeroids[i][0], centeroids[i][0], centeroids[i][1], centeroids[i][1], searchArea)
#    filtered = ps.sqldf(query,locals())
#    filtered['bindingSite'] = i
#    filteredLocs = filteredLocs.append(filtered)
#    print(i)
#
##export filteredDF
#filteredLocs.to_csv(savePath)




#### COMMENT OUT ON FIRST RUN #######
##load filteredDF
filteredLocs = pd.read_csv(savePath)


##########################################################################################################

#filteredLocs.plot.scatter(x='x',y='y', s=0.1, color='black')

ax2.scatter(x=filteredLocs.x, y=filteredLocs.y, s=0.1, color='blue')
ax2.scatter(centeroids[:,0],centeroids[:,1], color='red')


#get background from manually selected locations

backGroundLocs = pd.DataFrame()

for i in range(len(backgroundCenteroids)):
    query = "SELECT * FROM locs WHERE (((locs.x - {})*(locs.x - {})) + ((locs.y - {})*(locs.y - {}))) <= ({})".format(backgroundCenteroids[i][0], backgroundCenteroids[i][0], backgroundCenteroids[i][1], backgroundCenteroids[i][1], searchArea)
    filtered = ps.sqldf(query,locals())
    filtered['bindingSite'] = i
    backGroundLocs = backGroundLocs.append(filtered)
    print(i)

#backGroundLocs.plot.scatter(x='x',y='y', s=0.1, color='black')

ax2.scatter(x=backGroundLocs.x, y=backGroundLocs.y, s=0.1, color='green')
ax2.scatter(backgroundCenteroids[:,0],backgroundCenteroids[:,1], color='yellow')    

#plot all binding sites against time
filteredLocs.plot.scatter(x='frame',y='photons_normalized',c='bindingSite',colormap='tab20b',s=0.5)
filteredLocs.plot.scatter(x='frame',y='photons',c='bindingSite',colormap='tab20b',s=0.5)

filteredLocs.hist('photons_normalized',bins=1000)
filteredLocs.hist('photons',bins=1000)

backGroundLocs.hist('photons_normalized',bins=1000)
backGroundLocs.hist('photons',bins=1000)

#plot by binding site
def createPlot(df, groupNumber = [0], bindingSite = 0, filterByGroup = True, normalized = True):
    #if filter by group true:
    if filterByGroup:
        group = df.loc[(df.group.isin(groupNumber)) & (df.bindingSite == bindingSite)]
    else:
        group = df.loc[df.bindingSite == bindingSite]
  
    #plot group histogram photons
    if normalized:
        group.hist(column='photons_normalized',bins=40)
    else:
        group.hist(column='photons',bins=40)

    #plot histo frames
    group.hist(column='frame', bins=40)
    
    #plot group photons / frame
    if normalized:
        group.plot.scatter(x='frame', y='photons_normalized')
    else:
       group.plot.scatter(x='frame', y='photons') 
    
    return


#createPlot(filteredLocs, groupNumber = [0], bindingSite = 0, normalized=True)
#createPlot(filteredLocs, bindingSite = 12, filterByGroup = False)
createPlot(filteredLocs, bindingSite = 0, filterByGroup = False, normalized = False)

#plot all binding sites seperately
#for i in range(max(filteredLocs['bindingSite'])):
#    createPlot(filteredLocs, bindingSite = i, filterByGroup = False, normalized = False)
#    print(i)


#get number of binding sites per object

def bindingSitePlot(df, groupNumber = 0, numberOfBindingSites = len(centeroids)):
    group = df.loc[df.group == groupNumber]
    bindingSites = group.groupby('bindingSite',as_index=False).count().drop(['x', 'y', 'photons', 'sx', 'sy', 'bg', 'lpx', 'lpy', 
                                        'meanPHOTONS', 'photons_normalized'],axis=1)
    #bindingSites['group'] = groupNumber
    #bindingSites.rename(index=str,columns={'frame':'numberOfLocalizations'},inplace=True)
    #print(bindingSites)
    #group.hist(column='bindingSite',bins=numberOfBindingSites)
    count,division = np.histogram(group['bindingSite'], bins=numberOfBindingSites)
    return count

#binding sites
numberOfBindingSites = len(filteredLocs['bindingSite'].unique())    
bindingSiteDF = pd.DataFrame(columns=list(range(numberOfBindingSites))).astype(int)   
for i in range(len(filteredLocs['group'].unique())):
    bindingSiteDF.loc[i] = bindingSitePlot(filteredLocs, groupNumber = i)
    
#background
numberOfBackgroundSites = len(backGroundLocs['bindingSite'].unique())  
backgroundDF = pd.DataFrame(columns=list(range(numberOfBackgroundSites))).astype(int)    
for i in range(len(backGroundLocs['group'].unique())):
    backgroundDF.loc[i] = bindingSitePlot(backGroundLocs, groupNumber = i, numberOfBindingSites = numberOfBackgroundSites)


backgroundStats = backgroundDF.describe()
backgroundMean = np.mean(backgroundStats.loc['mean'].values)

#incrementally alter background to try to improve false posiitive rate
#for i in [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 100, 150]:
for i in [5]:    
    #backgroundMean = backgroundMean + 25
    backgroundMean = i
        
    bindingSiteStatDF = pd.DataFrame()
    
    bindingSiteStatDF['zeros'] = (bindingSiteDF < backgroundMean).astype(int).sum(axis=1)
    bindingSiteStatDF['numberOfBindingSites'] = (numberOfBindingSites - bindingSiteStatDF['zeros'])
    
    #fig5, ax3 = plt.subplots()
#    fig5 = bindingSiteStatDF.hist(column='numberOfBindingSites', bins=numberOfBindingSites+1)
#    fig5.flatten()[0].set_xlabel('number of binding sites per origami')
#    fig5.flatten()[0].set_ylabel('number of origami')
    
    stats = bindingSiteDF.describe()
    ind = np.arange(numberOfBindingSites)
    siteMean = stats.loc['mean'].values
    siteStd = stats.loc['std'].values
    
#    fig6, ax4 = plt.subplots()
#    ax4.bar(ind,siteMean, width=0.5, yerr = siteStd)
#    ax4.set_xlabel('binding site')
#    ax4.set_ylabel('mean localizations per origami')
    
    
    siteMap = bindingSiteDF > backgroundMean
    siteMap_stats = siteMap.describe()
    siteFrequency = siteMap_stats.loc['freq'].values
    
    numberOfGroups = len(filteredLocs['group'].unique())
    
    sitePercent = siteFrequency / numberOfGroups
    
#    fig7, ax5 = plt.subplots()
#    ax5.bar(ind,sitePercent, width=0.5)
#    ax5.set_ylabel('site frequency (%)')
#    ax5.set_xlabel('binding site')
    
    centeroidGroups=range(len(centeroids))
    
#    fig8, ax6 = plt.subplots()
#    scatter = ax6.scatter(centeroids[:,0],centeroids[:,1], s=800, c=sitePercent, cmap='hot',edgecolors='black',linewidths=1)
#    legend = ax6.legend(*scatter.legend_elements(),
#                    loc="lower left", title="site frequency")
#    #ax6.axis([0,512,0,512])
#    ax6.add_artist(legend)  
#    for i,txt in enumerate(centeroidGroups):
#        ax6.annotate(txt, (centeroids[i][0]+0.02,centeroids[i][1]))
    
    
    
    decodeDF = siteMap.astype(int)
    decodeRenameDF = decodeDF.rename(columns={   33:2,
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
                                                 })
    
    
    
    decodeReorderDF = decodeRenameDF.reindex(sorted(decodeRenameDF.columns), axis=1)
    
    savePath2 = filePath.split('.')[0] + '_incrementaBackground_{}.csv'.format(i)    
    decodeReorderDF.to_csv(savePath2, header=False, index=False)
    print(i)




