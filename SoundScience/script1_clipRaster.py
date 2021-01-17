import os
import csv
import arcpy
from os import path
from arcpy import da
from arcpy import env
from arcpy.sa import *
import glob
from pandas import read_csv

arcpy.CheckOutExtension("Spatial")

env.overwriteOutput = True
env.workspace = r'C:\Users\George\Desktop\LiDAR_classification\testing'

polygon_shp = path.join(env.workspace, 'PVER_blocks_negative20m.shp')
vertex_csv_path = r'C:\Users\George\Desktop\LiDAR_classification\testing\poly_vertex.csv'
rasterInput_path = r'C:\Users\George\Desktop\LiDAR_classification\testing\pver_bhb_BHC.tif'
rasterSavePath =  r'C:\Users\George\Desktop\LiDAR_classification\testing\output\clip'

geoTiffPath =  r'C:\Users\George\Desktop\LiDAR_classification\testing\output\rasterConversion'
fragResultsPath = r'C:\Users\George\Desktop\LiDAR_classification\fragStat_tests\results'
fcaFile = r'C:\Users\George\Desktop\LiDAR_classification\fragStat_tests\test1.fca'

fragOutput =  r'C:\Users\George\Desktop\LiDAR_classification\fragStat_tests\results\frag_out'


workingDirectory = os.getcwd()


def getPolygonCoordinates(fc):
    """For each polygon geometry in a shapefile get the sequence number and
    and coordinates of each vertex and tie it to the OID of its corresponding
    polygon"""

    vtx_dict = {}
    s_fields = ['OID@', 'Shape@XY']
    pt_array = da.FeatureClassToNumPyArray(polygon_shp, s_fields,
        explode_to_points=True)

    for oid, xy in pt_array:
        xy_tup = tuple(xy)

        if oid not in vtx_dict:
            vtx_dict[oid] = [xy_tup]
        # this clause ensures that the first/last point which is listed
        # twice only appears in the list once
        elif xy_tup not in vtx_dict[oid]:
            vtx_dict[oid].append(xy_tup)

    vtx_sheet = []
    for oid, vtx_list in vtx_dict.iteritems():
        for i, vtx in enumerate(vtx_list):
            vtx_sheet.append((oid, i, vtx[0], vtx[1]))

    return vtx_sheet


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

    return finalList


#arcpy.RasterToOtherFormat_conversion(clip,"OtherFormat","BIL")

def runFragstats():
    env.workspace = r'C:\Users\George\Desktop\LiDAR_classification\testing\output'
    os.chdir(r"C:\Program Files (x86)\Fragstats 4")

    # Call fragstats from script.
    print "\n\nCREATING A FRAGSTATS BATCH FILE ...\n"
    # fragstats batch file
    batchFileName = os.path.join(geoTiffPath,"batch.fbt")
    # tif list
    fragTifs = []

    for file in os.listdir(geoTiffPath):
        if file.endswith(".tif"):
            fragTifs.append(file)


    # delete old batch file
    try:
        os.remove(batchFileName)
    except:
        pass

    # Batch file
    fbtFile = open(batchFileName, 'a')
    for tif in fragTifs:
        fbtFile.write(geoTiffPath + "\\" + tif + ", x, 999, x, x, 1, IDF_GeoTIFF\n")
    fbtFile.close()


    # Run FRAGSTATS
    print "\nRUN Fragstats batch file ...\n"
    frgExePath = 'frg.exe'
    try:
        cmd = frgExePath + " -m " + fcaFile + " -b " + batchFileName + " -o " + fragOutput
        print(cmd)
        os.system(cmd)
    except:
        print "\n\nUnable to run FRAGSTATS. Quitting!\n\n"
        sys.exit()

    ### Reformat fragstats output files
    print "\n\nREFORMATTING THE FRAGSTATS CLASS AND LANDSCAPE METRICS OUTPUT FILES ..."
    cl_infile_name = fragResultsPath + r"\frag_out.class"
    cl_outfile_name = fragResultsPath + r"\temp_class_out.csv"
    ##ls_infile_name = fragResultsPath + r"\frag_out.land"
    ##ls_outfile_name = fragResultsPath + r"\Fragstats_Landscape_Metrics_Output.csv"
    ##

    ### Make class file
    with open(cl_infile_name, 'rb') as csvfile:
        reader = csv.reader(csvfile, skipinitialspace=True)
        infile = []
        for row in reader:
            line = [item.strip() for item in row]
            infile.append(line)

    with open(cl_outfile_name, "wb") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(infile)

    # Rearrange class file
    df = read_csv(cl_outfile_name)
    df = df.pivot(index="LID", columns="TYPE")
    df.to_csv(fragResultsPath + r"\Fragstats_Class_Metrics_Output.csv", na_rep=0, sep=',',
              float_format="%.4f")

    ### Make landscape file
    ##with open(ls_infile_name, 'rb') as csvfile:
    ##    reader = csv.reader(csvfile, skipinitialspace=True)
    ##    infile = []
    ##    for row in reader:
    ##        line = [item.strip() for item in row]
    ##        infile.append(line)
    ##
    ##with open(ls_outfile_name, "wb") as outfile:
    ##    writer = csv.writer(outfile)
    ##    writer.writerows(infile)

    # Finish run
    os.chdir(workingDirectory)
    print "\n\nALL PROCESSES COMPLETED SUCCESSFULLY. PLEASE VIEW THE OUTPUT TABLES IN THE 'FINAL_RESULTS' SUBDIRECTORY IN THE 'WORKING DIRECTORY'."


########## run ################
#pointsList = getPolygonCoordinates(polygon_shp)
#clipList = clipRaster(pointsList)
runFragstats()
