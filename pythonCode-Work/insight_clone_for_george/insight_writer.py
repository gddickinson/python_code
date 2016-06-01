# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 18:10:38 2016

@author: kyle
"""
import numpy as np
import struct

def i3DataType():
    return np.dtype([('x', np.float32),   # original x location
                    ('y', np.float32),   # original y location
                    ('xc', np.float32),  # drift corrected x location
                    ('yc', np.float32),  # drift corrected y location
                    ('h', np.float32),   # fit height
                    ('a', np.float32),   # fit area
                    ('w', np.float32),   # fit width
                    ('phi', np.float32), # fit angle (for unconstrained elliptical gaussian)
                    ('ax', np.float32),  # peak aspect ratio
                    ('bg', np.float32),  # fit background
                    ('i', np.float32),   # sum - baseline for pixels included in the peak
                    ('c', np.int32),     # peak category ([0..9] for STORM images)
                    ('fi', np.int32),    # fit iterations
                    ('fr', np.int32),    # frame
                    ('tl', np.int32),    # track length
                    ('lk', np.int32),    # link (id of the next molecule in the trace)
                    ('z', np.float32),   # original z coordinate
                    ('zc', np.float32)]) # drift corrected z coordinate
                    
def _putV(fp, format, data):
    fp.write(struct.pack(format, data))
    
def getMolecules(pts,tracks):
    data = np.zeros(len(pts), dtype = i3DataType())
    t=pts[:,0]
    pts_txy=np.hstack((t[:,None],pts[:,3:5]))
    for track in tracks:
        track_length = len(track)
        for i, pt in enumerate(track):
            idx=np.argwhere(np.all(pts_txy==pt,1))[0][0]
            data[idx]['fr']=pts[idx][0]
            data[idx]['x' ]=pts[idx][1]
            data[idx]['y' ]=pts[idx][2]
            data[idx]['xc']=pts[idx][3]
            data[idx]['yc']=pts[idx][4]
            data[idx]['w' ]=pts[idx][5]
            data[idx]['h' ]=pts[idx][6]
            if i+1==track_length:
                data[idx]['lk']=-1
            else:
                data[idx]['lk']=np.argwhere(np.all(pts_txy==track[i+1],1))[0][0]
    return data
    
    
def write_insight_bin(filename, pts, tracks):
    frames=int(np.max(pts[:,0]))
    
    fp = open(filename, "wb")
    _putV(fp, "4s", "M425")
    _putV(fp, "i", frames)
    _putV(fp, "i", 6) # *int32 ;% identified = 2, traced = 3, tracked = 4, stormed = 6
    _putV(fp, "i", 0)
    
    molecules=getMolecules(pts,tracks)
    molecules.tofile(fp)
    nMolecules=len(pts)
    
    _putV(fp, "i", 0)
    fp.seek(12)
    _putV(fp, "i", nMolecules)
    fp.close()
    
    
if __name__=='__main__':
    filename=r'C:\Users\kyle\Desktop\test2.bin'
    
    