# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# ArcPyCSIPPtToWtrShdRstr.py
# Derived from:  ArcPyDEMPPtSCatchV1.py
#   Michael E. Kress, Ph. D.
#   College of Staten Island, CUNY
# Description:
#    1.  Calculate the watershed from a specified pourpoint in a shape file.
#           First, snap the pourpoint to the accumulation raster.
#           Second, calculate the corresponding watershed as a raster.
#           Next, evaluate 
#    2.  Calculate the watershed as a polygon and get the area of the shape file.
#    3.  Using the watershed polygon as a mask, get the average slope of the watershed.
#  Previouys calculations:
#    1.  The fill raster from the DEM.
#    2.  The accumulation raster
#    3.  The direction of flow raster.
#    4.  The pour point as a shape file.
#
#   July 9, 2023
#   Initial coding.
#   July 21, 2023
#   Code cleanup and testing and verification.
#
# ---------------------------------------------------------------------------

# Import arcpy module
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
#Direction = "C:\\Users\\M Kress\\OneDrive - csi.cuny.edu\\Documents\\ArcGIS\\Default.gdb\\FlowDir_Fill2"
Direction = GISDirectory+"CSITileD"
#   Specify the shape file containing the input pour point.
InputPourPointShapeFile="WbArSbPPt3.shp"
NthOutF = GISDirectory+InputPourPointShapeFile
#    Accumulation raster previously calculated
Accumulation = GISDirectory+"csitilea"
#    Snapped pour point
OutputSnapFile="SnpPPtsArSb3"
SnapPourPt = GISDirectory+OutputSnapFile
#    Watershed Raster name calculated here
OutPutWatershed="WtrShdArSb3a"
Subcatchment = GISDirectory+OutPutWatershed
# Process: Snap Pour Point
print(Accumulation)
print(NthOutF)
print(SnapPourPt)
#################   Make sure that there is an Id field in the polygon
#                   with the pour point.  The situation arises because
#                   when the point shp file it creates a field named, "name"
#                   On the other hand when the points are put into other shape
#                   files they have a field called, "Id".  We continue to use
#                   the Id field identifier.
#
###########################################################
arcpy.gp.SnapPourPoint_sa(NthOutF, Accumulation, SnapPourPt, "1", "Id")

# Process: Watershed
arcpy.gp.Watershed_sa(Direction, SnapPourPt, Subcatchment, "Value")
#
##########################################################
#
#   Pause Here and evalute the Watershed based on the pour points.
#
Message=input("End Here and evaluate the watersheds")
#
#
arcpy.CheckInExtension("Spatial")
#
#   END HERE
#########################################################
