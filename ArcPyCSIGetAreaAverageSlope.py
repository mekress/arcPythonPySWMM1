# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Process Area and Average Slope .py
# Created on: 2023-06-30 09:54:32.00000
#   Michael E. Kress, Ph. D.
# Usage: Run in python or in arcMap
# Description: This routine takes as input a list of the shape files for
# subcatchments and the corresponding slope raster files and creates
# a csv text file where each row is a subcatchment and the columns are the area
# and average slope.
#   Oct 10,2023
#   Used for different shape files and rasters and revised some to have inputs in the
#   same area of the code.
#   This does the same calculation as  ArcPyCSIAllLayersAreaSlope in
#   a less automated way.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
#   Check out the Spatial Analysis Tool Box to prevent license error.
arcpy.CheckOutExtension("Spatial")
#   Set envvironment so that output files can be overwritten.
#   If running in arcMap, also have to set the Geoprocessin Optin to allow overwriting 
#   This is in the Georocessing menue
arcpy.overwriteOutput = True
#
#   Define subroutines -----
#
#   Polygon Area
#
def shedarea(in_poly, atype, aunits):
    sumarea = 0
    with arcpy.da.SearchCursor(in_poly, "SHAPE@") as rows:
        for row in rows:
            sumarea += row[0].getArea(atype, aunits)
    return sumarea
#
#   Average Slope
#
def aveslope(inslope):
    # Process: Get Raster Properties
    MeanSlope = arcpy.GetRasterProperties_management(inslope, "MEAN", "")
    return MeanSlope
######################################################################
#
#  Specify the run specific files and directory. ------------------------------------------------------------------------------------------
#
#WDirectory=r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodingPythonSource\DEMtoSubcatchmentWork"
WDirectory=r"C:\Zhanyang\SensorData\CompoundFlooding\SWMM\PySWMM\Campus\Juy2023Subcatchments"
os.chdir(WDirectory)
print("Working Directory for the resulting txt file "+os.getcwd())
#
#   Specify the input files for the polygon area and
#   slope raster.
#
In_Poly=r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodModel\DEMtoSubcatchment\ShapeOutfall\NWtrShd.shp"
InSlope = "C:\\Users\\M Kress\\OneDrive - csi.cuny.edu\\Documents\\ArcGIS\\Default.gdb\\Extract_Slop2"
#
#   Specify a list of Subcatchment shape and raster file names
#
CatchLst=["S2APoly","S2BPoly2","S2subsecCPoly","S2BCWoodsPoly"]
SlopeLst=["S2APolySlp","S2BPoly2Slp","S2CPolySlp","S2DPolySlp"]
#
#CatchLst=["NentShdPoly1","NEnt2ShdPoly","NWtrShd","WPrkBBShdPoly",
#          "WWbrkBB3ShdPoly","NLRShdPoly","WWbrkBB2ShdPoly",
#          "WWTrckShdPoly","BBCF2ShdPly"]
#SlopeLst=["NentSlpPrcnt","Nent2SlpPrcnt","NWtrSlope","WPrkBBSlpPrcn",
#          "WWbrkBB3SlPr","NLRSlopePrcnt","WWbrkBB2SlPr",
#          "WWTrckSlopePr","BBCF2SlopePr"]
#
#   Specify the location of the directory which contains the shape and raster files.
#
#CatchDir="C:\\Zhanyang\\SensorData\\CompoundFlooding\\CompoundFloodModel\\DEMtoSubcatchment\\ShapeOutfall\\"
CatchDir="C:\\Zhanyang\\SensorData\\CompoundFlooding\\SWMM\\PySWMM\\Campus\\Juy2023Subcatchments\\"
#
#   Open output files
#
#OutputFile="AreaSlope1.txt"
OutputFile="S2RevAreaSlope.txt"
output = file(OutputFile, "w")  
print("Opened Output " + OutputFile +" \n")
output.write("Name, Area (Acrea), Average Slope \n")
#
# ##############################################
#
#   Do Calculation.
#
n=len(CatchLst)
print(CatchDir)
print(CatchLst)
print(SlopeLst)
Summary=['Index','File','Calculation']
print(Summary)
#
#   Iterate through the shape and raster files and do the calculations and write the
#   the output.
#
for i in range(0,n):
    CatchFile=CatchDir+CatchLst[i]+".shp"
    SlopeFile=CatchDir+SlopeLst[i]
    #
    #   Area ---
    #
    atype="GEODESIC"
    aunits="ACRES"
    sumarea = shedarea(CatchFile, atype, aunits)
    print(i, CatchLst[i],sumarea)
    #
    #   Average slope
    #
    MeanSlope = aveslope(SlopeFile)
    print(i, SlopeLst[i],MeanSlope)
    output.write(CatchLst[i]+","+str(sumarea)+","+str(MeanSlope)+"\n")
output.close()
#
arcpy.CheckInExtension("Spatial")
#
#   Fini
#

