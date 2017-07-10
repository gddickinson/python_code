# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Step7_Import_shadeData.py
# Created on: 2017-05-15 15:35:03.00000
#   (generated by ArcGIS/ModelBuilder)
# Description:
# ---------------------------------------------------------------------------

from __future__ import division, print_function
import sys
import os
import gc
import time
import traceback
from datetime import timedelta
from math import radians, sin, cos, ceil, sqrt
# Import arcpy module
import arcpy
from arcpy import env

arcpy.env.workspace = r"C:\Google Drive\SiCr_Digitization\scripts\data"
env.overwriteOutput = True

# Local variables:
##dataSheet = r"C:\Google Drive\SiCr_Digitization\scripts\output2.xlsx"
##shade_fc = "shade_fc"
##shade_fc_shp = r"C:\Google Drive\SiCr_Digitization\shadeOutput"
##shade_fc_shp = shade_fc_shp + "\\" + shade_fc + ".shp"


# From ArcMap #

dataSheet = arcpy.GetParameterAsText(0)
shade_fc = arcpy.GetParameterAsText(1)
shade_fc_shp = arcpy.GetParameterAsText(2)

#dataSheet2 = dataSheet + "\\Sheet1$"
arcpy.ExcelToTable_conversion(dataSheet,"outdbf.dbf")

shade_fc_shp = shade_fc_shp + "\\" + shade_fc + ".shp"

arcpy.AddMessage(dataSheet)
arcpy.AddMessage(shade_fc_shp)


#enable garbage collection
gc.enable()

try:
    arcpy.AddMessage("Step 8: Import shade data as featureclass")
    print("Step 8: Import shade data as featureclass")

    #keeping track of time
    startTime= time.time()

    # Process: Make XY Event Layer
    arcpy.MakeXYEventLayer_management("outdbf.dbf", "longitude", "latitude", shade_fc, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision", "")

    # Process: Copy Features
    arcpy.CopyFeatures_management(shade_fc, shade_fc_shp, "", "0", "0", "0")

    #Add feature class to map layer

    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = mxd.activeDataFrame
    newLayer = arcpy.mapping.Layer(shade_fc_shp)
    arcpy.mapping.AddLayer(df,newLayer,"TOP")

    arcpy.AddMessage("Shade featureclass added to map")
    print("Shade featureclass added to map")


    endTime = time.time()

    elapsedmin= ceil(((endTime - startTime) / 60)* 10)/10

    print("Process Complete in {0} minutes".format(elapsedmin))
    arcpy.AddMessage("Process Complete in %s minutes" % (elapsedmin))


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