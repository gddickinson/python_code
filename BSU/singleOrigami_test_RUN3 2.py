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
from scipy import spatial
from scipy.optimize import minimize, dual_annealing

from skimage import restoration
from multiprocessing import Process, Pipe

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

class LocalizationCluster:
    def __init__(self,grid,localizations,recenter):
        #grid NX2 array of x,y localizations NX3 array of x,y,prec
        self.grid = np.copy(grid)
        self.gridTran = np.copy(grid)
        self.localizations = np.copy(localizations)
        self.weight = 1/localizations[:,2]
        self.nnTree = []
        self.nn = []
        self.dx = 0
        self.dy = 0
        self.dt = 0
        
        #Center grid and localizations on 0,0
        xGAve = 0
        yGAve = 0
        gCount = 0
        xLAve = 0
        yLAve = 0
        lCount = 0
        self.uAve=0
        for row in range(self.grid.shape[0]):
            xGAve+=self.grid[row,0]
            yGAve+=self.grid[row,1]
            gCount+=1
            
        for row in range(self.localizations.shape[0]):
            xLAve+=self.localizations[row,0]
            yLAve+=self.localizations[row,1]
            self.uAve += self.localizations[row,2]
            lCount+=1
        
        xGAve/=gCount
        yGAve/=gCount
        
        xLAve/=lCount
        yLAve/=lCount
        self.uAve/=lCount
        
        if recenter:
            for row in range(self.grid.shape[0]):
                self.grid[row,0]-=xGAve
                self.grid[row,1]-=yGAve
                
            for row in range(self.localizations.shape[0]):
                self.localizations[row,0]-=xLAve
                self.localizations[row,1]-=yLAve
                
            self.roughClock()
            
        self.weightDistMatrix = np.zeros((self.localizations.shape[0],self.gridTran.shape[0]))
        self.wdmComputed = False

    def squareNNDist(self,tm):
        self.dx = tm[0]
        self.dy = tm[1]
        self.dt = tm[2]
        rotMat = np.array([[np.cos(self.dt),-np.sin(self.dt)],[np.sin(self.dt),np.cos(self.dt)]])
        self.gridTran = np.dot(self.grid,rotMat)
        self.gridTran[:,0]+=self.dx
        self.gridTran[:,1]+=self.dy
        self.nnTree = spatial.cKDTree(self.gridTran)
        self.nn = self.nnTree.query(self.localizations[:,0:2])
        self.wdmComputed = False
        return float(sum(np.multiply(self.nn[0],self.weight)**2))
    
    def roughClock(self):
        minObj = self.squareNNDist([self.dx,self.dy,0])
        minTheta = 0
        for thetaId in range(180):
            theta = thetaId*np.pi/180
            obj = self.squareNNDist([self.dx,self.dy,theta])
            if obj<minObj:
                minObj = obj
                minTheta=theta
        self.dt = minTheta
        self.wdmComputed = False
        return self.squareNNDist([self.dx,self.dy,self.dt])
    
    def computeWeightDistMatrix(self):
        for locId in range(self.localizations.shape[0]):
            for gridId in range(self.gridTran.shape[0]):
                self.weightDistMatrix[locId,gridId] = self.localizations[locId,2]**2/((self.localizations[locId,0]-self.gridTran[gridId,0])**2+(self.localizations[locId,1]-self.gridTran[gridId,1])**2)
        self.wdmComputed=True
        
    def likelyhoodScore(self,image,*args):
        score = 0
        
        if not self.wdmComputed:
            self.computeWeightDistMatrix()
        
        targetSum = args[0]
        sumWeight = args[1]
        
        for locId in range(self.localizations.shape[0]):
            locScoreInv = sum(np.dot(self.weightDistMatrix,image))
            score += 1/locScoreInv
            
        score += sumWeight*(sum(image)-targetSum)**2
        
        return score
    
def mpClusterFit(lc,index,conn):
    #if verbose:
        #    print(lc.dt)
    out = minimize(lc.squareNNDist,[lc.dx,lc.dy,lc.dt],method='Nelder-Mead')
    lc.squareNNDist(out.x)
    #if verbose:
    #   print(lc.dt)
        
    bounds = np.array([[-.225+out.x[0],.225+out.x[0]],[-.225+out.x[1],.225+out.x[1]],[-np.pi/6+out.x[2],np.pi/6+out.x[2]]])    
    out = dual_annealing(lc.squareNNDist,bounds,x0=out.x)
    lc.squareNNDist(out.x)
    #print(self.dx,self.dy,self.dt)
    conn.send([index,lc.dx,lc.dy,lc.dt])


if __name__ == '__main__':       
    #set group number
    groupNumbers = [i for i in range(0,11794,1)]
    #groupNumbers = [3,167]
    
    #groupNumbers = [0]
    
    distThreshold = 5
    pixelsize = 106.66667
    
    scaled_threshold = 500
    
    display = False
    display2 = False
    verbose = False
    
    #set filepath
    
    #filtered by photons averaged dataset
    filePath = r"Y:\George_D_DATA\2019-09-13\fromIAPETUS\run1\20190913_All-Matrices_syn2_pure_Triangles_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_12mM_PCD_TROLOX_1mM_10_38_52_substack_fixed_locs_render_DRIFT_3_filter_manual2-picked.hdf5"
    #filePath = r"20190913_All-Matrices_syn2_pure_Triangles_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_12mM_PCD_TROLOX_1mM_13_42_03_fixed_locs_render_DRIFT_3_filter_picked_manual_avg.hdf5"   
    #filePath = r"20190913_george_test2_conv_locs_render_render_picked_filter.hdf5"
    #filePath = r"20190913_All-Matrices_syn2_pure_Triangles_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_12mM_PCD_TROLOX_1mM_13_42_03_fixed_locs_render_DRIFT_3_filter_picked_automatic.hdf5"
    #filePath = r"20190930_Matrix-3_syn2_pure_Triangles_300msExp_Mid-9nt-3nM_MgCl2_18mM_PCA_12mM_PCD_TROLOX_1mM_11_18_45_fixed_locs_render_DRIFT_4_filter_picked_manual.hdf5"
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
    
    
    if display:
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
    
    nShifts = 0
    #filter for one origami
    
    localizationClusterList = []
    
    for groupNumber in groupNumbers:
        print(groupNumber,"read")
        sublocs = locs[locs['group']==groupNumber]
        
        x = sublocs['x']
        y = sublocs['y']
        photons=sublocs['photons']
        lpx = sublocs['lpx']
        lpy = sublocs['lpy']
        
        localizations = np.array([x,y,lpx]).T
        if localizations.shape[0]==0:
            continue;
        
        
        #if display:
        #plt.figure(4)
            #fig4, ax2 = plt.subplots()
            #ax2.scatter(x,y, s=0.1, color='black')
            
            ##filter locs by centeroid positions
            #searchArea = 0.035 * 0.035
            #filteredLocs= pd.DataFrame()
            
            #
            #### UNCOMMENT ON FIRST RUN  ########
            #for i in range(len(centeroids)):
                #query = "SELECT * FROM locs WHERE (((locs.x - {})*(locs.x - {})) + ((locs.y - {})*(locs.y - {}))) <= ({})".format(centeroids[i][0], centeroids[i][0], centeroids[i][1], centeroids[i][1], searchArea)
                #filtered = ps.sqldf(query,locals())
                #filtered['bindingSite'] = i
                #filteredLocs = filteredLocs.append(filtered)
                #print(i)
            
            ##export filteredDF
            #filteredLocs.to_csv(savePath)
            
            
            #### COMMENT OUT ON FIRST RUN #######
            ##load filteredDF
            #filteredLocs = pd.read_csv(savePath)
            
            
            ##########################################################################################################
            
            #filteredLocs.plot.scatter(x='x',y='y', s=0.1, color='black')
            
            #ax2.scatter(x=filteredLocs.x, y=filteredLocs.y, s=0.1, color='blue')
            #ax2.scatter(centeroids[:,0],centeroids[:,1], color='red')
            
            #centeroidGroups=range(len(centeroids))
            
            #for i,txt in enumerate(centeroidGroups):
            #    ax2.annotate(txt, (centeroids[i][0]+0.02,centeroids[i][1]))
            
            
            #get number of binding sites per object
            #def bindingSitePlot(df, groupNumber = 0, numberOfBindingSites = len(centeroids)):
            #    group = df.loc[df.group == groupNumber]
            #    count,division = np.histogram(group['bindingSite'], bins=numberOfBindingSites)
            #    return count
            
            #binding sites
            #numberOfBindingSites = len(filteredLocs['bindingSite'].unique())    
        #bindingSiteDF = pd.DataFrame(columns=list(range(numberOfBindingSites))).astype(int)   
        #for i in range(len(filteredLocs['group'].unique())):
        #    bindingSiteDF.loc[i] = bindingSitePlot(filteredLocs, groupNumber = i)
            
        
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
        lc = LocalizationCluster(centeroids,localizations,True)
        localizationClusterList.append(lc)
        
    processes = []
    parentConnections = []
    
    for index in range(len(localizationClusterList)):
        pconn,cconn = Pipe(False)
        proc = Process(target=mpClusterFit,args=(localizationClusterList[index],index,cconn,))
        processes.append(proc)
        parentConnections.append(pconn)
        #mpClusterFit(lc)
        processes[-1].start()
        
        #if verbose:
        #    print(lc.dt) 
      
    for pconn in parentConnections:
        msg = pconn.recv();
        print(msg[0],'fitting done')
        localizationClusterList[msg[0]].squareNNDist(msg[1:])
        
    for proc in processes:
        proc.join()
        
    for lc in localizationClusterList:
        gridShape = (6,8)
        
        gridPoints = np.copy(lc.gridTran).reshape(gridShape[0],gridShape[1],2)
        
        rx=0
        ry=0
        cx=0
        cy=0
        
        
        for rid in range(1,gridShape[0]):
            for cid in range(0,gridShape[1]):
                rx += gridPoints[rid,cid,0]-gridPoints[rid-1,cid,0]
                ry += gridPoints[rid,cid,1]-gridPoints[rid-1,cid,1]
                
        for rid in range(0,gridShape[0]):
            for cid in range(1,gridShape[1]):
                cx += gridPoints[rid,cid,0]-gridPoints[rid,cid-1,0]
                cy += gridPoints[rid,cid,1]-gridPoints[rid,cid-1,1]
        
        rx/=(gridShape[0]-1)*gridShape[1]
        ry/=(gridShape[0]-1)*gridShape[1]
        cx/=gridShape[0]*(gridShape[1]-1)
        cy/=gridShape[0]*(gridShape[1]-1)
        
        minDeltaR = 0
        minDeltaC = 0
    
        dx = lc.dx
        dy = lc.dy
        dt = lc.dt
        
        minObj = lc.squareNNDist([dx,dy,dt])
        for deltaR in range(-2,3):
            for deltaC in range(-2,3):
                obj3 = lc.squareNNDist([dx+deltaR*rx+deltaC*cx,dy+deltaR*ry+deltaC*cy,dt])
                if obj3 < minObj:
                    minObj = obj3
                    minDeltaR = deltaR
                    minDeltaC = deltaC
        
        obj3 = lc.squareNNDist([dx+minDeltaR*rx+minDeltaC*cx,dy+minDeltaR*ry+minDeltaC*cy,dt])
        gridPoints = np.copy(lc.gridTran).reshape(gridShape[0],gridShape[1],2)
        
        superGridPoints = np.zeros((gridShape[0]+2,gridShape[1]+2,2))
        
        for rid in range(0,gridShape[0]):
            for cid in range(0,gridShape[1]):
                superGridPoints[rid+1,cid+1,:] = gridPoints[rid,cid,:]
                
        for rid in range(gridShape[0]+2):
            superGridPoints[rid,0,0] = gridPoints[0,0,0] - rx - cx + rid * rx
            superGridPoints[rid,0,1] = gridPoints[0,0,1] - ry - cy + rid * ry
            superGridPoints[rid,-1,0] = gridPoints[-1,-1,0] + rx + cx - rid * rx
            superGridPoints[rid,-1,1] = gridPoints[-1,-1,1] + ry + cy - rid * ry
            
        for cid in range(1,gridShape[1]+1):
            superGridPoints[0,cid,0] = gridPoints[0,0,0] - rx - cx + cid * cx
            superGridPoints[0,cid,1] = gridPoints[0,0,1] - ry - cy + cid * cy
            superGridPoints[-1,cid,0] = gridPoints[-1,-1,0] + rx + cx - cid * cx
            superGridPoints[-1,cid,1] = gridPoints[-1,-1,1] + ry + cy - cid * cy
        
        superGrid = np.copy(superGridPoints).reshape((superGridPoints.shape[0]*superGridPoints.shape[1],superGridPoints.shape[2]))
        
        lc2 = LocalizationCluster(superGrid,lc.localizations,False)
        #out2 = minimize(lc2.squareNNDist,[0,0,0],method='Nelder-Mead')
        #obj2 = lc2.squareNNDist(out2.x)
        obj2 = lc2.squareNNDist([0,0,0])
        
        if display2:
            plt.figure()
            plt.scatter(lc.localizations[:,0],lc.localizations[:,1],s=.1,color='blue')
            plt.scatter(lc.gridTran[:,0],lc.gridTran[:,1],color='orange')
            plt.scatter(lc.grid[:,0],lc.grid[:,1],color='red')
            plt.scatter(superGrid[:,0],superGrid[:,1],s=3,color='black')
            plt.scatter(lc2.gridTran[:,0],lc2.gridTran[:,1],s=2,color='green')
    
        
        
        hist = np.zeros((lc2.grid.shape[0]))
        
        for loc in range(len(lc2.nn[0])):
            if lc2.nn[0][loc] < distThreshold/pixelsize:
                hist[lc2.nn[1][loc]]+=lc2.weight[loc]
        
        if display2:        
            fig, axt = plt.subplots(3,2)
            axt[0,0].bar([i for i in range(len(hist))],hist.tolist())
        
        kernel = np.zeros((3,3))
        
        sigma = max(0.5,lc.uAve/((np.sqrt(rx**2+ry**2)+np.sqrt(cx**2+cy**2))/2))
        #print(sigma)
        sq2sigma = np.sqrt(2)*sigma
        xc = 1.0
        yc = 1.0
        
        for xi in range(3):
            xp = xi - xc
            for yi in range(3):
                yp = yi  - yc
                kernel[yi,xi] = 1/4*(np.math.erf((xp+.5)/sq2sigma)-np.math.erf((xp-.5)/sq2sigma))*(np.math.erf((yp+.5)/sq2sigma)-np.math.erf((yp-0.5)/sq2sigma))
                
        kernel /= sum(sum(kernel))
        scale = max(hist)*2     
        signal = hist.reshape(superGridPoints.shape[0],superGridPoints.shape[1])/scale
        rec = restoration.richardson_lucy(signal,kernel,50)
        rec *= sum(sum(signal))/sum(sum(rec))*scale
        
        if display2:
            axt[1,0].imshow(signal)
            axt[1,1].imshow(rec)
        hist2 = rec.reshape(hist.shape)
    
        if display2:       
            axt[0,1].bar([i for i in range(len(hist2))],hist2.tolist())
        
        binaryImage = np.copy(rec)[1:-1,1:-1]
        for rid in range(binaryImage.shape[0]):
            for cid in range(binaryImage.shape[1]):
                if binaryImage[rid,cid] > scaled_threshold:
                    binaryImage[rid,cid] = 1
                else:
                    binaryImage[rid,cid] = 0
        
        if display2:        
            axt[2,1].imshow(binaryImage)
            
            superRes = np.zeros((60,60))
            
            for rid in range(lc2.localizations.shape[0]):
                x = int(-lc2.localizations[rid,1]*pixelsize/2+superRes.shape[0]/2)
                y = int(-lc2.localizations[rid,0]*pixelsize/2+superRes.shape[1]/2)
                if x > 0 and x<superRes.shape[0] and y > 0 and y < superRes.shape[1]:
                    superRes[x,y] += 1
                    
            axt[2,0].imshow(superRes)
            
        #binaryImage = np.array([[0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,0],[1,1,0,0,0,0,1,0],[0,0,1,1,1,1,0,1],[0,0,1,0,1,1,0,0],[0,0,0,0,1,0,0,0]])
            
        rShifts = [0]
        cShifts = [0]
        
        rSums = np.sum(binaryImage,axis=0)
        cSums = np.sum(binaryImage,axis=1)
        
        if rSums[0] == 0:
            rShifts.append(-1)
        if rSums[-1] == 0:
            rShifts.append(1)
        if cSums[0] == 0:
            cShifts.append(-1)
        if cSums[-1] == 0:
            cShifts.append(1) 
        
        for rShift in rShifts:
            for cShift in cShifts:
                binaryImageShifted = np.roll(binaryImage,(cShift,rShift),(0,1))
                binaryData = binaryImageShifted.reshape((binaryImage.shape[0]*binaryImage.shape[1]))
                binaryString=""
                
                if not (rShift == 0 and cShift == 0):
                    nShifts += 1
                    if display2:
                        plt.figure()
                        plt.imshow(binaryImageShifted)
                
                for bit in binaryData:
                    if bit==0:
                        binaryString+='0'
                    else:
                        binaryString+='1'
                
                with open('read_data','a') as fup:
                    fup.write(binaryString+'\n')
                    
    print(len(groupNumbers),nShifts)