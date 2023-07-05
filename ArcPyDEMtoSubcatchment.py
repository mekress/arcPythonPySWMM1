# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# DEMtoSubcatchment1.py
# Created on: 2023-06-29 09:54:32.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: DEMtoSubcatchment1 <Output_Values> 
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy,os
from arcpy import env
#
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
# Load required toolboxes
#arcpy.ImportToolbox("Model Functions")

# Script arguments
Output_Values = arcpy.GetParameterAsText(0)
if Output_Values == '#' or not Output_Values:
    Output_Values = "56052.3478269834;7.14733592025083" # provide a default value if unspecified

# Local variables:
DEM_Input = "C:\\Zhanyang\\SensorData\\CompoundFlooding\\CompoundFloodModel\\DEMtoSubcatchment\\CSITiles\\CSITiles.gdb\\CSITiles"
Filled_DEM = "C:\\Users\\M Kress\\OneDrive - csi.cuny.edu\\Documents\\ArcGIS\\Default.gdb\\Fill_CSITile2"
Output_drop_raster = ""
Direction = "C:\\Users\\M Kress\\OneDrive - csi.cuny.edu\\Documents\\ArcGIS\\Default.gdb\\FlowDir_Fill2"
NthOutF = "NthOutF"
Accumulation = "C:\\Users\\M Kress\\OneDrive - csi.cuny.edu\\Documents\\ArcGIS\\Default.gdb\\FlowAcc_Flow2"
SnapPourPt = "C:\\Users\\M Kress\\OneDrive - csi.cuny.edu\\Documents\\ArcGIS\\Default.gdb\\SnapPou_shp8"
Subcatchment = "C:\\Users\\M Kress\\OneDrive - csi.cuny.edu\\Documents\\ArcGIS\\Default.gdb\\Watersh_Flow4"
NWtrShd2 = "C:\\Users\\M Kress\\OneDrive - csi.cuny.edu\\Documents\\ArcGIS\\Default.gdb\\NWtrShd2"
Area = NWtrShd2
Flow_Slope = "C:\\Users\\M Kress\\OneDrive - csi.cuny.edu\\Documents\\ArcGIS\\Default.gdb\\Slope_CSITil1"
MaskedSlope = "C:\\Users\\M Kress\\OneDrive - csi.cuny.edu\\Documents\\ArcGIS\\Default.gdb\\Extract_Slop2"
MeanSlope = "7.14733592025083"

# Process: Fill
arcpy.gp.Fill_sa(DEM_Input, Filled_DEM, "")

# Process: Flow Direction
arcpy.gp.FlowDirection_sa(Filled_DEM, Direction, "NORMAL", Output_drop_raster, "D8")

# Process: Flow Accumulation
arcpy.gp.FlowAccumulation_sa(Direction, Accumulation, "", "FLOAT", "D8")

# Process: Snap Pour Point
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

# Process: Get Field Value
#arcpy.GetFieldValue_mb(NWtrShd2, "Shape_Area", "String", "0")

# Process: Slope
arcpy.gp.Slope_sa(DEM_Input, Flow_Slope, "PERCENT_RISE", "1", "PLANAR", "METER")

# Process: Extract by Mask
arcpy.gp.ExtractByMask_sa(Flow_Slope, NWtrShd2, MaskedSlope)

# Process: Get Raster Properties
arcpy.GetRasterProperties_management(MaskedSlope, "MEAN", "")

# Process: Collect Values
#arcpy.CollectValues_mb("56052.3478269834;7.14733592025083")

arcpy.CheckInExtension("Spatial")
