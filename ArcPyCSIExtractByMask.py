# ---------------------------------------------------------------------------
#
#   July 1, 2023
#   Extract Extract a subset of a raster based on a polygon mask.
#   Michael E. Kress, Ph. D.
#   College of Staten Island, CUNY
#
#   Purpose:
#         This routine takes a mask shape file and an input raster slope file
#       and creates a raster slope file of the masked area which is used for the
#       subcatchment average slope calculation.
#    Julky 21, 2023:  Code clean-up, testing and verification.
#
# ----------------------------------------------------------------------------
#
#   Specify the arcpy parameters and libraries.
#
import arcpy, os
from arcpy import env
from arcpy.sa import *
#   Check-out the Spatial Analysis Tool Box to prevent license error.
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
#
#   End Header -----
#
#   Define inputs and output files.
#
inRaster=r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodModel\DEMtoSubcatchment\ShapeOutfall\CSISlopePrcnt"
#
mask = r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodModel\DEMtoSubcatchment\ShapeOutfall\PPts1WtrShPly.shp"
#mask = r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodModel\DEMtoSubcatchment\ShapeOutfall\wtrshdarsb3aPly.shp"
#
#   Note:  Characters in Name must be <= 13
#outName=r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodModel\DEMtoSubcatchment\ShapeOutfall\WSarsb3aSlp"
outName=r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodModel\DEMtoSubcatchment\ShapeOutfall\ppts1slpprnta"
#
#   Process extraction.
#
outExtractByMask = ExtractByMask(inRaster, mask)
#
#   Save output raster.
#
outExtractByMask.save(outName)
#
arcpy.CheckInExtension("Spatial")
#
#   Fini
#
