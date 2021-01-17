from arcpy import da
from arcpy import env
from arcpy.sa import *
import os, shutil
import arcpy
from os import path

#Environmental settings
arcpy.CheckOutExtension("Spatial")
env.overwriteOutput = True
workingDirectory = os.getcwd()


def str_to_bool(s):
    """Convert string to boolean"""
    if s == 'True':
        return True
    elif s == 'true':
        return True
    else:
        return False

### Arc Toolbox ####
#Get Toolbox GUI inputs
env.workspace = arcpy.GetParameterAsText(0)
fragstatsProgramPath = arcpy.GetParameterAsText(1)
polygon_shp = arcpy.GetParameterAsText(2)
rasterInput_path = arcpy.GetParameterAsText(3)
packageInstall = str_to_bool(arcpy.GetParameterAsText(4))
package = arcpy.GetParameterAsText(5)

#Included in case some packages are missing
import pip
def packageInstaller(package):
    try:
        pip.main(['install',package])
        arcpy.AddMessage(package + " succesfully installed")
    except:
        arcpy.AddMessage("package install failed for: " + package)

if packageInstall:
    packageInstaller(package)


import subprocess
import numpy as np
import re
import time
import traceback
import gc
import sys
from math import ceil
import pandas as pd
from pandas import read_csv
import csv
import glob

#make results folders if needed
if os.path.isdir(env.workspace + '\\clipFiles'):
    shutil.rmtree(env.workspace + '\\clipFiles')
os.mkdir(env.workspace + '\\clipFiles')

#paths
vertex_csv_path = env.workspace + r'\inputData\poly_vertex.csv'
rasterSaveFolder =  env.workspace + r'\clipFiles'
rasterSavePath =  rasterSaveFolder + '\\clip'
geoTiffPath =  env.workspace + r'\rasterConversion'

#helper functions
def sorted_nicely(l):
    """Sort function"""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)

def deleteFilesInFolder(folder):
    """Remove files from a folder"""
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #to remove subdiectories
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def startProcessMessage(processName):
    """Start of Process Message"""
    print(processName)
    arcpy.AddMessage("-------------------------------------------------------------------------")
    arcpy.AddMessage(processName + " Started")
    arcpy.AddMessage("-------------------------------------------------------------------------")
    return

def endProcessMessage (startTime, processName):
    """End of Process Message"""
    endTime = time.time()
    elapsedmin = ceil(((endTime - startTime) / 60)* 10)/10
    print(processName + " Complete in {0} minutes.".format(elapsedmin))
    arcpy.AddMessage("-------------------------------------------------------------------------")
    arcpy.AddMessage(processName + " completed after %s minutes." % (elapsedmin))
    arcpy.AddMessage("-------------------------------------------------------------------------")
    return



#main functions
def getPolygonCoordinates(shapeFile):
    """For each polygon geometry in a shapefile get the sequence number and
    and coordinates of each vertex and tie it to the OID of its corresponding
    polygon"""

    vertex_dict = {}
    s_fields = ['OID@', 'Shape@XY']
    pt_array = da.FeatureClassToNumPyArray(shapeFile, s_fields,
        explode_to_points=True)

    for oid, xy in pt_array:
        xy_tup = tuple(xy)

        if oid not in vertex_dict:
            vertex_dict[oid] = [xy_tup]
        # this clause ensures that the first/last point which is listed
        # twice only appears in the list once
        elif xy_tup not in vertex_dict[oid]:
            vertex_dict[oid].append(xy_tup)

    vertex_sheet = []
    for oid, vertex_list in vertex_dict.iteritems():
        for i, vertex in enumerate(vertex_list):
            vertex_sheet.append((oid, i, vertex[0], vertex[1]))

    return vertex_sheet


def clipRaster(pointsList):
    """For each polygon geometry in list, clip raster and save output"""

    numberOfPolygons =  (pointsList[-1][0]) + 1
    listOfPolygons = []
    finalList = []

    for i in range(numberOfPolygons):
        newRow = []
        for row in pointsList:
            if row[0] == i:
                newRow.append(arcpy.Point(row[2],row[3]))

        newRow.append(newRow[0])
        listOfPolygons.append(newRow)

    for i in range(numberOfPolygons):
        extPolygonOut = ExtractByPolygon(rasterInput_path, listOfPolygons[i], "INSIDE")
        finalList.append(extPolygonOut)
        savePath = rasterSavePath + "_" + str(i)
        extPolygonOut.save(savePath)
        arcpy.AddMessage("clip_{0} finished".format(i))

    #print(finalList)
    return finalList

def convertRasters(listOfRasters):
    """create geotiffs to use in fragstats"""
    strList = str(clipList).replace("[","").replace("]","").replace(",",';')
    arcpy.RasterToOtherFormat_conversion(strList, geoTiffPath,"TIFF")



try:
    #enable garbage collection
    gc.enable()

    #start timing
    startTime= time.time()

    ########## run ################
    startProcessMessage("Step 1 of 7 - Get Polygon Vertices")
    pointsList = getPolygonCoordinates(polygon_shp)
    endProcessMessage (startTime, "Get Polygon Vertices")

    startProcessMessage("Step 2 of 7 - Clipping")
    clipList = clipRaster(pointsList)
    endProcessMessage (startTime, "Clipping")

    startProcessMessage("Step 3 of 7 - Convert Rasters to geoTiffs")
    convertRasters(clipList)
    endProcessMessage (startTime, "Convert Rasters to geoTiffs")


############################################################
################ error handling exceptions #################
############################################################

# For arctool errors
except arcpy.ExecuteError:
    msgs = arcpy.GetMessages(2)
    arcpy.AddError(msgs)
    print(msgs)

# For other errors
except:
    tbinfo = traceback.format_exc()

    pymsg = "PYTHON ERRORS:\n" + tbinfo + "\nError Info:\n" +str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"

    arcpy.AddError(pymsg)
    arcpy.AddError(msgs)

    print(pymsg)
    print(msgs)
