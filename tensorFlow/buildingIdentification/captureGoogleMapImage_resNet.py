"""
Stitch together Google Maps images from lat, long coordinates
Based on work by heltonbiker and BenElgar
Changes: 
  * updated for Python 3
  * added Google Maps API key (compliance with T&C, although can set to None)
  * handle http request exceptions
"""

import requests
from io import BytesIO
from math import log, exp, tan, atan, pi, ceil
from PIL import Image
import sys

EARTH_RADIUS = 6378137
EQUATOR_CIRCUMFERENCE = 2 * pi * EARTH_RADIUS
INITIAL_RESOLUTION = EQUATOR_CIRCUMFERENCE / 256.0
ORIGIN_SHIFT = EQUATOR_CIRCUMFERENCE / 2.0
GOOGLE_MAPS_API_KEY = None  # set to 'your_API_key'
#GOOGLE_MAPS_API_KEY = "AIzaSyC5gyrsTtaX4qnA63RqyFpSaWjcIDHCAio"

def latlontopixels(lat, lon, zoom):
    mx = (lon * ORIGIN_SHIFT) / 180.0
    my = log(tan((90 + lat) * pi/360.0))/(pi/180.0)
    my = (my * ORIGIN_SHIFT) /180.0
    res = INITIAL_RESOLUTION / (2**zoom)
    px = (mx + ORIGIN_SHIFT) / res
    py = (my + ORIGIN_SHIFT) / res
    return px, py

def pixelstolatlon(px, py, zoom):
    res = INITIAL_RESOLUTION / (2**zoom)
    mx = px * res - ORIGIN_SHIFT
    my = py * res - ORIGIN_SHIFT
    lat = (my / ORIGIN_SHIFT) * 180.0
    lat = 180 / pi * (2*atan(exp(lat*pi/180.0)) - pi/2.0)
    lon = (mx / ORIGIN_SHIFT) * 180.0
    return lat, lon

def getNWSECorners(centerPoint,zoom, xDim, yDim):
    res = INITIAL_RESOLUTION / (2**zoom)
    
    centerY, centerX = latlontopixels(centerPoint[1], centerPoint[0], zoom)
    NWcornerX = centerX + (yDim / res) - (yDim / 76)
    NWcornerY = centerY - (xDim / res) + (xDim / 76)
    
    SEcornerX = centerX - (yDim / res) + (yDim / 76)
    SEcornerY = centerY + (xDim / res) - (xDim / 76) 
    
    NWCornerLat, NWCornerLong = pixelstolatlon(NWcornerY, NWcornerX, zoom)
    SECornerLat, SECornerLong = pixelstolatlon(SEcornerY, SEcornerX, zoom)
    
    return (NWCornerLat, NWCornerLong),(SECornerLat, SECornerLong)


def get_maps_image(NW_lat_long, SE_lat_long, zoom=18):

  ullat, ullon = NW_lat_long
  lrlat, lrlon = SE_lat_long

  # Set some important parameters
  scale = 1
  maxsize = 640

  # convert all these coordinates to pixels
  ulx, uly = latlontopixels(ullat, ullon, zoom)
  lrx, lry = latlontopixels(lrlat, lrlon, zoom)

  # calculate total pixel dimensions of final image
  dx, dy = lrx - ulx, uly - lry

  # calculate rows and columns
  cols, rows = int(ceil(dx/maxsize)), int(ceil(dy/maxsize))

  # calculate pixel dimensions of each small image
  bottom = 120
  largura = int(ceil(dx/cols))
  altura = int(ceil(dy/rows))
  alturaplus = altura + bottom

  # assemble the image from stitched
  final = Image.new("RGB", (int(dx), int(dy)))
  for x in range(cols):
      for y in range(rows):
          dxn = largura * (0.5 + x)
          dyn = altura * (0.5 + y)
          latn, lonn = pixelstolatlon(ulx + dxn, uly - dyn - bottom/2, zoom)
          position = ','.join((str(latn), str(lonn)))
          print(x, y, position)
          urlparams = {'center': position,
                        'zoom': str(zoom),
                        'size': '%dx%d' % (largura, alturaplus),
                        'maptype': 'satellite',
                        'sensor': 'false',
                        'scale': scale}
          if GOOGLE_MAPS_API_KEY is not None:
            urlparams['key'] = GOOGLE_MAPS_API_KEY

          url = 'http://maps.google.com/maps/api/staticmap'
          try:                  
            response = requests.get(url, params=urlparams)
            response.raise_for_status()
          except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

          im = Image.open(BytesIO(response.content))                  
          final.paste(im, (int(x*largura), int(y*altura)))

  return final

############################################

if __name__ == '__main__':

  # location
  #NW_lat_long =  (43.523902,-114.321426)
  #SE_lat_long = (43.522107,-114.317918)

  centerPoint = (-114.318634, 43.522553) #(long,lat)

  zoom = 19   # be careful not to get too many images!

  #for 100,100 pixel crop: 15,15
  #for 1000,1000 pixel crop 150,150
  #for 1000,2000 pixel crop 300,150 -> for tensorflow analysis
  NW_lat_long, SE_lat_long = getNWSECorners(centerPoint,zoom, 15, 15)



  result = get_maps_image(NW_lat_long, SE_lat_long, zoom=zoom)
  result.show()