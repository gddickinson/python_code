# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 10:17:10 2018

@author: George
"""

import exifread
# Open image file for reading (binary mode)
f = open(r"C:\Users\George\Desktop\UCI\testStacks\from_IanS\SHSY_8ms__9_MMStack_Pos0.ome.tif", 'rb')

# Return Exif tags
tags = exifread.process_file(f)

# Print the tag/ value pairs
for tag in tags.keys():
    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
        print ("Key: %s, value %s" % (tag, tags[tag]))


