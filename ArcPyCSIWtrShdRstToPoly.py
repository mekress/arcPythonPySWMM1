# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# ArcPyCSIWtrShdRstToPoly.py
# Derived from:  ArcPyCSIPPtToWtrShdRstr.py and ArcPyDEMPPtSCatchV1.py
# Description:
#    1.  Calculate the watershed from a specified pourpoint in a shape file.
#           First, snap the pourpoint to the accumulation raster.
#           Second, calculate the corresponding watershed as a raster.
#           Next, evaluate
#    2.  This Routine -- Calculate the watershed as a polygon and get the area of the shape file.
#    3.  Using the watershed polygon as a mask, get the average slope of the watershed.
#           This can be done with ArcPyCSIExtractByMask followed by ArcPyCSIGetPolyAreaAverageSlope
#  Previouys calculations:
#    1.  The fill raster from the DEM.
#    2.  The accumulation raster
#    3.  The direction of flow raster.
#    4.  The pour point as a shape file.
#
#   July 9, 2023
#   Initial coding.
#   July 21, 2023
#   Code clean-up, testing and verification.
#
# ---------------------------------------------------------------------------
#
# Import arcpy module
#
import arcpy, os
from arcpy import env
from arcpy.sa import *
#   Check out the Spatial Analysis Tool Box.
arcpy.CheckOutExtension("Spatial")
#   Set envvironment so that output files can be overwritten.
#   If running in arcMap, also have to set the Geoprocessin Optin to allow overwriting 
#   This is in the Georocessing menue
arcpy.env.overwriteOutput = True
#
#   End Header -----
#
#   Set working directory
#
WDirectory=r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodingPythonSource\DEMtoSubcatchmentWork"
os.chdir(WDirectory)
print("Working Directory for the resulting txt file "+os.getcwd())
#
# Local variables:
#
#   Set directory for GIS Files.
#
GISDirectory="C:\\Zhanyang\\SensorData\\CompoundFlooding\\CompoundFloodModel\\DEMtoSubcatchment\\ShapeOutfall\\"
#
#   In the pipline of the process, the output of the previous calculation for
#   getting the raster version of the watershed (subcatchment) is input to
#   this routine for creatingn a shape file of the raster.
#
OutPutWatershed="wtrshdarsb3a"
Subcatchment = GISDirectory+OutPutWatershed
#
#    Watershed as a polygon shape file
#
#NWtrShd2 = GISDirectory+"WtrShdPPtTMPPly.shp"
NWtrShd2 = GISDirectory+OutPutWatershed+"Ply.shp"
#
###########################################################
#
# Process: Raster to Polygon
#
#   Save arcpy environment
#
tempEnvironment0 = arcpy.env.outputZFlag
arcpy.env.outputZFlag = "Disabled"
tempEnvironment1 = arcpy.env.outputMFlag
arcpy.env.outputMFlag = "Disabled"
#
#   Do the calculation.
#
arcpy.RasterToPolygon_conversion(Subcatchment, NWtrShd2, "SIMPLIFY", "VALUE", "SINGLE_OUTER_PART", "")
#
#   Return to original arcpy environment.
#
arcpy.env.outputZFlag = tempEnvironment0
arcpy.env.outputMFlag = tempEnvironment1
#
#  Return license.
#
arcpy.CheckInExtension("Spatial")
#
Message=input("End Here WtrShdRste To Poly")

#   END HERE
#________________________________________________________________________________________
#
##
#   Please see ArcPyCSIGetAreaAverageSlope.py for subroutines for calculating the 
#   area of the polygon (shape file) and mean slope.

