# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 17:00:13 2015

@author: George
"""

src=scipy.misc.lena()
c_in=0.5*array(src.shape)
c_out=array((256.0,256.0))
for i in xrange(0,7):
    a=i*15.0*pi/180.0
    transform=array([[cos(a),-sin(a)],[sin(a),cos(a)]])
    offset=c_in-c_out.dot(transform)
    dst=scipy.ndimage.interpolation.affine_transform(
        src,transform.T,order=2,offset=offset,output_shape=(512,512),cval=0.0,output=float32
    )
    subplot(1,7,i+1);axis('off');imshow(dst,cmap=cm.gray)
show()