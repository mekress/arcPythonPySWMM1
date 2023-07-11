# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# ArcPyDEMPPtSCatchV1.py
# Created on: 2023-06-29 09:54:32.00000
#   (generated by ArcGIS/ModelBuilder)
#   Michael E. Kress, Ph. D.
#   College of Staten Island, CUNY
# Derived from: DEMtoSubcatchment1 <Output_Values> 
# Description:
#    1.  Calculate the watershed from a specified pourpoint as a shape file.  First,
#    snap the pourpoint to the accumulation raster.  Next, calculate the corresponding watershed.
#    2.  Calculate the watershed as a polygon and get the area of the shape file.
#    3.  Using the watershed polygon as a mask, get the average slope of the watershed.
#  Previouys calculations:
#    1.  The fill raster from the DEM.
#    2.  The accumulation raster
#    3.  The direction of flow raster.
#    4.  The pour point as a shape file.
#
#   July 3, 2023
#   Revise to use local directory rather than One-Drive canged to V1
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
#Output_drop_raster = ""   #   Not sure what this is for.
#
#   Set directory for GIS Files.
#
GISDirectory="C:\\Zhanyang\\SensorData\\CompoundFlooding\\CompoundFloodModel\\DEMtoSubcatchment\\ShapeOutfall\\"
#Direction = "C:\\Users\\M Kress\\OneDrive - csi.cuny.edu\\Documents\\ArcGIS\\Default.gdb\\FlowDir_Fill2"
Direction = GISDirectory+"CSITileD"
#   Target pour point
NthOutF = GISDirectory+"PPtTMP.shp"
#    Accumulation raster previously calculated
Accumulation = GISDirectory+"csitilea"
#    Snapped pour point
SnapPourPt = GISDirectory+"SnapPPtTMP_1"
#    Watershed Raster calculated here
Subcatchment = GISDirectory+"WShdPPtTMP_1"
#    Watershed as a polygon shape file
NWtrShd2 = GISDirectory+"WtrShdPPtTMPPly.shp"
#    Slope Raster previously calculated 
Flow_Slope = GISDirectory+"CSISlopePrcnt"
#    Masked slope raster calculated here
MaskedSlope = GISDirectory+"MkSlpPPtTMP_1"

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

# Process: Raster to Polygon
tempEnvironment0 = arcpy.env.outputZFlag
arcpy.env.outputZFlag = "Disabled"
tempEnvironment1 = arcpy.env.outputMFlag
arcpy.env.outputMFlag = "Disabled"
arcpy.RasterToPolygon_conversion(Subcatchment, NWtrShd2, "SIMPLIFY", "VALUE", "SINGLE_OUTER_PART", "")
arcpy.env.outputZFlag = tempEnvironment0
arcpy.env.outputMFlag = tempEnvironment1
#
#   Get value of area.  Set up a function to replace the next few lines of code.
#
in_poly=NWtrShd2
atype="GEODESIC"
aunits="ACRES"
sumarea = 0
with arcpy.da.SearchCursor(in_poly, "SHAPE@") as rows:
    for row in rows:
        sumarea += row[0].getArea(atype, aunits)
print sumarea


# Process: Extract by Mask
arcpy.gp.ExtractByMask_sa(Flow_Slope, NWtrShd2, MaskedSlope)

# Process: Get Raster Properties to get the mean slope 
MeanSlope = arcpy.GetRasterProperties_management(MaskedSlope, "MEAN", "")
print MeanSlope

arcpy.CheckInExtension("Spatial")

#   END HERE
#________________________________________________________________________________________
#
##
#   Please see ArcPyCSIGetAreaAverageSlope.py for subroutines for calculating the 
#   area of the polygon (shape file) and mean slope.

