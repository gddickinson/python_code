# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 14:44:12 2016


Algorithm:
1) Gaussian Blur
2) High pass butterworth filter

@author: kyle
"""
import numpy as np
import sys
sys.path.insert(0, os.path.expanduser(r'~\Desktop\insight_clone_for_george'))
from insight_writer import write_insight_bin


def Export_pts_from_MotilityTracking():
    tracks=g.m.trackPlot.all_tracks
    t_out=[]
    x_out=[]
    y_out=[]
    for i in np.arange(len(tracks)):
        track=tracks[i]
        t_out.extend(track['frames'])
        x_out.extend(track['x_cor'])
        y_out.extend(track['y_cor'])
    p_out=np.array([t_out,x_out,y_out]).T
    filename=r'C:\Users\kyle\Desktop\trial8_pts.txt'
    np.savetxt(filename,p_out)
    
    
def getSigma():
    ''' This function isn't complete.  I need to cut out a 20x20 pxl window around large amplitude particles '''
    from gaussianFitting import fitGaussian
    I=g.m.currentWindow.image
    xorigin=8
    yorigin=9
    sigma=2
    amplitude=50
    p0=[xorigin, yorigin, sigma,amplitude]
    p, I_fit, _ =fitGaussian(I,p0)
    xorigin, yorigin, sigma,amplitude = p
    return sigma

def gaussian(x,y,xorigin,yorigin,sigma,amplitude):
    '''xorigin,yorigin,sigmax,sigmay,angle'''
    return amplitude*(np.exp(-(x-xorigin)**2/(2.*sigma**2))*np.exp(-(y-yorigin)**2/(2.*sigma**2)))
    
def generate_gaussian(mx,sigma=1.15):
    assert mx%2==1 #mx must be odd
    x=np.arange(mx)
    y=np.arange(mx)
    xorigin=int(np.floor(mx/2.))
    yorigin=xorigin
    amplitude=1
    I=gaussian(x[:,None], y[None,:],xorigin,yorigin,sigma,amplitude)
    I=I-(np.sum(I)/mx**2)
    return I
    
def convolve(I,sigma):
    from scipy.signal import convolve2d
    G=generate_gaussian(17,sigma)
    newI=np.zeros_like(I)
    for t in np.arange(len(I)):
        print(t)
        newI[t]=convolve2d(I[t], G, mode='same', boundary='fill', fillvalue=0)
    return newI
    
def get_points(I):
    import scipy.ndimage
    s=scipy.ndimage.generate_binary_structure(3,1)
    labeled_array, num_features = scipy.ndimage.measurements.label(I, structure=s)
    objects=scipy.ndimage.measurements.find_objects(labeled_array)
    
    all_pts=[]
    for loc in objects:
        offset=np.array([a.start for a in loc])
        pts=np.argwhere(labeled_array[loc]!=0)+offset
        ts=np.unique(pts[:,0])
        for t in ts:
            pts_t=pts[pts[:,0]==t]
            x=np.mean(pts_t[:,1])
            y=np.mean(pts_t[:,2])
            all_pts.append([t,x,y])
    all_pts=np.array(all_pts)
    return all_pts
    
def extend_track(track,pts,pts_remaining):
    pt=track[-1]
    t,x,y=pt
    pts_subset=pts[pts_remaining]
    # pt can move less than two pixels in one frame, two frames can be skipped
    for dt in [1,2,3]:
        candidates=np.argwhere(pts_subset[:,0]==t+dt).T[0]
        if len(candidates)==0:
            continue
        if len(candidates)==1:
            distances=np.array([np.sqrt(np.sum((np.squeeze(pts_subset[candidates,1:3])-np.array([x,y]))**2))])
        elif len(candidates)>1:
            distances=np.sqrt(np.sum((np.squeeze(pts_subset[candidates,1:3])-np.array([x,y]))**2,1))
        if any(distances<3):
            next_pt_idx=candidates[np.argmin(distances)]
            track.append(pts_subset[next_pt_idx])
            pts_remaining[np.argwhere(pts_remaining)[next_pt_idx][0]]=False
            track,pts_remaining=extend_track(track,pts,pts_remaining)
            return track,pts_remaining
    return track, pts_remaining
            
def link_pts(pts):
    if pts.shape[1]>3:
        t=pts[:,0]
        pts=np.hstack((t[:,None],pts[:,3:5]))
    tracks=[]
    pts_remaining=np.ones(len(pts),dtype=np.bool)
    while np.any(pts_remaining):
        pt_idx=np.argwhere(pts_remaining)[0][0]
        pt=pts[pt_idx]
        pts_remaining[pt_idx]=False
        track=[pt]
        track,pts_remaining=extend_track(track,pts,pts_remaining)
        tracks.append(track)
    return tracks
    
def cutout(pt,Movie,width):
    assert width%2==1 #mx must be odd
    t,x,y=pt
    mid=int(np.floor(width/2))
    x0=int(x-mid)
    x1=int(x+mid)
    y0=int(y-mid)
    y1=int(y+mid)
    mt,mx,my=Movie.shape
    if y0<0: y0=0
    if x0<0: x0=0
    if y1>=my: y1=my-1
    if x1>=mx: x1=mx-1
    corner=[x0,y0]
    I=Movie[t,x0:x1+1,y0:y1+1]
    return I, corner

    
        
def refine_pts(pts,Movie):
    from gaussianFitting import fitGaussian
    new_pts=[]
    for pt in pts:
        print(pt)
        width=9
        mid=int(np.floor(width/2))
        I, corner=cutout(pt,Movie,width)
        xorigin=mid; yorigin=mid; sigma=1.1; amplitude=50
        p0=[xorigin,yorigin,sigma,amplitude]
        fit_bounds = [(0,9), (0,9),  (0,4),    (0,1000)]
        p, I_fit, _ = fitGaussian(I,p0, fit_bounds)
        xfit=p[0]+corner[0]
        yfit=p[1]+corner[1]
        new_pts.append([pt[0],pt[1],pt[2],xfit,yfit,p[2],p[3]])
    new_pts=np.array(new_pts)
    return new_pts
           
    
    
#inside Flika
'''
open_file(r'J:\WORK_IN_PROGRESS\Nikon_System_Data\Best examples\SY5Y\Tubulin\130903_SY5Y_Tubulin_405_3D_003.nd2')
trim(1,5001)
butterworth_filter(1,.005,1)
set_value(0,0,10)
set_value(0,4990,5000)
#sigma=getSigma()
sigma=1.15
I=convolve(g.m.currentWindow.image,sigma)
Window(I)

'''
#pts=np.loadtxt(r'C:\Users\kyle\Desktop\trial8_pts.txt')

open_file(r'J:\WORK_IN_PROGRESS\Nikon_System_Data\Best examples\SY5Y\Tubulin\130903_SY5Y_Tubulin_405_3D_003_frames1-5000_convolved.tif')
I=g.m.currentWindow.image
threshold(1000)
pts=get_points(g.m.currentWindow.image)
np.savetxt(r'J:\WORK_IN_PROGRESS\Nikon_System_Data\Best examples\SY5Y\Tubulin\130903_SY5Y_Tubulin_405_3D_003_pts.txt',pts)  #####These can be imported into flika######
refined_pts=refine_pts(pts,I)

#tracks=link_pts(refined_pts)
#filename=r'C:\Users\kyle\Desktop\test_flika.bin'
#write_insight_bin(filename, refined_pts, tracks)












pg.plot(refined_pts[:,5])





