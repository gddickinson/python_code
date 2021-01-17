# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 09:43:35 2017

@author: George
"""

from PIL import Image
import os

def crop(infile,height,width):
    im = Image.open(infile)
    imgwidth, imgheight = im.size
    for i in range(imgheight-height):
        for j in range(imgwidth-width):
            box = (j, i, (j+1)*width, (i+1)*height)
            yield im.crop(box)

if __name__=='__main__':
    infile=r"D:\\neuralNet_data\\AerialImageDataset\\AerialImageDataset\\test\\cropped\\IMG-425.jpg"
    height=100
    width=100
    start_num=0
    for k,piece in enumerate(crop(infile,height,width),start_num):
        img=Image.new('RGB', (height,width), 255)
        img.paste(piece)
        path=os.path.join(r"D:\\neuralNet_data\\AerialImageDataset\\AerialImageDataset\\test\\mapSections2\\" ,  "IMG-%s.jpg" % k)
        img.save(path,"JPEG")
        print(path)
    