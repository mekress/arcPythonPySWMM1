# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Process Area and Average Slope .py
# Created on: 2023-06-30 09:54:32.00000
#   Michael E. Kress, Ph. D.
#   College of Staten Island, CUNY
# Usage: Run in ipython or in arcMap
# Description: This routine takes as input a list of the shape files for
# subcatchments and the corresponding slope raster files and creates
# a csv text file where each row is a subcatchment and the columns are the area
# and average slope.
# ---------------------------------------------------------------------------
#
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
#
#  Do calculations. ------------------------------------------------------------------------------------------
#
WDirectory=r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodingPythonSource\DEMtoSubcatchmentWork"
os.chdir(WDirectory)
print("Working Directory for the resulting txt file "+os.getcwd())
#
#   Specify the input files for the polygon area and
#   slope raster.
#
In_Poly=r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodModel\DEMtoSubcatchment\ShapeOutfall\NWtrShd.shp"
InSlope = "C:\\Users\\M Kress\\OneDrive - csi.cuny.edu\\Documents\\ArcGIS\\Default.gdb\\Extract_Slop2"
#
#   Specify a list of Subcatchment shape file names
#
CatchLst=["NentShdPoly1","NEnt2ShdPoly","NWtrShd","WPrkBBShdPoly",
          "WWbrkBB3ShdPoly","NLRShdPoly","WWbrkBB2ShdPoly",
          "WWTrckShdPoly","BBCF2ShdPly"]
SlopeLst=["NentSlpPrcnt","Nent2SlpPrcnt","NWtrSlope","WPrkBBSlpPrcn",
          "WWbrkBB3SlPr","NLRSlopePrcnt","WWbrkBB2SlPr",
          "WWTrckSlopePr","BBCF2SlopePr"]
CatchDir="C:\\Zhanyang\\SensorData\\CompoundFlooding\\CompoundFloodModel\\DEMtoSubcatchment\\ShapeOutfall\\"
n=len(CatchLst)
print(n)
print(CatchLst)
print(CatchDir)
Summary=['Name','Area','Slope']
print(Summary)
#
OutputFile="AreaSlope.txt"
output = file(OutputFile, "w")  
print("Opened Output " + OutputFile +" \n")
output.write("Name, Area (Acrea), Average Slope \n")
#
for i in range(0,n):
    CatchFile=CatchDir+CatchLst[i]+".shp"
    SlopeFile=CatchDir+SlopeLst[i]
    #print(CatchFile)
    #print(SlopeFile)
    #
    #   Area ---
    #
    atype="GEODESIC"
    aunits="ACRES"
    sumarea = shedarea(CatchFile, atype, aunits)
    #print(sumarea)
    #
    #   Average slope
    #
    #print(i,CatchLst[i])
    #print(SlopeFile)
    MeanSlope = aveslope(SlopeFile)
    #print(MeanSlope)
    output.write(CatchLst[i]+","+str(sumarea)+","+str(MeanSlope)+"\n")
output.close()
#
arcpy.CheckInExtension("Spatial")
#
#   Fini
#

