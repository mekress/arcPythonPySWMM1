#
#   July 1, 2023
#   Extract Extract a subset of a raster based on a polygon mask.
#   Michael E. Kress, Ph. D.
#   College of Staten Island, CUNY
#
#   The general idea here is to create a full output file path and input that into the .save command
#
import arcpy, os
from arcpy import env
from arcpy.sa import *
#   Check out the Spatial Analysis Tool Box to prevent license error.
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
#
#   End Header -----
#
#   Define inputs and output files.
#
inRaster=r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodModel\DEMtoSubcatchment\ShapeOutfall\CSISlopePrcnt"
#
mask = r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodModel\DEMtoSubcatchment\ShapeOutfall\WtrShdTrackPly.shp"
#
#   Note:  Characters in Name must be <= 13
outName=r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodModel\DEMtoSubcatchment\ShapeOutfall\WSTrckSlpPrnt"
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
