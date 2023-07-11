# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# ArcPyCSIGetPolyAreaAverageSlope
# Process Area and Average Slope .py
# Created on: 2023-06-30 09:54:32.00000
# Michael E. Kress, Ph. D.
# College of Staten Islan, CUNY
# Usage: Run in ipython or in arcMap
# Description: This routine takes as input a shape file for
# subcatchments and the corresponding slope raster file and creates
# a csv text file where each row is a subcatchment and the columns are the area
# and average slope.
# This routine is derived from:  ArcPyCSIGetAreaAverageSlope, which does the calculation
# for a list of polygons.
# July 6, 2023
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
#In_Poly=r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodModel\DEMtoSubcatchment\ShapeOutfall\NWtrShd.shp"
#InSlope = "C:\\Users\\M Kress\\OneDrive - csi.cuny.edu\\Documents\\ArcGIS\\Default.gdb\\Extract_Slop2"
#In_Poly=r"C:\\Users\\M Kress\\OneDrive - csi.cuny.edu\\Documents\\ArcGIS\\Default.gdb\\PPtsWtrShPly"
In_Poly = r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodModel\DEMtoSubcatchment\ShapeOutfall\\WtrShdTrackPly.shp"
InSlope = r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodModel\DEMtoSubcatchment\ShapeOutfall\\wstrckslpprnt"
#
#  Write header line for output file
#
Summary=['Name','Area','Slope']
print(Summary)
#
OutputFile="AreaSlopePoly.txt"
output = file(OutputFile, "w")  
print("Opened Output " + OutputFile +" \n")
output.write("Name, Area (Acrea), Average Slope \n")
#
#   Area ---
#
atype="GEODESIC"
aunits="ACRES"
sumarea = shedarea(In_Poly, atype, aunits)
print(sumarea)
#
#   Average slope
#
MeanSlope = aveslope(InSlope)
print(MeanSlope)
output.write("PolyName"+","+str(sumarea)+","+str(MeanSlope)+"\n")
output.close()
#
arcpy.CheckInExtension("Spatial")
#
#   Fini
#

